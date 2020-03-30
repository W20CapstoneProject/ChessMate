from CMController.MoveoArm.ik import InverseKinematics
from CMController.MoveoArm.moveo_arm import MoveoArm
from CMController.MoveoArm.instruction import InstructionManager

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

    def is_within_constraints(self, commands):
        '''
        Verify that the calculated command is with the allowable constraints of the joints.
        '''
        for command in commands:
            print(command)
            within_constraints = self.arm.check_constraints(command[0], command[1], command[2], command[3])
            if (within_constraints is not True):
                return False
        
        return True

    def serialize_command(self, command):
        '''
        Given a command of format: (-1.36006, 8.02968, 56.31752, 0.0)
        Translate to move instruction for Merlin: move (-1.36006, 8.02968, 56.31752, 0.0)
        '''
        instruction = self.instruction_m.get_move_instruction(command[0], command[1], command[2], command[3])
        return instruction