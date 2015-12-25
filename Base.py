__author__ = 'ryanvade'
import serialCommunication


# Is the RPi module available?
# try:
#     import RPi.GPIO as GPIO
# except ImportError as e:
#     print(e)
#     sys.exit(1)


class Base:
    __max_speed = 255
    __min__speed = 0
    __default_speed = 127
    __current__speed = 0
    __veer__correction = 39
    __decrease_speed_value = 5
    __increase_speed_value = 5
    __serial_connection = None

    def __init__(self, port="/dev/ttyACM0", baud_rate=19200):
        self.__serial_connection = serialCommunication.BaseSerial(port, baud_rate)

    def stop(self):
        self.__serial_connection.send_command('h', '\r')

    def drive_forward(self, speed):
        if self.__min__speed <= speed <= self.__max_speed:
            self.__serial_connection.send_command('df', speed, '\r')

    def turn_left(self, speed):
        if self.__min__speed <= speed <= self.__max_speed:
            self.__serial_connection.send_command('tl', speed, '\r')

    def turn_right(self, speed):
        if self.__min__speed <= speed <= self.__max_speed:
            self.__serial_connection.send_command('tr', speed, '\r')

    def drive_reverse(self, speed):
        if self.__min__speed <= speed <= self.__max_speed:
            self.__serial_connection.send_command('db', speed, '\r')

    def get_ping_distance(self):
        self.__serial_connection.send_command('p', '\r')
        response_ack = self.__serial_connection.get_response()
        return response_ack

    def close(self):
        self.__serial_connection.close_connection()

    def connection_information(self):
        return self.__serial_connection.get_connection_info()

    def get_last_response_from_serial(self):
        return self.__serial_connection.get_response()

    def get_ping_distance(self):
        # self.__serial_connection.flush()
        self.__serial_connection.send_command('p', '\r')
        return self.__serial_connection.get_response()
