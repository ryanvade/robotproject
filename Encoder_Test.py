__author__ = 'ryanvade'

import sys
import time
from time import sleep

import serial



# Is the RPi module available?

try:
    import nanpy
    from nanpy import (Arduino, OneWire, Lcd, SerialManager, ArduinoApi, Stepper, Servo)
except ImportError as e:
    print(e)
    sys.exit(1)

tty = "/dev/ttyACM0"
connectionName = SerialManager(device=tty)
mega = ArduinoApi(connection=connectionName)
#encoder_read = serial.Serial(tty, 115200)
low = mega.LOW
high = mega.HIGH


motor1PWM = 46
motor3PWM = 44
motor2PWM = 9
motor4PWM = 3


sonar1Trig = 14
sonar1Echo = 16
mega.pinMode(sonar1Trig, mega.OUTPUT)
mega.digitalWrite(14, low)
mega.pinMode(sonar1Echo, mega.INPUT)
print("Define sonar")
time.sleep(0.03)

def sonar(trigPin, echoPin):
    print("Sleep one")
    mega.digitalWrite(trigPin, low)
    mega.digitalWrite(trigPin, high)
    time.sleep(0.0001)
    print("Sleep two")
    mega.digitalWrite(trigPin, low)
    duration = pulsein(echoPin)
    print(duration)
    centimeters = duration *17000
    return centimeters


#print("Define pulsein")


def pulsein(echoPin):
    offTime = 0.0
    onTime = 0.0
    iteration = 0
    while  (mega.digitalRead(echoPin) != high) and (iteration < 500):
        offTime = time.clock()
        iteration = iteration +1
    while mega.digitalRead(echoPin) == high:
        onTime = time.clock()
    if(onTime == 0.0):
        return onTime
    pulseTime = onTime - offTime
    return pulseTime


print("Done defines")

while True:
    distance = sonar(sonar1Trig, sonar1Echo)
    print(distance)
    print("\n")

connectionName.close()

#GPIO.wait_for_edge(5, GPIO.RISING)
#print(encoder_read.read(8))

#curses.endwin()
#stop()

