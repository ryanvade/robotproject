__author__ = 'ryanvade'

import sys
import serial
import time
import threading


# try:
#     import RPi.GPIO as GPIO
# except ImportError as e:
#     print(e)
#     sys.exit(1)


class BaseSerial:
    constant_communication = False

    def __init__(self, port, baud_rate):
        self.__port = port
        self.__baud_rate = baud_rate
        self.__expecting_response = False
        self.__expecting_acknowledge = False
        self.__wait_time_in_seconds = 3

        try:
            self.__connection = serial.Serial(port, baud_rate, timeout=1)
        except serial.SerialException as e:
            print(e)
            exit(1)

        self.__character_code_list = []
        self.__parameter_list = []
        self.__response_list = []

        if not self.__connection.isOpen():
            print("No serial self.connection")
            # TODO what to do if no self.connection is created
            sys.exit(1)
        else:
            self.flush()
            print("Connection Established on:" + self.__port + " At " + str(self.__baud_rate))

    def send_command(self, character_code, parameter1=None, parameter2=None):
        # TODO put send code in seperate thread
        try:
            self.__connection.write(str(character_code).encode())
            # self.character_code_list.append(str(character_code))
        except serial.SerialTimeoutException as e:
            print(e)

        if parameter1 is not None:
            try:
                self.__connection.write(str(parameter1).encode())
                self.__parameter_list.append(str(parameter1))
            except serial.SerialTimeoutException as e:
                print(e)
                return 1

        if parameter2 is not None:
            try:
                self.__connection.write(str(parameter2).encode())
                self.__parameter_list.append(str(parameter2))
            except serial.SerialTimeoutException as e:
                print(e)
        self.__expecting_acknowledge = True
        time.sleep(self.__wait_time_in_seconds)

    def start_constant_communication(self):
        # TODO process for constant listening on separate thread
        self.constant_communication = True

    def get_response(self):
        # TODO make a private get response thread to update the queue
        # get_response should then pop the last item on the queue
        # TODO should the __expecting_reponse always be true to receive a respons?
        while self.__connection.inWaiting() == 0 and self.__expecting_response:
            print("Waiting for response")
        response = self.__connection.read(self.__connection.inWaiting())
        self.__response_list.append(response)
        self.__expecting_response = False
        self.__expecting_acknowledge = False
        return str(response)

    # TODO get_last methods should be replaced
    def get_last_response(self):
        return self.__response_list[-1]

    def get_last_character_code(self):
        return self.__character_code_list[-1]

    def get_last_parameter(self):
        return self.__parameter_list[-1]

    # TODO implement try/catch and finally clause
    def close_connection(self):
        print("Closing Port")
        self.flush()
        self.__connection.close()

    def flush(self):
        self.__connection.flushInput()
        self.__connection.flushOutput()
        self.__connection.flush()

    def get_connection_info(self):
        return self.__connection.getByteSize
