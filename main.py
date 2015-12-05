__author__ = 'ryanvade'
import os
import sys
import time
import Base

__debugging__ = True
if not __debugging__:
    # is this an Arm system (raspberry pi)
    if not os.uname()[4].startswith("arm"):
        sys.stdout.write("Cannot run on: ")
        print(os.uname()[4])
        sys.exit(1)
    # Is the RPi module available?
    try:
        import RPi.GPIO as GPIO
    except ImportError as e:
        print(e)
        sys.exit(1)

# variables
tty = "/dev/ttyAMA0"
baud_rate = 19200
waitTime = 5  # seconds
control = Base.Base(port=tty, baud_rate=baud_rate)
print(control.connection_information())

# control.drive_forward(255)
# time.sleep(waitTime)
#
# print(control.get_last_response_from_serial())
#
# control.stop()
# print(control.get_last_response_from_serial())

for i in range(255):
    print(control.get_ping_distance())
    time.sleep(1)

control.close()
