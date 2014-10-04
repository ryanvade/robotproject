import serial
import time

port = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=3.0)
data = bytearray([1])
while(True):
	port.write(data[0])
	time.sleep(2)
	port.flush()


