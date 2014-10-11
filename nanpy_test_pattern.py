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
motor1PWM = 5
motor3PWM = 6
motor2PWM = 9
motor4PWM = 3

dir1 = 4
dir2 = 2
dir3 = 7
dir4 = 10

GND1 = 12
GND2 = 11

uno.pinMode(motor1PWM, uno.OUTPUT)
uno.pinMode(motor2PWM, uno.OUTPUT)
uno.pinMode(motor3PWM, uno.OUTPUT)
uno.pinMode(motor4PWM, uno.OUTPUT)
uno.pinMode(dir1, uno.OUTPUT)
uno.pinMode(dir2, uno.OUTPUT)
uno.pinMode(dir3, uno.OUTPUT)
uno.pinMode(dir4, uno.OUTPUT)
uno.pinMode(GND1, uno.OUTPUT)
uno.pinMode(GND2, uno.OUTPUT)

uno.digitalWrite(GND1, uno.LOW)
uno.digitalWrite(GND2, uno.LOW)

uno.digitalWrite(dir1, uno.HIGH)
uno.digitalWrite(dir2, uno.LOW)
uno.digitalWrite(dir3, uno.LOW)
uno.digitalWrite(dir4, uno.HIGH)

uno.digitalWrite(motor1PWM, 35)
uno.digitalWrite(motor2PWM, 35)
uno.digitalWrite(motor3PWM, 35)
uno.digitalWrite(motor4PWM, 35)

time.sleep(5)

uno.digitalWrite(dir1, uno.LOW)
uno.digitalWrite(dir2, uno.HIGH)
uno.digitalWrite(dir3, uno.HIGH)
uno.digitalWrite(dir4, uno.LOW)

time.sleep(5)
