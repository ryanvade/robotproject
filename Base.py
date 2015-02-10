__author__ = 'ryanvade'
import sys, time
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


defaultspeed = 127
currentspeed = defaultspeed
veercorrection = 39
decreasespeedvalue = 5
increasespeedvalue = 5

class Base:
    def __init__(self, arduino, motor1PWM, motor2PWM, motor3PWM, motor4PWM, dir1, dir2, dir3, dir4):
        self.mega = arduino
        self.motor1PWM = motor1PWM
        self.motor2PWM = motor2PWM
        self.motor3PWM = motor3PWM
        self.motor4PWM = motor4PWM
        self.dir1 = dir1
        self.dir2 = dir2
        self.dir3 = dir3
        self.dir4 = dir4
        high = self.mega.HIGH
        low = self.mega.LOW

    def stop(self):
        self.mega.digitalWrite(self.motor1PWM, 0)
        self.mega.digitalWrite(self.motor2PWM, 0)
        self.mega.digitalWrite(self.motor3PWM, 0)
        self.mega.digitalWrite(self.motor4PWM, 0)


    def forward(self):
        self.mega.digitalWrite(self.dir1, self.high)
        self.mega.digitalWrite(self.dir3, self.high)
        self.mega.digitalWrite(self.dir2, self.low)
        self.mega.digitalWrite(self.dir4, self.low)


    def left(self):
        self.mega.digitalWrite(self.dir1, self.low)
        self.mega.digitalWrite(self.dir3, self.high)
        self.mega.digitalWrite(self.dir2, self.high)
        self.mega.digitalWrite(self.dir4, self.low)


    def right(self):
        self.mega.digitalWrite(self.dir1, self.high)
        self.mega.digitalWrite(self.dir3, self.low)
        self.mega.digitalWrite(self.dir2, self.low)
        self.mega.digitalWrite(self.dir4, self.high)


    def reverse(self):
        self.mega.digitalWrite(self.dir1, self.low)
        self.mega.digitalWrite(self.dir3, self.low)
        self.mega.digitalWrite(self.dir2, self.high)
        self.mega.digitalWrite(self.dir4, self.high)


    def setspeed(self, speed):
        if (speed >= 0) & (speed <= 255):
            self.mega.analogWrite(self.motor1PWM, speed - veercorrection)
            self.mega.analogWrite(self.motor2PWM, speed - veercorrection)
            self.mega.analogWrite(self.motor3PWM, speed)
            self.mega.analogWrite(self.motor4PWM, speed)
        else:
            print("Bad speed value")


    def setleftspeed(self, speed):
        if (speed >= 0) & (speed <= 255):
            self.mega.analogWrite(self.motor1PWM, speed)
            self.mega.analogWrite(self.motor2PWM, speed)
        else:
            print("Bad speed value")


    def smoothleft(self, speedleft, speedright):
        self.mega.analogWrite(self.motor1PWM, speedleft)
        self.mega.analogWrite(self.motor2PWM, speedleft)
        self.mega.analogWrite(self.motor3PWM, speedright)
        self.mega.analogWrite(self.motor4PWM, speedright)
        self.forward()


    def smoothright(self, speedleft, speedright):
        self.mega.analogWrite(self.motor1PWM, speedleft)
        self.mega.analogWrite(self.motor2PWM, speedleft)
        self.mega.analogWrite(self.motor3PWM, speedright)
        self.mega.analogWrite(self.motor4PWM, speedright)
        self.forward()


    def sonar(self, trigPin, echoPin):
        self.mega.digitalWrite(trigPin, self.high)
        self.sleep(0.000002)
        self.mega.digitalWrite(trigPin, self.low)
        self.mega.digitalWrite(trigPin, self.high)
        time.sleep(0.00001)
        self.mega.digitalWrite(trigPin, self.low)
        duration = self.pulsein(echoPin)
        centimeters = duration / 29.0 / 2.0
        return centimeters


    def pulsein(self, echoPin):
        startTime = time.time()
        currentTime = 0.0
        while self.mega.digitalRead(echoPin) == self.high:
            currentTime = time.time()

        pulseTime = currentTime - startTime
        return pulseTime