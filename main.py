__author__ = 'ryanvade'
import time, serial, sys, os, errno

tty = "/dev/ttyAMA0"

try:#lets try to open the getty
    with open(tty) as file:
        pass
except IOError as e:#if unable to do so...
    print(e)
    sys.exit(1)#exit with error

#port will be the connection to the arduino
port = serial.Serial(tty, baudrate=115200, timeout=3.0)

