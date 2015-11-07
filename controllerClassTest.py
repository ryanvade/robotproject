import controllerClass
import time
import sys

def control_call_back(xboxControlId, value):
    print ("Control ID = " + str(xboxControlId) +  " Value = " + str(value))

def left_thumb_x(xValue):
    print("LX" + str(xValue))

def right_thumb_x(xValue):
    print("RX" + str(xValue))

def right_thumb_y(yValue):
    print("RY" + str(yValue))

def left_thumb_y(yValue):
    print("LY" + str(yValue))

if __name__ == '__main__':
    controller = controllerClass.Controller(controller_call_back=None, joystick_number=0, dead_zone=0.1, scale=1, invert_Y_axis=True, controller_is_xbox=True)
    xboxControls = controllerClass.XboxControls
    controller.setup_control_call_back(controller.l_thumb_x, left_thumb_x)
    controller.setup_control_call_back(controller.l_thumb_y, left_thumb_y)

    try:
        controller.start()
        print("Controller startup")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print ("Exiting")

    except:
        print("Unknown Error" + sys.exc_info()[0])
        raise

    finally:
        controller.stop()

