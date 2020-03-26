from ik import InverseKinematics
from moveo_arm import MoveoArm
from calibrate import MoveoCalibrate

class CMControl:
    '''
    Can be used to control the MoveoArm.

    Will include all information necessary to calculate commands and instructions for the arm.
    '''
    def __init__(self):
        self.ik = InverseKinematics()
        self.arm = MoveoArm()
        self.calibration = Calibration()