__author__ = 'ryanvade'
import serial, time, os, sys, pprint
import RPi.GPIO as GPIO

#pp = pprint.PrettyPrinter(indent=4)
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(7, GPIO.OUT)

port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=None)
port.flushInput()
port.flushOutput()


data = bytearray()
data.append(1)
port.write(data)
port.close()