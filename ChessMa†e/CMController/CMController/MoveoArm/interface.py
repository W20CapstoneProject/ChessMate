from CMController.MoveoArm.ik import InverseKinematics
from CMController.MoveoArm.moveo_arm import MoveoArm
from CMController.MoveoArm.instruction import InstructionManager
from CMController.MoveoArm.instruction import MerlinInstruction

class MoveoInterface:
    '''
    Can be used to control the MoveoArm.

    Will include all information necessary to calculate commands and instructions for the arm.
    '''
    def __init__(self):
        self.ik = InverseKinematics()
        self.arm = MoveoArm()
        self.instruction_m = InstructionManager()
        self.merlin_instruction= MerlinInstruction()

    def get_degrees_from_coordinates(self, x, y, z):
        ''' Calculates the inverse kinematics equation. '''
        phi = self.ik.calculate_phi(x, y, z)
        base = self.ik.calculate_base(x, y)
        shoulder, elbow, wrist = self.ik.solve_inverse(x, y, phi)
        grip = 0
        return (base, shoulder, elbow, wrist, grip)

    def get_steps_from_degrees(self, base, shoulder, elbow, wrist, grip):
        ''' Calculate the steps required based off of the given degrees. '''
        return self.arm.calculate_steps(base, shoulder, elbow, wrist, grip)

    def is_within_constraints(self, commands):
        ''' Verify that the calculated command is with the allowable constraints of the joints.'''
        for cmd in commands:
            within_constraints = self.arm.verify_steps(cmd[0], cmd[1], cmd[2], cmd[3])
            if (within_constraints is not True):
                return False
        return True

    def serialize_command(self, command):
        '''
        Given a command of format: (-1.36006, 8.02968, 56.31752, 0.0)
        Translate to move instruction for Merlin: move (-1.36006, 8.02968, 56.31752, 0.0)
        Returns - (base, shoulder, elbow, wrist)
        '''
        instruction = self.merlin_instruction.create(command[0], command[1], command[2], command[3], command[4])
        return instruction