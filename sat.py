#! /usr/bin/env python

import urllib
import math
import time
from datetime import datetime
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
#   Do not change any code below	#
#   		this line     		#
#########################################
print "\nGenerating the Station Acquisition Table\n\n"

print "Getting latest TLE from nasa.gov"
# download latest info from NASA
testfile = urllib.URLopener()
testfile.retrieve("https://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/orbit/ISS/SVPOST.html", "SVPOST.txt")
print "."
input_file = open('SVPOST.txt')
print "."
# search for latest TLE information
cond = False
while cond == False:
	line = input_file.readline()
	if 'TWO LINE MEAN ELEMENT SET' in line:
		line = input_file.readline()
		line = input_file.readline()
		break
print "."		
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

print "Generating file"
sat = open("./products/sat.txt","w")
sat.write("\n" + "TWO LINE MEAN ELEMENT SET\n" + '.........................................................................\n')
sat.write('. ' + tle1 + ' .\n')
sat.write('. ' + tle2 + ' .\n')
sat.write('.........................................................................\n\n')
sat.write(' Rise               | Fade               | RiseAz | FadeAz | MaxEl | Dur\n')
sat.write('=========================================================================\n')
sat.close()

iss = ephem.readtle('ISS', tle1, tle2)
home = ephem.Observer()
home.lon = local_lon
home.lat = local_lat
home.elevation = local_alt 
home.date = datetime.utcnow()
next_contact = home.next_pass(iss)
iss.compute(home)
degrees_per_radian = 180.0 / math.pi
i = home.next_pass(iss)[0]

while i >= next_contact[0] - 1:
	sat = open("./products/sat.txt","a")
	#print "{}  ::  {}".format(i,next_contact[0])
	duration = (next_contact[4] - next_contact[0]) * 86400
	home.date = next_contact[4] + .02
	line = " %s | %s | %6.2f | %6.2f | %5.2f | %3d\n" % (next_contact[0], next_contact[4], next_contact[1]*degrees_per_radian, (next_contact[5]*degrees_per_radian), next_contact[3]*degrees_per_radian, duration)
	sat.write(line)
	sat.close()
	next_contact = home.next_pass(iss)

sat=open("./products/sat.txt","a")
sat.write('\n\n')
sat.close()
print "Finished\n\n"

