__author__ = 'ryanvade'

import sys
import serial

# try:
#     import RPi.GPIO as GPIO
# except ImportError as e:
#     print(e)
#     sys.exit(1)

class BaseSerial:
    constant_communication = False

    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate
        self.expecting_response = False
        self.expecting_acknowledge = False

        try:
            self.connection = serial.Serial(port, baud_rate, timeout=1)
        except serial.SerialException as e:
            print(e)
            exit(1)

        self.character_code_list = []
        self.paramater_list = []
        self.response_list = []

        if(not self.connection.isOpen()):
            print("No serial self.connection")
            #TODO what to do if no self.connection is created
            sys.exit(1)
        else:
            self.flush()
            print("Connection Established on:" + self.port + " At " + str(self.baud_rate))

    def send_command(self, character_code, paramater1 = None, paramater2 = None):
        try:
            self.connection.write(str(character_code).encode())
            #self.character_code_list.append(str(character_code))
        except serial.SerialTimeoutException as e:
            print(e)

        if(not paramater1 is None):
            try:
                self.connection.write(str(paramater1).encode())
                self.paramater_list.append(str(paramater1))
            except serial.SerialTimeoutException as e:
                print(e)
                return 1

        if(not paramater2 is None):
            try:
                self.connection.write(str(paramater2).encode())
                self.paramater_list.append(str(paramater2))
            except serial.SerialTimeoutException as e:
                print(e)
        self.expecting_acknowledge = True

    def start_constant_communication(self):
        #TODO process for constant listening
        self.constant_communication = True

    def get_response(self,):
        while(self.connection.inWaiting() == 0):
            print("Waiting for response")
        response = self.connection.read(self.connection.inWaiting())
        self.response_list.append(response)
        self.expecting_response = False
        self.expecting_acknowldege = False
        return str(response)

    def get_last_response(self):
        return self.response_list[-1]

    def get_last_character_code(self):
        return self.character_code_list[-1]

    def get_last_paramater(self):
        return self.paramater_list[-1]

    def close_connection(self):
        print("Closing Port")
        self.flush()
        self.connection.close()

    def flush(self):
        self.connection.flushInput()
        self.connection.flushOutput()
        self.connection.flush()