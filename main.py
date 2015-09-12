__author__ = 'ryanvade'
# Program to be run on the raspberry pi
import os
import sys
import curses
import time
import array

import Base


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

# variables
tty = "/dev/ttyAMA0"
baud_rate = 19200
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

base = Base.Base(motor1PWM, motor2PWM, motor3PWM, motor4PWM, dir1, dir3, dir3, dir4)

#lTrigger = 2  # from 0 to 1
#rTrigger = 5  # from 0 to 1
#lStick = array.array[0, 1]  # x direction -1 -> 1 , y direction -1 -> 1
#rStick = array.array[3, 4]  # x direction -1 -> 1, y direction -1 -> 1


stdscr = curses.initscr()
# curses.cbreak()
stdscr.keypad(1)
stdscr.addstr(0, 10, "Hit 'q' to quit")
stdscr.refresh()

key = ''

while (key != ord('q')): #and (distance > 18.0):
    key = stdscr.getch()
    stdscr.addch(20, 25, key)
    stdscr.refresh()
    #base.setspeed(currentspeed)

    if key == curses.KEY_UP:
        stdscr.addstr(2, 20, "Up")
        fack = base.forward(10)
        stdscr.addstr(2, 25, fack)
    elif key == curses.KEY_DOWN:
        stdscr.addstr(3, 20, "Down")
        back = base.reverse(10)
        stdscr.addstr(3, 25, rack)
    elif key == curses.KEY_LEFT:
        stdscr.addstr(4, 20, "LEFT")
        lack = base.left(10)
        stdscr.addstr(4, 25, lack)
    elif key == curses.KEY_RIGHT:
        stdscr.addstr(5, 20, "RIGHT")
        rack  = base.right(10)
        stdscr.addstr(5, 25, rack)
    elif key == curses.KEY_NPAGE:
        stdscr.addstr(6, 20, "Next Page")
        currentspeed += increasespeedvalue
        #base.setspeed(currentspeed)
    elif key == curses.KEY_PPAGE:
        stdscr.addstr(7, 20, "PREVIOUS Page")
        currentspeed -= decreasespeedvalue
        #base.setspeed(currentspeed)
    elif key == ord("s"):
        stdscr.addstr(8, 20, "s")
        sack = base.stop()
        stdscr.addstr(8, 25, sack)
    #distance = base.sonar(sonar1Trig, sonar1Echo)

time.sleep(5)
curses.endwin()
base.stop()
base.close()


