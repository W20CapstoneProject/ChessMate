from .moveo_arm import MoveoArm
from .ik import InverseKinematics

class CommandManager():
    pass

class Command:
    '''
    Contains method for converting moves into commands
    '''
    def __init__(self, platform):
        self.ik = InverseKinematics()
        self.arm = MoveoArm()
        self.platform = platform


    def create_command(self, square_number):
        '''
        Used to create the individual commands for the Merlin system.

        1. Get cartesian coordinates of square number
        2. Use inverse kinematics to determine the required joint rotations
        3. Convert joint rotations angles to steps
        '''
        coordinates = self.get_coordinates(square_number)
        degrees = self.ik.solve_inverse(coordinates[0], coordinates[1], coordinates[2])
        steps = self.arm.calculate_steps()
        return steps


class MoveCommand():
    def __init_(self):
        self.instruction = InstructionList.move
        self.base = Arm.base_command()
        self.shoulder = Arm.shoulder_command()
        self.elbow = Arm.elbow_command()
        self.wrist = Arm.wrist_command()
        self.grip = 0

    def getCommand():
        pass



class InstructionList:

    def __init__(self):
        self.move = "move"
        self.base = "base"
        self.shoulder = "shoulder"
        self.elbow = "elbow"
        self.wrist = "wrist"
        self.grip = "grip"