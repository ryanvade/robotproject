__author__ = 'ryanvade'
os.environ["SDL_VIDEODRIVER"] = "dummy" # don't ask
# Program to be run on the raspberry pi
import os
import sys
import curses
import pygame
import array
import time
from time import sleep


# is this an Arm system (raspberry pi)
if not os.uname()[4].startswith("arm"):
    sys.stdout.write("Cannot run on: ")
    print(os.uname()[4])
    sys.exit(1)

# Is the RPi module available?
try:
    import RPi.GPIO as GPIO
except ImportError as e:
    print(e)
    sys.exit(1)
# Is the nanpy module available?
try:
    import nanpy
    from nanpy import (Arduino, OneWire, Lcd, SerialManager, ArduinoApi, Stepper, Servo)
except ImportError as e:
    print(e)
    sys.exit(1)

# variables
tty = "/dev/ttyAMA0"
connectionName = SerialManager(device=tty)
mega = ArduinoApi(connection=connectionName)
low = mega.LOW
high = mega.HIGH
message = " "
screen = curses.initscr()
defaultspeed = 127
currentspeed = defaultspeed
veercorrection = 39
decreasespeedvalue = 5
increasespeedvalue = 5

motor1PWM = 46
motor3PWM = 44
motor2PWM = 9
motor4PWM = 3

sonar1Trig = 6
sonar1Echo = 5

dir1 = 7
dir2 = 2
dir3 = 8
dir4 = 10

interuptLeft = 51
interuptRight = 53

# Xbone controller info
lTrigger = 2  # from 0 to 1
rTrigger = 5  # from 0 to 1
aButton = 0  # 0 false, 1 true
bButton = 1
xButton = 2
yButton = 3

hatLeft = (-1, 0)# hat is dpad
hatRight = (1, 0)
hatUp = (0, 1)
hatDown = (0, -1)
hatDefault = (0, 0)

def stop():
    mega.digitalWrite(motor1PWM, 0)
    mega.digitalWrite(motor2PWM, 0)
    mega.digitalWrite(motor3PWM, 0)
    mega.digitalWrite(motor4PWM, 0)


def forward():
    mega.digitalWrite(dir1, high)
    mega.digitalWrite(dir3, high)
    mega.digitalWrite(dir2, low)
    mega.digitalWrite(dir4, low)


def left():
    mega.digitalWrite(dir1, low)
    mega.digitalWrite(dir3, high)
    mega.digitalWrite(dir2, high)
    mega.digitalWrite(dir4, low)


def right():
    mega.digitalWrite(dir1, high)
    mega.digitalWrite(dir3, low)
    mega.digitalWrite(dir2, low)
    mega.digitalWrite(dir4, high)


def reverse():
    mega.digitalWrite(dir1, low)
    mega.digitalWrite(dir3, low)
    mega.digitalWrite(dir2, high)
    mega.digitalWrite(dir4, high)


def setspeed(speed):
    if (speed >= 0) & (speed <= 255):
        mega.analogWrite(motor1PWM, speed - veercorrection)
        mega.analogWrite(motor2PWM, speed - veercorrection)
        mega.analogWrite(motor3PWM, speed)
        mega.analogWrite(motor4PWM, speed)
    else:
        print("Bad speed value")


def setleftspeed(speed):
    if (speed >= 0) & (speed <= 255):
        mega.analogWrite(motor1PWM, speed)
        mega.analogWrite(motor2PWM, speed)
    else:
        print("Bad speed value")


def smoothleft(speedleft, speedright):
    mega.analogWrite(motor1PWM, speedleft)
    mega.analogWrite(motor2PWM, speedleft)
    mega.analogWrite(motor3PWM, speedright)
    mega.analogWrite(motor4PWM, speedright)
    forward()


def smoothright(speedleft, speedright):
    mega.analogWrite(motor1PWM, speedleft)
    mega.analogWrite(motor2PWM, speedleft)
    mega.analogWrite(motor3PWM, speedright)
    mega.analogWrite(motor4PWM, speedright)
    forward()

# Initialize the joysticks
pygame.joystick.init()
#joystick_count = pygame.joystick.get_count()

done = False

joystick_count = pygame.joystick.get_count()
for i in range(joystick_count):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
name = joystick.get_name()
print(name)

while done == False:
    for event in pygame.event.get():  # User did something
        buttons = joystick.get_numbuttons()
        bA = joystick.get_button(aButton)
        bB = joystick.get_button(bButton)
        if bA == 1:
            print("A button pressed: Exiting")
            stop()
            done = True
        if bB == 1:
            print("B Button pressed: stopping")
            stop()

        hats = joystick.get_numhats()
        axes = joystick.get_numaxes()

        #lTriggerValue = (joystick.get_axis(lTrigger) + 1.0) / 2.0

        for i in range( hats ):
            dpadValue = joystick.get_hat( i )
            #print(dpadValue)
            if dpadValue == hatLeft:
                left()
                print("Left")
            elif dpadValue == hatRight:
                right()
                print("Right")
            elif dpadValue == hatUp:
                forward()
                print("Up")
            elif dpadValue == hatDown:
                reverse()
                print("Reverse")
            elif dpadValue == hatDefault:
                print("Default")
    rTriggerValue = 255 * ((joystick.get_axis(rTrigger) + 1.0) / 2.0)
    setspeed(rTriggerValue)

pygame.joystick.quit()
pygame.quit()