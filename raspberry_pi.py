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
    import raspberrypi
    import RPi.GPIO as GPIO
except ImportError:
    print("Module not found")
    sys.exit(1)

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(7, GPIO.OUT)

try: #lets try to open the getty
    with open(tty) as file:
        pass
except IOError as e: #if unable to do so...
    print(e.errno)
    print(e)
    sys.exit(1) #exit with error

port = serial.Serial(tty, baudrate=115200, timeout=None)
port.flushInput()
port.flushOutput()


data = bytearray()
data.append(1)
port.write(data)
port.close()