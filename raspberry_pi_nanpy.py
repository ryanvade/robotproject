__author__ = 'ryanvade'
#Program to be run on the raspberry pi
import serial, time, os, sys, pprint, errno

#variables
pp = pprint.PrettyPrinter(indent=4)
tty = "/dev/ttyAMA0"

# is this an Arm system (raspberry pi)
if not os.uname()[4].startswith("arm"):
    sys.stdout.write("Cannot run on: ")
    print(os.uname()[4])
    sys.exit(1)

#Is the RPi module available?
try:
    
    import RPi.GPIO as GPIO
except ImportError as e:
    print(e)
    sys.exit(1)

try:
    from nanpy import Arduino
    from nanpy import (OneWire, LCD)
    from nanpy import SerialManager
except ImportError as e:
    print(e)
    sys.exit(1)
