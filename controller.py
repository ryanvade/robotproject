__author__ = 'ryanvade'
import pygame
import os
import sys
import threading
import time

"""
NOTES - pygame events and values derived from xboneControllerTest.py
JOYAXISMOTION
event.axis              event.value
0 - x axis left thumb   (+1 is right, -1 is left)
1 - y axis left thumb   (+1 is down, -1 is up)
2 - x axis right thumb  (+1 is right, -1 is left)
3 - y axis right thumb  (+1 is down, -1 is up)
4 - right trigger
5 - left trigger
JOYBUTTONDOWN | JOYBUTTONUP
event.button
A = 0
B = 1
X = 2
Y = 3
LB = 4
RB = 5
BACK = 6
START = 7
XBOX = 8
LEFTTHUMB = 9
RIGHTTHUMB = 10
JOYHATMOTION
event.value
[0] - horizontal
[1] - vertival
[0].0 - middle
[0].-1 - left
[0].+1 - right
[1].0 - middle
[1].-1 - bottom
[1].+1 - top
"""
# internal ids for the xbox controls
class XboxControls:
    def __init__(self):
        self.__L_THUMB_X = 0
        self.__L_THUMB_Y = 1
        self.__R_THUMB_X = 2
        self.__R_THUMB_Y = 3
        self.__R_TRIGGER = 4
        self.__L_TRIGGER = 5
        self.__A_BUTTON = 6
        self.__B_BUTTON = 7
        self.__X_BUTTON = 8
        self.__Y_BUTTON = 9
        self.__L_BUMPER = 10
        self.__R_BUMPTER = 11
        self.__BACK_BUTTON = 12
        self.__START_BUTTON = 13
        self.__XBOX_BUTTON = 14
        self.__LEFT_THUMB = 15
        self.__RIGHT_THUMB = 16
        self.__D_PAD = 17

    def get_l_thumb_x(self): return self.__L_THUMB_X
    def set_l_thumb_x(self, value): self.__L_THUMB_X = value
    L_THUMB_X = property(get_l_thumb_x, set_l_thumb_x, "Left Stick X direction map")
    def get_l_thumb_y(self): return self.__L_THUMB_Y
    def set_l_thumb_y(self, value): self.__L_THUMB_Y = value
    L_THUMB_Y = property(get_l_thumb_y, set_l_thumb_y, "Left Stick Y direction map")

    def get_r_thumb_x(self): return self.__R_THUMB_X
    def set_r_thumb_x(self, value): self.__R_THUMB_X = value
    R_THUMBX = property(get_r_thumb_x, set_r_thumb_x, "Right Stick X direction map")
    def get_r_thumb_y(self): return self.__R_THUMB_Y
    def set_r_thumb_y(self, value): self.__R_THUMB_Y = value
    R_THUMB_Y = property(get_r_thumb_y, set_r_thumb_y, "Right Stick Y direction map")

    def get_r_trigger(self): return self.__R_TRIGGER
    def set_r_trigger(self, value): self.__R_TRIGGER = value
    R_TRIGGER = property(get_r_trigger, set_r_trigger, "Right Trigger map")
    def get_l_trigger(self): return self.__L_TRIGGER
    def set_l_trigger(self, value): self.__L_TRIGGER = value
    L_TRIGGER = property(get_l_trigger, set_l_trigger, "Left Trigger map")

    def get_a_button(self): return self.__A_BUTTON
    def set_a_button(self, value): self.__A_BUTTON = value
    A_BUTTON = property(get_a_button, set_a_button, "A Button map")
    def get_b_button(self): return self.__B_BUTTON
    def set_b_button(self, value): self.__B_BUTTON = value
    B_BUTTON = property(get_b_button, set_b_button, "B Button map")
    def get_x_button(self): return self.__X_BUTTON
    def set_x_button(self, value): self.__X_BUTTON = value
    X_BUTTON = property(get_x_button, set_x_button, "X Button map")
    def get_y_button(self): return self.__Y_BUTTON
    def set_y_button(self, value): self.__Y_BUTTON = value
    Y_BUTTON = property(get_y_button, set_y_button, "Y Button map")

    def get_l_bumper(self): return self.__L_BUMPER
    def set_l_bumper(self, value): self.__L_BUMPER = value
    L_BUMPER = property(get_l_bumper, set_l_bumper, "Left Bumper map")
    def get_r_bumper(self): return self.__R_BUMPER
    def set_r_bumper(self, value): self.__R_BUMPER = value
    R_BUMPER = property(get_r_bumper, set_r_bumper, "Right Bumper map")

    def get_back_button(self): return self.__BACK_BUTTON
    def set_back_button(self, value): self.__BACK_BUTTON = value
    BACK_BUTTON = property(get_back_button, set_back_button, "Back Button map")
    def get_start_button(self): return self.__START_BUTTON
    def set_start_button(self, value): self.__START_BUTTON = value
    START_BUTTON = property(get_start_button, set_start_button, "Start Button map")
    def get_xbox_button(self): return self.__XBOX_BUTTON
    def set_xbox_button(self, value): self.__XBOX_BUTTON = value
    XBOX_BUTTON = property(get_back_button, set_back_button, "XBOX Button map")

    def get_l_thumb(self): return self.__LEFT_THUMB
    def set_l_thumb(self, value): self.__LEFT_THUMB = value
    LEFT_THUMB = property(get_l_thumb, set_l_thumb, "Left Stick Press map")
    def get_r_thumb(self): return self.__RIGHT_THUMB
    def set_r_thumb(self, value): self.__RIGHT_THUMB = value
    RIGHT_THUMB = property(get_r_thumb, set_r_thumb, "Right Stick Press map")


# pygame axis constants for the analogue controls of the xbox controller
class PyGameAxis:
    __LTHUMBX = 0
    __LTHUMBY = 1
    __RTHUMBX = 2
    __RTHUMBY = 3
    __RTRIGGER = 4
    __LTRIGGER = 5

# pygame constants for the buttons of the xbox controller
class PyGameButtons:
    __A = 0
    __B = 1
    __X = 2
    __Y = 3
    __LB = 4
    __RB = 5
    __BACK = 6
    __START = 7
    __XBOX = 8
    __LEFTTHUMB = 9
    __RIGHTTHUMB = 10

class Controller(threading.Thread):


    def map_xbox_controller(self):
        #map between pygame axis (analogue stick) ids and xbox control ids
         __axis_control_map = {PyGameAxis.LTHUMBX: XboxControls.__L_THUMBX,
                          PyGameAxis.LTHUMBY: XboxControls.LTHUMBY,
                          PyGameAxis.RTHUMBX: XboxControls.RTHUMBX,
                          PyGameAxis.RTHUMBY: XboxControls.RTHUMBY}

        #map between pygame axis (trigger) ids and xbox control ids
        __trigger_control_map = {PyGameAxis.RTRIGGER: XboxControls.__RTRIGGER,
                             PyGameAxis.LTRIGGER: XboxControls.__LTRIGGER}

    #map between pygame buttons ids and xbox contorl ids
    BUTTONCONTROLMAP = {PyGameButtons.A: XboxControls.A,
                        PyGameButtons.B: XboxControls.B,
                        PyGameButtons.X: XboxControls.X,
                        PyGameButtons.Y: XboxControls.Y,
                        PyGameButtons.LB: XboxControls.LB,
                        PyGameButtons.RB: XboxControls.RB,
                        PyGameButtons.BACK: XboxControls.BACK,
                        PyGameButtons.START: XboxControls.START,
                        PyGameButtons.XBOX: XboxControls.XBOX,
                        PyGameButtons.LEFTTHUMB: XboxControls.LEFTTHUMB,
                        PyGameButtons.RIGHTTHUMB: XboxControls.RIGHTTHUMB}