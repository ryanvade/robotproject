__author__ = 'ryanvade'
import sys
import BaseSerial

# Is the RPi module available?
try:
    import RPi.GPIO as GPIO
except ImportError as e:
    print(e)
    sys.exit(1)
# Is the nanpy module available?
try:
    from nanpy import (Arduino, OneWire, Lcd, SerialManager, ArduinoApi, Stepper, Servo)
except ImportError as e:
    print(e)
    sys.exit(1)


class Base:
    maxspeed = 255
    minspeed = 0
    defaultspeed = 127
    currentspeed = 0
    veercorrection = 39
    decreasespeedvalue = 5
    increasespeedvalue = 5
    serial = None


    def __init__(self, motor1PWM, motor2PWM, motor3PWM, motor4PWM, dir1, dir2, dir3, dir4):
        self.motor1PWM = motor1PWM
        self.motor2PWM = motor2PWM
        self.motor3PWM = motor3PWM
        self.motor4PWM = motor4PWM
        self.dir1 = dir1
        self.dir2 = dir2
        self.dir3 = dir3
        self.dir4 = dir4
        self.serial = BaseSerial.serialManager()

    def stop(self):
        self.serial.send_command()
        stop_ack = self.serial.receive_acknowledge()
        print(stop_ack)



    def forward(self):
        self.serial.send_command()
        drive_ack = self.serial.receive_acknowledge()
        print(drive_ack)


    def left(self):
        self.serial.send_command()
        left_ack = self.serial.receive_acknowledge()
        print(left_ack)

    def right(self):
        self.serial.send_command()
        right_ack = self.serial.receive_acknowledge()
        print(right_ack)


    def reverse(self):
        self.serial.send_command()
        reverse_ack = self.serial.receive_acknowledge()
        print(reverse_ack)