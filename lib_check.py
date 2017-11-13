#! /usr/bin/env python

import imp

try:
    imp.find_module('urllib')
    print('PASS :: urllib is installed')
except ImportError:
    print('FAIL :: Please install urllib python module')
    
try:
    imp.find_module('termcolor')
    print('PASS :: termcolor is installed')
except ImportError:
    print('FAIL :: Please install termcolor python module')

try:
    imp.find_module('ephem')
    print('PASS :: ephem is installed')
except ImportError:
    print('FAIL :: Please install PyEphem python module')
