__author__ = 'ryanvade'

import sys
import time

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

sonar1Trig = 14
sonar1Echo = 16
mega.pinMode(sonar1Trig, mega.OUTPUT)
mega.digitalWrite(14, low)
mega.pinMode(sonar1Echo, mega.INPUT)
print("Define sonar")
time.sleep(0.03)
pulseLength = 0.00001
lowLength = 0.000002

def sonar(trigPin, echoPin):
    mega.digitalWrite(trigPin, low) # to be sure we are not transmitting
    time.sleep(lowLength) # for a low output, 2 microseconds from http://arduinobasics.blogspot.com/2012/11/arduinobasics-hc-sr04-ultrasonic-sensor.html
    mega.digitalWrite(trigPin, high)
    time.sleep(pulseLength) # high output for 10 microseconds
    mega.digitalWrite(trigPin, low)
    duration = pulsein(echoPin)
    print(duration)
    centimeters = duration * 17000 #IS this correct? or should it be / 58.2
    return centimeters


def pulsein(echoPin):
    offTime = 0.0
    onTime = 0.0
    iteration = 0
    while (mega.digitalRead(echoPin) != high) and (iteration < 500):
        offTime = time.clock()
        iteration += 1
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

