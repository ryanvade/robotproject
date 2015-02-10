__author__ = 'ryanvade'
import sys
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

class Base:
    def __init__(self, arduino, motor1PWM, motor2PWM, motor3PWM, motor4PWM, dir1, dir2, dir3, dir4, ):
        self.mega = arduino
        self.motor1PWM = motor1PWM
        self.motor2PWM = motor2PWM
        self.motor3PWM = motor3PWM
        self.motor4PWM = motor4PWM
        self.dir1 = dir1
        self.dir2 = dir2
        self.dir3 = dir3
        self.dir4 = dir4
        high = mega.HIGH
        low = mega.LOW
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
        mega.digitalWrite(trigPin, high)
        sleep(0.000002)
        mega.digitalWrite(trigPin, low)
        mega.digitalWrite(trigPin, high)
        sleep(0.00001)
        mega.digitalWrite(trigPin, low)
        duration = pulsein(echoPin)
        centimeters = duration / 29.0 / 2.0
        return centimeters


    def pulsein(echoPin):
        startTime = time.time()
        currentTime = 0.0
        while mega.digitalRead(echoPin) == high:
            currentTime = time.time()

        pulseTime = currentTime - startTime
        return pulseTime