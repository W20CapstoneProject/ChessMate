import keyboard

class MoveoCalibrate:
    '''
    Calibrate

    Can be used to increment stepper motors to help to zero them to a starting position.

    Runs a calibrate program which will target the 4 corners of the board.
    '''

    def __init__(self):
        self.bias = 0

    def calibrate_stepper(self, stepper):
        pass

    def calibrate_arm(self):
        pass
