__author__ = 'ryanvade'

import sys
import serial

try:
    import RPi.GPIO as GPIO
except ImportError as e:
    print(e)
    sys.exit(1)

class serialManager:
    global expecting_response
    global expecting_acknowledge
    global character_code_list
    global paramater_list
    global response_list
    global connection
    constant_communication = False

    def __init__(self, port="/dev/ttyACM0", baud_rate=19200):
        self.port = port
        self.baud_rate = baud_rate
        self.expecting_response = False
        self.expecting_acknowledge = False
        self.connection = None

        try:
            self.connection = serial.Serial(port, baud_rate, timeout=1)
        except serial.SerialException as e:
            print(e)
            return None

        self.character_code_list = []
        self.paramater_list = []
        self.response_list = []

        if(not self.connection.isOpen()):
            print("No serial connection")
            #TODO what to do if no connection is created
            sys.exit(1)
        else:
            print("Connection Established on:" +  port)

        return self

    def send_command(self, character_code, paramater1 = None, paramater2 = None):

        try:
            self.connection.write(character_code)
            self.character_code_list.append(str(character_code))
        except serial.SerialTimeoutException as e:
            print(e)
            return 1

        if(not paramater1 == None):
            try:
                self.connection.write(paramater1)
                self.paramater_list.append(str(paramater1))
            except serial.SerialTimeoutException as e:
                print(e)
                return 1

        if(not paramater2 == None):
            try:
                self.connection.write(paramater2)
                self.paramater_list.append(str(paramater2))
            except serial.SerialTimeoutException as e:
                print(e)
                return 1
        self.expecting_acknowledge = True
        return 0

    def receive_full_buffer(self):
        try:
            self.expecting_response = False
            return self.connection.read(self.conection.inWaiting()) #return the full buffer
        except serial.SerialException as e:
            print(e)
            return 0

    def receive_byte_buffer(self,size=1):#where size is the number of bytes
        try:
            self.expecting_response = False
            return self.connection.read(size)
        except serial.SerialException as e:
            print(e)
            return 0

    def recive_full_line_buffer(self, size=None, eol='\n'): #where size is the max number of bytes
        try:
            self.expecting_response = False
            return self.connection.readline(size, eol)
        except serial.SerialException as e:
            print(e)
            return 0

    def start_constant_communication(self):
        #TODO process for constant listening
        self.constant_communication = True

    def get_response(self, type="Byte", size=1, eol='\n'):
        if type == "full":
            response = self.receive_full_buffer()
        elif type == "line":
            response = self.recive_full_line_buffer(size, eol)
        else:
            response = self.receive_byte_buffer(size)
        self.response_list.append(response)
        self.expecting_response = False
        return response

    def receive_acknowledge(self):
            self.expecting_acknowldege = False
            ack = self.receive_full_buffer()
            self.response_list.append(ack)
            return ack

    def get_last_response(self):
        return self.response_list[-1]

    def get_last_character_code(self):
        return self.character_code_list[-1]

    def get_last_paramater(self):
        return self.paramater_list[-1]

    def close_connection(self):
        self.connection.close()