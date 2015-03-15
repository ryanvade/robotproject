__author__ = 'ryanvade'
# Program to be run on the raspberry pi
import os, sys, Base, pygame
os.environ["SDL_VIDEODRIVER"] = "dummy" # don't ask

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
# Is the nanpy module available?
try:
    import nanpy
    from nanpy import (Arduino, OneWire, Lcd, SerialManager, ArduinoApi, Stepper, Servo)
except ImportError as e:
    print(e)
    sys.exit(1)

class Controller:
    # Xbone controller info
    lTrigger = 2  # from 0 to 1
    rTrigger = 5  # from 0 to 1
    aButton = 0  # 0 false, 1 true
    bButton = 1
    xButton = 2
    yButton = 3

    hatLeft = (-1, 0)# hat is dpad
    hatRight = (1, 0)
    hatUp = (0, 1)
    hatDown = (0, -1)
    hatDefault = (0, 0)

    def __init__(self, base):
        self.base = base

        # Initialize the joysticks
        pygame.init()
        pygame.display.set_mode((1, 1)) # seriously, don't ask
        pygame.joystick.init()
        self.joystick_count = pygame.joystick.get_count()

        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count):
            self.joystick = pygame.joystick.Joystick(i)
            self.joystick.init()
        name = self.joystick.get_name()
        print(name)
        triggervalue = ((self.joystick.get_axis(self.rTrigger) + 1.0) / 2.0)
        while (triggervalue < 0) or (triggervalue > 1):
            print("Controller Not ready!")
            triggervalue = ((self.joystick.get_axis(self.rTrigger) + 1.0) / 2.0)

    def runWithController(self):
        done = False
        while not done:
            for event in pygame.event.get():  # User did something
                buttons = self.joystick.get_numbuttons()
                bA = self.joystick.get_button(self.aButton)
                bB = self.joystick.get_button(self.bButton)
                if bA == 1:
                    print("A button pressed: Exiting")
                    self.base.stop()
                    done = True
                if bB == 1:
                    print("B Button pressed: stopping")
                    self.base.stop()

                hats = self.joystick.get_numhats()
                axes = self.joystick.get_numaxes()

                #lTriggerValue = (joystick.get_axis(lTrigger) + 1.0) / 2.0

                for i in range( hats ):
                    dpadValue = self.joystick.get_hat( i )
                    #print(dpadValue)
                    if dpadValue == self.hatLeft:
                        self.base.left()
                        print("Left")
                    elif dpadValue == self.hatRight:
                        self.base.right()
                        print("Right")
                    elif dpadValue == self.hatUp:
                        self.base.forward()
                        print("Up")
                    elif dpadValue == self.hatDown:
                        self.base.reverse()
                        print("Reverse")
                    elif dpadValue == self.hatDefault:
                        print("Default")
            rTriggerValue = int(255 * ((self.joystick.get_axis(self.rTrigger) + 1.0) / 2.0))
            self.base.setspeed(rTriggerValue)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pygame.joystick.quit()
        pygame.quit()
        self.Controller_obj.cleanup()