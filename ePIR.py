__author__ = 'ryanvade'
from nanpy import SerialManager


class _EPIR:
    def __init__(self, tx, rx, port):
        ack = '6'
        nack = '12'
        port.serial.readChar()