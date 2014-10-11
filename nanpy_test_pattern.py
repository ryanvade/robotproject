__author__ = 'ryanvade'
# Program to be run on the raspberry pi
import serial, time, os, sys, pprint, errno, csv

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


#variables
pp = pprint.PrettyPrinter(indent=4)
tty = "/dev/ttyAMA0"
connectionName = SerialManager(device=tty)
uno = ArduinoApi(connection=connectionName)
low = uno.LOW
high = uno.HIGH
message = " "
#turn led on pin 13 on for 4 seconds then turn it off
motor1PWM = 5
motor3PWM = 6
motor2PWM = 9
motor4PWM = 3


GND1 = 12
GND2 = 11

dir1 = 4
dir2 = 2
dir3 = 7
dir4 = 10



def stop():
    uno.digitalWrite(motor1PWM, 0)
    uno.digitalWrite(motor2PWM, 0)
    uno.digitalWrite(motor3PWM, 0)
    uno.digitalWrite(motor4PWM, 0)


def forward():
    uno.digitalWrite(dir1, high)
    uno.digitalWrite(dir3, high)
    uno.digitalWrite(dir2, low)
    uno.digitalWrite(dir4, low)


def left():
    uno.digitalWrite(dir1, low)
    uno.digitalWrite(dir3, high)
    uno.digitalWrite(dir2, high)
    uno.digitalWrite(dir4, low)


def right():
    uno.digitalWrite(dir1, high)
    uno.digitalWrite(dir3, low)
    uno.digitalWrite(dir2, low)
    uno.digitalWrite(dir4, high)


def reverse():
    uno.digitalWrite(dir1, low)
    uno.digitalWrite(dir3, low)
    uno.digitalWrite(dir2, high)
    uno.digitalWrite(dir4, high)


def setspeed(speed):
    if (speed >= 0) & (speed <= 255):
        uno.analogWrite(motor1PWM, speed)
        uno.analogWrite(motor2PWM, speed)
        uno.analogWrite(motor3PWM, speed)
        uno.analogWrite(motor4PWM, speed)
    else:
        print("Bad speed value")


def smoothleft(speedleft, speedright):
    uno.analogWrite(motor1PWM, speedleft)
    uno.analogWrite(motor2PWM, speedleft)
    uno.analogWrite(motor3PWM,speedright)
    uno.analogWrite(motor4PWM, speedright)
    forward()


def smoothright(speedleft, speedright):
    uno.analogWrite(motor1PWM, speedleft)
    uno.analogWrite(motor2PWM, speedleft)
    uno.analogWrite(motor3PWM,speedright)
    uno.analogWrite(motor4PWM, speedright)
    forward()

while message != "END":
    message = input('Please enter a direction: ')
    if message == "END":
        stop()
        setspeed(0)
    else:
        if message == "left":
            left()
        else:
            if message == "right":
                right()
            else:
                if message == "forward":
                    forward()
                else:
                    if message == "reverse":
                        reverse()
                    else:
                        if message == "smoothleft":
                            givenleftspeed = int(input("Enter left speed: "))
                            givenrightspeed = int(input("Enter right speed: "))
                            smoothleft(givenleftspeed, givenrightspeed)
                        else:
                            if message == "smoothright":
                                givenleftspeed = int(input("Enter left speed: "))
                                givenrightspeed = int(input("Enter right speed: "))
                                smoothright(givenleftspeed, givenrightspeed)
                            else:
                                stop()
        if (message != "END") & (message != "smoothleft") & (message != "smoothright"):
            givenspeed = int(input('Please enter a speed: '))
            setspeed(givenspeed)



