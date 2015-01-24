__author__ = 'ryanvade'
# Program to be run on the raspberry pi
import os
import sys
import curses
from time import sleep
import time

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

#variables
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

print("Hello")

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


def sonar(trigPin, echoPin):
    mega.digitalWrite(trigPin, mega.HIGH)
    sleep(0.000002)
    mega.digitalWrite(trigPin, mega.LOW)
    mega.digitalWrite(trigPin, mega.HIGH)
    sleep(0.00001)
    mega.digitalWrite(trigPin, mega.LOW)
    duration = pulsein(echoPin)
    centimeters = duration / 29 / 2
    return centimeters


def pulsein(echoPin):
    startTime = time.time()
    currentTime = 0
    while mega.digitalRead(echoPin):
        currentTime = time.time()

    pulseTime = currentTime - startTime
    return pulseTime

stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)

stdscr.addstr(0, 10, "Hit 'q' to quit")
stdscr.refresh()

key = ''
distance = sonar(sonar1Trig, sonar1Echo)
while (key != ord('q')) and (distance > 18.0):
    key = stdscr.getch()
    stdscr.addch(20, 25, key)
    stdscr.refresh()
    setspeed(currentspeed)

    if key == curses.KEY_UP:
        stdscr.addstr(2, 20, "Up")
        forward()
    elif key == curses.KEY_DOWN:
        stdscr.addstr(3, 20, "Down")
        reverse()
    elif key == curses.KEY_LEFT:
        stdscr.addstr(4, 20, "LEFT")
        left()
    elif key == curses.KEY_RIGHT:
        stdscr.addstr(5, 20, "RIGHT")
        right()
    elif key == curses.KEY_NPAGE:
        stdscr.addstr(6, 20, "Next Page")
        currentspeed += increasespeedvalue
        setspeed(currentspeed)
    elif key == curses.KEY_PPAGE:
        stdscr.addstr(7, 20, "PREVIOUS Page")
        currentspeed -= decreasespeedvalue
        setspeed(currentspeed)
    elif key == ord("s"):
        stdscr.addstr(8, 20, "s")
        stop()
    distance = sonar(sonar1Trig, sonar1Echo)

curses.endwin()
stop()


