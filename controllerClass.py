__author__ = 'ryanvade'
import os
import threading

import pygame

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
        self.__R_BUMPER = 11
        self.__BACK_BUTTON = 12
        self.__START_BUTTON = 13
        self.__XBOX_BUTTON = 14
        self.__LEFT_THUMB = 15
        self.__RIGHT_THUMB = 16
        self.__D_PAD = 17

    def get_l_thumb_x(self): return self.__L_THUMB_X

    def set_l_thumb_x(self, value): self.__L_THUMB_X = value

    def del_l_thumb_x(self): del self.__L_THUMB_X

    L_THUMB_X = property(get_l_thumb_x, set_l_thumb_x, del_l_thumb_x, "Left Stick X direction map")

    def get_l_thumb_y(self): return self.__L_THUMB_Y

    def set_l_thumb_y(self, value): self.__L_THUMB_Y = value

    def del_l_thumb_y(self): del self.__L_THUMB_Y

    L_THUMB_Y = property(get_l_thumb_y, set_l_thumb_y, del_l_thumb_y, "Left Stick Y direction map")

    def get_r_thumb_x(self): return self.__R_THUMB_X

    def set_r_thumb_x(self, value): self.__R_THUMB_X = value

    def del_r_thumb_x(self): del self.__R_THUMB_X

    R_THUMB_X = property(get_r_thumb_x, set_r_thumb_x, del_r_thumb_x, "Right Stick X direction map")

    def get_r_thumb_y(self): return self.__R_THUMB_Y

    def set_r_thumb_y(self, value): self.__R_THUMB_Y = value

    def del_r_thumb_Y(self): del self.__R_THUMB_Y

    R_THUMB_Y = property(get_r_thumb_y, set_r_thumb_y, del_r_thumb_Y, "Right Stick Y direction map")

    def get_r_trigger(self): return self.__R_TRIGGER

    def set_r_trigger(self, value): self.__R_TRIGGER = value

    def del_r_trigger(self): del self.__R_TRIGGER

    R_TRIGGER = property(get_r_trigger, set_r_trigger, del_r_trigger, "Right Trigger map")

    def get_l_trigger(self): return self.__L_TRIGGER

    def set_l_trigger(self, value): self.__L_TRIGGER = value

    def del_l_trigger(self): del self.__L_TRIGGER

    L_TRIGGER = property(get_l_trigger, set_l_trigger, del_l_trigger, "Left Trigger map")

    def get_a_button(self): return self.__A_BUTTON

    def set_a_button(self, value): self.__A_BUTTON = value

    def del_a_button(self): del self.__A_BUTTON

    A_BUTTON = property(get_a_button, set_a_button, del_a_button, "A Button map")

    def get_b_button(self): return self.__B_BUTTON

    def set_b_button(self, value): self.__B_BUTTON = value

    def del_b_button(self): del self.__B_BUTTON

    B_BUTTON = property(get_b_button, set_b_button, del_b_button, "B Button map")

    def get_x_button(self): return self.__X_BUTTON

    def set_x_button(self, value): self.__X_BUTTON = value

    def del_x_button(self): del self.__X_BUTTON

    X_BUTTON = property(get_x_button, set_x_button, del_x_button, "X Button map")

    def get_y_button(self): return self.__Y_BUTTON

    def set_y_button(self, value): self.__Y_BUTTON = value

    def del_y_button(self): del self.__Y_BUTTON

    Y_BUTTON = property(get_y_button, set_y_button, del_y_button, "Y Button map")

    def get_l_bumper(self): return self.__L_BUMPER

    def set_l_bumper(self, value): self.__L_BUMPER = value

    def del_l_bumper(self): del self.__L_BUMPER

    LEFT_BUMPER = property(get_l_bumper, set_l_bumper, del_l_bumper, "Left Bumper map")

    def get_r_bumper(self): return self.__R_BUMPER

    def set_r_bumper(self, value): self.__R_BUMPER = value

    def del_r_bumper(self): del self.__R_BUMPER

    RIGHT_BUMPER = property(get_r_bumper, set_r_bumper, del_r_bumper, "Right Bumper map")

    def get_back_button(self): return self.__BACK_BUTTON

    def set_back_button(self, value): self.__BACK_BUTTON = value

    def del_back_button(self): del self.__BACK_BUTTON

    BACK_BUTTON = property(get_back_button, set_back_button, del_back_button, "Back Button map")

    def get_start_button(self): return self.__START_BUTTON

    def set_start_button(self, value): self.__START_BUTTON = value

    def del_start_button(self): del self.__START_BUTTON

    START_BUTTON = property(get_start_button, set_start_button, del_start_button, "Start Button map")

    def get_xbox_button(self): return self.__XBOX_BUTTON

    def set_xbox_button(self, value): self.__XBOX_BUTTON = value

    def del_xbox_button(self): del self.__XBOX_BUTTON

    XBOX_BUTTON = property(get_back_button, set_back_button, del_xbox_button, "XBOX Button map")

    def get_l_thumb(self): return self.__LEFT_THUMB

    def set_l_thumb(self, value): self.__LEFT_THUMB = value

    def del_l_thumb(self): del self.__LEFT_THUMB

    LEFT_THUMB = property(get_l_thumb, set_l_thumb, del_l_thumb, "Left Stick Press map")

    def get_r_thumb(self): return self.__RIGHT_THUMB

    def set_r_thumb(self, value): self.__RIGHT_THUMB = value

    def del_r_thumb(self): del self.__RIGHT_THUMB

    RIGHT_THUMB = property(get_r_thumb, set_r_thumb, del_r_thumb, "Right Stick Press map")

    def get_d_pad(self): return self.__D_PAD

    def set_d_pad(self, value): self.__D_PAD = value

    def del_d_pad(self): del self.__D_PAD

    D_PAD = property(get_d_pad, set_d_pad, del_d_pad, "D Pad map")


# pygame axis constants for the analogue controls (Sticks)
class PyGameAxis:
    def __init__(self):
        self.__L_THUMB_X = 0
        self.__L_THUMB_Y = 1
        self.__R_THUMB_X = 2
        self.__R_THUMB_Y = 3
        self.__R_TRIGGER = 4
        self.__L_TRIGGER = 5

    def get_l_thumb_x(self): return self.__L_THUMB_X

    def set_l_thumb_x(self, value): self.__L_THUMB_X = value

    def del_l_thumb_x(self): del self.__L_THUMB_X

    L_THUMB_X = property(get_l_thumb_x, set_l_thumb_x, del_l_thumb_x, "Left Stick X Direction map - Pygame")

    def get_l_thumb_y(self): return self.__L_THUMB_Y

    def set_l_thumb_y(self, value): self.__L_THUMB_Y = value

    def del_l_thumb_y(self): del self.__L_THUMB_Y

    L_THUMB_Y = property(get_l_thumb_y, set_l_thumb_y, del_l_thumb_y, "Left Stick Y Direction map - Pygame")

    def get_r_thumb_x(self): return self.__R_THUMB_X

    def set_r_thumb_x(self, value): self.__R_THUMB_X = value

    def del_r_thumb_x(self): del self.__R_THUMB_X

    R_THUMB_X = property(get_r_thumb_x, set_r_thumb_x, del_r_thumb_x, "Right Stick X Direction map - Pygame")

    def get_r_thumb_y(self): return self.__R_THUMB_Y

    def set_r_thumb_y(self, value): self.__R_THUMB_Y = value

    def del_r_thumb_y(self): del self.__R_THUMB_Y

    R_THUMB_Y = property(get_r_thumb_y, set_r_thumb_y, del_r_thumb_y, "Right Stick Y Direction map - Pygame")

    def get_r_trigger(self): return self.__R_TRIGGER

    def set_r_trigger(self, value): self.__R_TRIGGER = value

    def del_r_trigger(self): del self.R_TRIGGER

    R_TRIGGER = property(get_r_trigger, set_r_trigger, del_r_trigger, "Right Trigger map - Pygame")

    def get_l_trigger(self): return self.__L_TRIGGER

    def set_l_trigger(self, value): self.__L_TRIGGER = value

    def del_l_trigger(self): del self.__L_TRIGGER

    L_TRIGGER = property(get_l_trigger, set_l_trigger, del_l_trigger, "Left Trigger map - Pygame")


# pygame constants for the buttons
class PyGameButtons:
    def __init__(self):
        self.__A_BUTTON = 0
        self.__B_BUTTON = 1
        self.__X_BUTTON = 2
        self.__Y_BUTTON = 3
        self.__LEFT_BUMPER = 4
        self.__RIGHT_BUMPER = 5
        self.__BACK_BUTTON = 6
        self.__START_BUTTON = 7
        self.__HOME_BUTTON = 8
        self.__LEFT_THUMB = 9
        self.__RIGHT_THUMB = 10

    def get_a_button(self): return self.__A_BUTTON

    def set_a_buton(self, value): self.__A_BUTTON = value

    def del_a_button(self): del self.__A_BUTTON

    A_BUTTON = property(get_a_button, set_a_buton, del_a_button, "A Button Map - Pygame")

    def get_b_button(self): return self.__B_BUTTON

    def set_b_buton(self, value): self.__B_BUTTON = value

    def del_b_button(self): del self.__B_BUTTON

    B_BUTTON = property(get_b_button, set_b_buton, del_b_button, "B Button Map - Pygame")

    def get_x_button(self): return self.__X_BUTTON

    def set_x_buton(self, value): self.__X_BUTTON = value

    def del_x_button(self): del self.__X_BUTTON

    X_BUTTON = property(get_x_button, set_x_buton, del_x_button, "X Button Map - Pygame")

    def get_y_button(self): return self.__Y_BUTTON

    def set_y_buton(self, value): self.__Y_BUTTON = value

    def del_y_button(self): del self.__Y_BUTTON

    Y_BUTTON = property(get_y_button, set_y_buton, del_y_button, "Y Button Map - Pygame")

    def get_left_bumper(self): return self.__LEFT_BUMPER

    def set_left_bumper(self, value): self.__LEFT_BUMPER = value

    def del_left_bumper(self): del self.__LEFT_BUMPER

    LEFT_BUMPER = property(get_left_bumper, set_left_bumper, del_left_bumper, "Left Bumper map - Pygame")

    def get_right_bumper(self): return self.__RIGHT_BUMPER

    def set_right_bumper(self, value): self.__RIGHT_BUMPER = value

    def del_right_bumper(self): del self.__RIGHT_BUMPER

    RIGHT_BUMPER = property(get_left_bumper, set_left_bumper, del_right_bumper, "Right Bumper map - Pygame")

    def get_back_button(self): return self.__BACK_BUTTON

    def set_back_button(self, value): self.__BACK_BUTTON = value

    def del_back_button(self): del self.__BACK_BUTTON

    BACK_BUTTON = property(get_back_button, set_back_button, del_back_button, "Back Button map - Pygame")

    def get_start_button(self): return self.__START_BUTTON

    def set_start_button(self, value): self.__START_BUTTON = value

    def del_start_button(self): del self.__START_BUTTON

    START_BUTTON = property(get_start_button, set_start_button, del_start_button, "Start Button map - Pygame")

    def get_home_button(self): return self.__HOME_BUTTON

    def set_home_button(self, value): self.__HOME_BUTTON = value

    def del_home_button(self): del self.__HOME_BUTTON

    HOME_BUTTON = property(get_home_button, set_home_button, del_home_button, "Home Button map - Pygame")

    def get_left_thumb(self): return self.__LEFT_THUMB

    def set_left_thumb(self, value): self.__LEFT_THUMB = value

    def del_left_thumb(self): del self.__LEFT_THUMB

    LEFT_THUMB = property(get_left_thumb, set_left_thumb, del_left_thumb, "Left Stick press map - Pygame")

    def get_right_thumb(self): return self.__RIGHT_THUMB

    def set_right_thumb(self, value): self.__RIGHT_THUMB = value

    def del_right_thumb(self): del self.__RIGHT_THUMB

    RIGHT_THUMB = property(get_right_thumb, set_right_thumb, del_right_thumb, "Right Stick press map - Pygame")


class Controller(threading.Thread):
    def __init__(self, controller_call_back=None, joystick_number=0, dead_zone=0.1, scale=1,
                 invert_Y_axis=False, controller_is_xbox=True):
        threading.Thread.__init__(self)
        self.__running = False
        self.__controller_call_back = controller_call_back
        self.__joystick_number = joystick_number
        self.__lower_dead_zone = dead_zone * -1
        self.__upper_dead_zone = dead_zone
        self.__scale = scale
        self.__invert_Y_axis = invert_Y_axis
        self.__controller_call_backs = {}
        self.__controller_is_xbox = controller_is_xbox
        self.__pygame_axis = PyGameAxis()
        self.__pygame_buttons = PyGameButtons()
        self.__controller_mapping = None
        self.__axis_control_map = None
        self.__trigger_control_map = None
        self.__button_control_map = None
        self.__controller_values = None

        if self.__controller_is_xbox:
            self.__controller_mapping = XboxControls()
            # map between pygame axis (analogue stick) ids and xbox control ids
            self.__axis_control_map = {self.__pygame_axis.L_THUMB_X: self.__controller_mapping.L_THUMB_X,
                                       self.__pygame_axis.L_THUMB_Y: self.__controller_mapping.L_THUMB_Y,
                                       self.__pygame_axis.R_THUMB_X: self.__controller_mapping.R_THUMB_X,
                                       self.__pygame_axis.R_THUMB_Y: self.__controller_mapping.R_THUMB_Y}

            # map between pygame axis (trigger) ids and xbox control ids
            self.__trigger_control_map = {self.__pygame_axis.R_TRIGGER: self.__controller_mapping.R_TRIGGER,
                                          self.__pygame_axis.L_TRIGGER: self.__controller_mapping.L_TRIGGER}

            # map between pygame buttons ids and xbox contorl ids
            self.__button_control_map = {self.__pygame_buttons.A_BUTTON: self.__controller_mapping.A_BUTTON,
                                         self.__pygame_buttons.B_BUTTON: self.__controller_mapping.B_BUTTON,
                                         self.__pygame_buttons.X_BUTTON: self.__controller_mapping.X_BUTTON,
                                         self.__pygame_buttons.Y_BUTTON: self.__controller_mapping.Y_BUTTON,
                                         self.__pygame_buttons.LEFT_BUMPER: self.__controller_mapping.LEFT_BUMPER,
                                         self.__pygame_buttons.RIGHT_BUMPER: self.__controller_mapping.RIGHT_BUMPER,
                                         self.__pygame_buttons.BACK_BUTTON: self.__controller_mapping.BACK_BUTTON,
                                         self.__pygame_buttons.START_BUTTON: self.__controller_mapping.START_BUTTON,
                                         self.__pygame_buttons.HOME_BUTTON: self.__controller_mapping.XBOX_BUTTON,
                                         self.__pygame_buttons.LEFT_THUMB: self.__controller_mapping.LEFT_THUMB,
                                         self.__pygame_buttons.RIGHT_THUMB: self.__controller_mapping.RIGHT_THUMB}

            # initial controller v__controller_call_backsalues
            self.__controller_values = {self.__controller_mapping.L_THUMB_X: 0,
                                        self.__controller_mapping.L_THUMB_Y: 0,
                                        self.__controller_mapping.R_THUMB_X: 0,
                                        self.__controller_mapping.R_THUMB_Y: 0,
                                        self.__controller_mapping.R_TRIGGER: 0,
                                        self.__controller_mapping.L_TRIGGER: 0,
                                        self.__controller_mapping.A_BUTTON: 0,
                                        self.__controller_mapping.B_BUTTON: 0,
                                        self.__controller_mapping.X_BUTTON: 0,
                                        self.__controller_mapping.Y_BUTTON: 0,
                                        self.__controller_mapping.LEFT_BUMPER: 0,
                                        self.__controller_mapping.RIGHT_BUMPER: 0,
                                        self.__controller_mapping.BACK_BUTTON: 0,
                                        self.__controller_mapping.START_BUTTON: 0,
                                        self.__controller_mapping.XBOX_BUTTON: 0,
                                        self.__controller_mapping.LEFT_THUMB: 0,
                                        self.__controller_mapping.RIGHT_THUMB: 0,
                                        self.__controller_mapping.D_PAD: (0, 0)}
        else:
            print("Not using an Xbox Controller")
            # TODO generic controller mappings

            # Create controller properties
        @property
        def l_thumb_x(self):
            return self.__controller_values[self.__controller_mapping.L_THUMB_X]

        @property
        def l_thumb_y(self):
            return self.__controller_values[self.__controller_mapping.L_THUMB_Y]

        @property
        def r_thumb_x(self):
            return self.__controller_values[self.__controller_mapping.R_THUMB_X]

        @property
        def r_thumb_y(self):
            return self.__controller_values[self.__controller_mapping.R_THUMB_Y]

        @property
        def r_trigger(self):
            return self.__controller_values[self.__controller_mapping.R_TRIGGER]

        @property
        def l_trigger(self):
            return self.__controller_values[self.__controller_mapping.L_TRIGGER]

        @property
        def a_button(self):
            return self.__controller_values[self.__controller_mapping.A_BUTTON]

        @property
        def b_button(self):
            return self.__controller_values[self.__controller_mapping.B_BUTTON]

        @property
        def x_button(self):
            return self.__controller_values[self.__controller_mapping.X_BUTTON]

        @property
        def y_button(self):
            return self.__controller_values[self.__controller_mapping.Y_BUTTON]

        @property
        def left_bumper(self):
            return self.__controller_values[self.__controller_mapping.LEFT_BUMPER]

        @property
        def right_button(self):
            return self.__controller_values[self.__controller_mapping.RIGHT_BUMPER]

        @property
        def back_button(self):
            return self.__controller_values[self.__controller_mapping.BACK_BUTTON]

        @property
        def start_button(self):
            return self.__controller_values[self.__controller_mapping.START_BUTTON]

        @property
        def home_button(self):
            return self.__controller_values[self.__controller_mapping.HOME_BUTTON]

        @property
        def left_thumb(self):
            return self.__controller_values[self.__controller_mapping.LEFT_THUMB]

        @property
        def right_thumb(self):
            return self.__controller_values[self.__controller_mapping.RIGHT_THUMB]

        @property
        def d_pad(self):
            return self.__controller_values[self.__controller_mapping.D_PAD]

        # call pygame setup
        self._setup_pygame(self.__joystick_number)

    # setup pygame
    @staticmethod
    def _setup_pygame(joystick_number):
        # set SDL to use the dummy NULL video driver, so it doesn't need a windowing system.
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        # init pygame
        pygame.init()
        # create a 1x1 pixel screen, its not used so it doesnt matter
        screen = pygame.display.set_mode((1, 1))
        # init the joystick control
        pygame.joystick.init()
        # get the first joystick
        joy = pygame.joystick.Joystick(joystick_number)
        # init that joystick
        joy.init()

    # override run in threading.Thread
    def run(self):
        self._start()

    # start the controller
    def _start(self):
        self.__running = True
        # run until the controller is stopped
        while self.__running:
            # react to the pygame events that come from the xbox controller
            for event in pygame.event.get():
                # thumb sticks, trigger buttons
                if event.type == pygame.JOYAXISMOTION:
                    # is this axis on our controller
                    if event.axis in self.__axis_control_map:
                        # is this a y axis
                        y_axis = True if (event.axis == self.__pygame_axis.L_THUMB_Y or
                                          event.axis == self.__pygame_axis.R_THUMB_Y) else False
                        # update the control value
                        self.__update_controller_value(self.__axis_control_map[event.axis],
                                                       self._rebase_axis_value(event.value, y_axis))
                    # is this axis a trigger
                    if event.axis in self.__trigger_control_map:
                        # update the control value
                        self.__update_controller_value(self.__trigger_control_map[event.axis],
                                                       self._rebase_trigger_value(event.value))

                # d pad
                elif event.type == pygame.JOYHATMOTION:
                    # update control value
                    self.__update_controller_value(self.__controller_mapping.D_PAD, event.value)

                # button pressed and unpressed
                elif event.type == pygame.JOYBUTTONUP or event.type == pygame.JOYBUTTONDOWN:
                    # is this button on our controller
                    if event.button in self.__button_control_map:
                        # update control value
                        self.__update_controller_value(self.__button_control_map[event.button],
                                                       self._rebase_button_value(event.type))

    # stops the controller
    def stop(self):
        self.__running = False

    # updates a specific value in the control dictionary
    def __update_controller_value(self, control, value):
        # if the value has changed update it and call the callbacks
        if self.__controller_values[control] != value:
            self.__controller_values[control] = value
            self.__do_call_backs(control, value)

    # calls the call backs if necessary
    def __do_call_backs(self, control, value):
        # call the general callback
        if self.__controller_call_back is not None: self.__controller_call_back(control, value)

        # has a specific callback been setup?
        if control in self.__controller_call_backs:
            self.__controller_call_backs[control](value)

    # used to add a specific callback to a control
    def setup_control_call_back(self, control, call_back_function):
        # add callback to the dictionary
        self.__controller_call_backs[control] = call_back_function

    # scales the axis values, applies the deadzone
    def _rebase_axis_value(self, value, y_axis=False):
        # invert yAxis
        if y_axis and self.__invert_Y_axis: value *= -1
        # scale the value
        value *= self.__scale
        # apply the dead zones
        if self.__upper_dead_zone > value > self.__lower_dead_zone: value = 0
        return value

    # turns the trigger value into something sensible and scales it
    def _rebase_trigger_value(self, value):
        # returns values (0, 1) given (-1, 1) from pygame
        value = max(0, (value + 1) / 2)
        # scale the value
        value *= self.__scale
        return value

    # turns the event type (up/down) into a value
    @staticmethod
    def _rebase_button_value(event_type):
        # if the button is down its 1, if the button is up its 0
        value = 1 if event_type == pygame.JOYBUTTONDOWN else 0
        return value
