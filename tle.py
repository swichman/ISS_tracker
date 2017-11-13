#! /usr/bin/env python

import urllib
import math
import time
from datetime import datetime
from termcolor import colored
import ephem
import os


#########################################
#   Change this information to match    #
#   your local lat/lon and altitude     #
#########################################
local_lat = '35.105596'
local_lon = '-106.629269'
local_alt = 1620 # meters


#########################################
#   Nothing needs to be changed         #
#           below this                  #
#########################################
print "\n\nGetting latest TLE from nasa.gov"
# download latest info from NASA
testfile = urllib.URLopener()
testfile.retrieve("https://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/orbit/ISS/SVPOST.html", "SVPOST.txt")

input_file = open('SVPOST.txt')

# search for latest TLE information
cond = False
while cond == False:
	line = input_file.readline()
	if 'TWO LINE MEAN ELEMENT SET' in line:
		line = input_file.readline()
		line = input_file.readline()
		break
		
tle1 = input_file.readline()
tle2 = input_file.readline()
input_file.close()
os.remove("SVPOST.txt")

print "Preparing TLE for use"
# format TLE for use
tle1 = tle1.strip()
tle2 = tle2.strip()

if not os.path.exists('./products/'):
	os.makedirs("./products")
if not os.path.exists('./logs/'):
	os.makedirs("./logs")

tle_file = open("./products/ISS_TLE.txt","w")
tle_file.write(tle1 + "\n")
tle_file.write(tle2)
tle_file.close()

print "\n\n" + "                    TWO LINE MEAN ELEMENT SET\n" + colored('                   .........................................................................','yellow')
print colored('                   . ','yellow') + colored(tle1,'white') + colored(' .','yellow')
print colored('                   . ','yellow') + colored(tle2,'white') + colored(' .','yellow')
print colored('                   .........................................................................\n\n','yellow')


log_file = open("./logs/log.txt","w")
log_file.write("Starting logging for ISS contact watcher \n\n")
log_file.write(tle1 + "\n")
log_file.write(tle2 + "\n\n")
log_file.close()

# define degrees
degrees_per_radian = 180.0 / math.pi

# define home position
home = ephem.Observer()
home.lon = '-106.520816'   # +E
home.lat = '35.080043'      # +N
home.elevation = 1673.1 # meters
print "Home coordinates are" + colored(' 35.080043 ','white') + colored('N','red') + colored(' -106.520816 ','white') + colored('E','red') + "\n\n"

# define iss position
iss = ephem.readtle('ISS', tle1, tle2)

home.date = datetime.utcnow()
next_contact = home.next_pass(iss)
duration = (next_contact[4] - next_contact[0]) * 86400
print "next pass at " + colored("%s (UTC)" % next_contact[0],'green') +  " with a duration of " + colored("%f" % duration,'green') + " seconds.\n\n"
print "Rise AZ  : " + colored("%f" % (next_contact[1] * degrees_per_radian),'green')
print "Fade AZ  : " + colored("%f" % (next_contact[5] * degrees_per_radian),'green')
print "Max EL   : " + colored("%f" % (next_contact[3] * degrees_per_radian),'green')
print "Mid Time : " + colored(next_contact[2],'green')
print "\n\n"

print "======= Beginning ISS sky tracking ======="

neg_horizon = False

while True:
    home.date = datetime.utcnow()
    iss.compute(home)
    dtg = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.utcnow())
    if (iss.alt * degrees_per_radian) < .7:
		print colored(dtg + " (UTC)",'red') + "    ISS is below horizon... looking again in 10 seconds    <<<>>>    AZ : %5.3f deg    ||    EL : %4.3f deg" % (iss.az * degrees_per_radian, iss.alt * degrees_per_radian)
		if neg_horizon == False:
			log_file = open("./logs/log.txt", "a")
			log_file.write(colored(dtg + " (UTC) ", 'red') + "ISS is below horizon, will begin logging when station rises at %s (UTC)\n\n" % next_contact[0])
			log_file.close()
			neg_horizon = True
		if (iss.alt * degrees_per_radian) >= 0 and (iss.alt * degrees_per_radian) < .7:
			log_file = open("./logs/log.txt", "a")
			log_file.write(colored(dtg + " (UTC)",'red') + "    ISS is below horizon... looking again in 10 seconds    <<<>>>    AZ : %5.3f deg    ||    EL : %4.3f deg\n" % (iss.az * degrees_per_radian, iss.alt * degrees_per_radian))
			log_file.close()
		time.sleep(10.0)
	
    if (iss.alt * degrees_per_radian) >= .7:
		print colored(dtg + " (UTC)",'white') + "    ISS    :::::    AZ : %5.1f deg    EL : %4.1f deg" % (iss.az * degrees_per_radian, iss.alt * degrees_per_radian)
		log_file = open("./logs/log.txt","a")
		log_file.write(colored(dtg + " (UTC)",'white') + "    ISS    :::::    AZ : %5.1f deg    EL : %4.1f deg\n" % (iss.az * degrees_per_radian, iss.alt * degrees_per_radian))
		log_file.close()
		time.sleep(1.0)
		neg_horizon = False
