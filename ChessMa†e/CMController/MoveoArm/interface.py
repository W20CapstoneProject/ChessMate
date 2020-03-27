from .ik import InverseKinematics
from .moveo_arm import MoveoArm
from .instruction import InstructionManager

class MoveoInterface:
    '''
    Can be used to control the MoveoArm.

    Will include all information necessary to calculate commands and instructions for the arm.
    '''
    def __init__(self):
        self.ik = InverseKinematics()
        self.arm = MoveoArm()
        self.instruction_m = InstructionManager()

    def get_inverse(self, x, y, phi):
        return self.ik.solve_inverse(x, y, phi)

    def get_steps_from_degrees(self, base, shoulder, elbow, wrist):
        return self.arm.calculate_steps(base, shoulder, elbow, wrist)

    def verify_commands(self, steps):
        '''
        Check the given steps
        '''
        return self.arm.check_constraints(steps)