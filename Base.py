__author__ = 'ryanvade'
import sys
import BaseSerial

# Is the RPi module available?
# try:
#     import RPi.GPIO as GPIO
# except ImportError as e:
#     print(e)
#     sys.exit(1)

class Base:
    maxspeed = 255
    minspeed = 0
    defaultspeed = 127
    currentspeed = 0
    veercorrection = 39
    decreasespeedvalue = 5
    increasespeedvalue = 5
    serialManager = None
    rcar = '\r'.encode()


    def __init__(self, motor1PWM, motor2PWM, motor3PWM, motor4PWM, dir1, dir2, dir3, dir4):
        self.motor1PWM = motor1PWM
        self.motor2PWM = motor2PWM
        self.motor3PWM = motor3PWM
        self.motor4PWM = motor4PWM
        self.dir1 = dir1
        self.dir2 = dir2
        self.dir3 = dir3
        self.dir4 = dir4
        self.serialManager = BaseSerial.serialManager

    def stop(self):
        self.serialManager.send_command('h', self.rcar)
        stop_ack = self.serialManager.receive_acknowledge()
        return stop_ack



    def forward(self, speed):
        self.serialManager.send_command('df', speed, self.rcar)
        drive_ack = self.serialManager.receive_acknowledge()
        return drive_ack


    def left(self, speed):
        self.serialManager.send_command('tl', speed, self.rcar)
        left_ack = self.serialManager.receive_acknowledge()
        return left_ack

    def right(self, speed):
        self.serialManager.send_command('tr', speed, self.rcar)
        right_ack = self.serialManager.receive_acknowledge()
        return right_ack


    def reverse(self, speed):
        self.serialManager.send_command('db', speed, self.rcar)
        reverse_ack = self.serialManager.receive_acknowledge()
        return reverse_ack

    def close(self):
        self.serialManager.close_connection()