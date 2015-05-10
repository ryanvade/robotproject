__author__ = 'ryanvade'
from nanpy.arduinoboard import ArduinoObject
from nanpy.arduinoboard import (arduinoobjectmethod, returns)


class Epir(ArduinoObject):
    def __init__(self, serialport, mdrpin, slppin, connection=None):
        ArduinoObject.__init__(self, connection=connection)
        self.id = self.call('new', serialport, mdrpin, slppin)

    @returns(str)
    @arduinoobjectmethod
    def Status(self):
        pass

    @returns(bytes)
    @arduinoobjectmethod
    def LightLevel(self):
        pass

    @returns(bytes)
    @arduinoobjectmethod
    def GateThresh(self, threshold):
        pass

    @returns(chr(1))
    @arduinoobjectmethod
    def MDRmode(self, mdrMode):
        pass

    @returns(bytes)
    @arduinoobjectmethod
    def MDtime(self, mdTime):
        pass

    @returns(bytes)
    @arduinoobjectmethod
    def TimeLeft(self, timeLeft):
        pass

    @returns(chr(1))
    @arduinoobjectmethod
    def Unsolicited(self, unsolicited):
        pass

    @returns(chr(1))
    @arduinoobjectmethod
    def Extended(self, extended):
        pass

    @returns(chr(1))
    @arduinoobjectmethod
    def Suspend(self, suspend):
        pass

    @returns(bytes)
    @arduinoobjectmethod
    def PulseCount(self, pulseCount):
        pass

    @returns(bytes)
    @arduinoobjectmethod
    def Sensitivity(self, sensitivity):
        pass

    @returns(chr(1))
    @arduinoobjectmethod
    def Direction(self, direction):
        pass

    @arduinoobjectmethod
    def Reset(self):
        pass

    @arduinoobjectmethod
    def Sleep(self):
        pass

    @returns(str)
    @arduinoobjectmethod
    def Version(self):
        pass

