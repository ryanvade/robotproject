__author__ = 'ryanvade'
import pygame
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
pygame.init()

# Initialize the joysticks
pygame.joystick.init()
#joystick_count = pygame.joystick.get_count()

done = False

joystick_count = pygame.joystick.get_count()
for i in range(joystick_count):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
name = joystick.get_name()
print(name)

while done == False:
    for event in pygame.event.get():  # User did something
        buttons = joystick.get_numbuttons()
        bA = joystick.get_button(aButton)
        bB = joystick.get_button(bButton)
        if bA == 1:
            print("A button pressed: Exiting")
            done = True
        if bB == 1:
            print("B Button pressed: stopping")
            # stop
            break

        hats = joystick.get_numhats()
        axes = joystick.get_numaxes()

        rTriggerValue = (joystick.get_axis(rTrigger) + 1.0) / 2.0
        #lTriggerValue = (joystick.get_axis(lTrigger) + 1.0) / 2.0

        for i in range( hats ):
            dpadValue = joystick.get_hat( i )
            #print(dpadValue)
            if dpadValue == hatLeft:
                #left()
                print("Left")
            elif dpadValue == hatRight:
                #right()
                print("Right")
            elif dpadValue == hatUp:
                #forward()
                print("Up")
            elif dpadValue == hatDown:
                #reverse()
                print("Reverse")
            elif dpadValue == hatDefault:
                print("Default")

pygame.joystick.quit()
pygame.quit()