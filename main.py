__author__ = 'ryanvade'
#Program to be run on the raspberry pi
import serial, time, os, sys, pprint, errno

#variables
pp = pprint.PrettyPrinter(indent=4)
tty = "/dev/ttyACM0"

#Is the nanpy module available?
try:
    import nanpy
    from nanpy import (Arduino, OneWire, Lcd, SerialManager, ArduinoApi, Stepper, Servo)
except ImportError as e:
    print(e)
    sys.exit(1)

connectionName = SerialManager(device=tty)
uno = ArduinoApi(connection=connectionName)

#turn led on pin 13 on for 4 seconds then turn it off
uno.pinMode(13,uno.OUTPUT)
uno.digitalWrite(13, uno.HIGH)
time.sleep(4)
uno.digitalWrite(13, uno.LOW)
