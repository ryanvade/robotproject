__author__ = 'ryanvade'

import sys
import time
from time import sleep

import serial



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

tty = "/dev/ttyAMA0"
connectionName = SerialManager(device=tty)
mega = ArduinoApi(connection=connectionName)
encoder_read = serial.Serial(tty, 115200)
low = mega.LOW
high = mega.HIGH
message = " "
#screen = curses.initscr()
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
    print("forward")
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
    print(speed)
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


#print("Define sonar")


def sonar(trigPin, echoPin):
    mega.digitalWrite(trigPin, high)
    sleep(0.000002)
    mega.digitalWrite(trigPin, low)
    mega.digitalWrite(trigPin, high)
    sleep(0.00001)
    mega.digitalWrite(trigPin, low)
    duration = pulsein(echoPin)
    centimeters = duration / 29.0 / 2.0
    return centimeters


#print("Define pulsein")


def pulsein(echoPin):
    startTime = time.time()
    currentTime = 0.0
    while mega.digitalRead(echoPin) == high:
        currentTime = time.time()

    pulseTime = currentTime - startTime
    return pulseTime


#print("Done defines")
#distance = sonar(sonar1Trig, sonar1Echo)
#print(distance)

GPIO.wait_for_edge(5, GPIO.RISING)
forward()
setspeed(currentspeed)
time.sleep(5)
stop()
print(encoder_read.read(8))

#curses.endwin()
#stop()

