__author__ = 'ryanvade'
import time, serial, sys, os

tty = "/dev/ttyAMA0" # for PC
#tty = "/dev/ttyUSB0" #for raspberry pi

try:#lets try to open the getty
    with open(tty) as file:
        pass
except IOError as e:#if unable to do so...
    print("Unable to open or do not have permission to open",tty)
    sys.exit(1)#exit with error

#port will be the connection to the arduino
port = serial.Serial(tty, baudrate=115200, timeout=3.0)

