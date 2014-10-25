__author__ = 'ryanvade'
# Program to be run on the raspberry pi
import serial, time, os, sys, pprint, errno, csv, curses

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
screen = curses.initscr()
defaultspeed = 127
currentspeed = defaultspeed
decreasespeedvalue = 10
increasespeedvalue = 10
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

# while message != "END":
#     message = input('Please enter a direction: ')
#     if message == "END":
#         stop()
#         setspeed(0)
#     elif message == "left":
#         left()
#     elif message == "right":
#         right()
#     elif message == "forward":
#         forward()
#     elif message == "reverse":
#         reverse()
#     elif message == "smoothleft":
#         givenleftspeed = int(input("Enter left speed: "))
#         givenrightspeed = int(input("Enter right speed: "))
#         smoothleft(givenleftspeed, givenrightspeed)
#     elif message == "smoothright":
#         givenleftspeed = int(input("Enter left speed: "))
#         givenrightspeed = int(input("Enter right speed: "))
#         smoothright(givenleftspeed, givenrightspeed)
#     else:
#         stop()
#     if (message != "END") & (message != "smoothleft") & (message != "smoothright"):
#         givenspeed = int(input('Please enter a speed: '))
#         setspeed(givenspeed)
#stop()


stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)

stdscr.addstr(0, 10, "Hit 'q' to quit")
stdscr.refresh()

key = ''
while key != ord('q'):
    key = stdscr.getch()
    stdscr.addch(20,25,key)
    stdscr.refresh()
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
        stdscr.addstr(6 , 20, "Next Page")
        currentspeed = currentspeed + increasespeedvalue
        setspeed(currentspeed)
    elif key == curses.KEY_PPAGE:
        stdscr.addstr(7, 20, "PREVIOUS Page")
        currentspeed = currentspeed - decreasespeedvalue
        setspeed(currentspeed)
    elif key == ord("s"):
        stdscr.addstr(8, 20, "s")
        stop()

curses.endwin()



