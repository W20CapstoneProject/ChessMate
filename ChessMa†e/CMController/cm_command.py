
from MoveoArm import ik
from board import GameBoard

class CMCommand:
    '''
    Contains method for converting moves into commands
    '''
    def __init__(self):
        self.ik = ik.InverseKinematics()
        self.board = GameBoard()


    def create_command(self, square_number):
        '''
        Used to create the individual commands for the Merlin system.

        1. Get cartesian coordinates of square number
        2. Use inverse kinematics to determine the required joint rotations
        3. Convert joint rotations angles to steps
        '''
        coordinates = self.get_coordinates(square_number)
        joints = self.ik.solve_inverse(coordinates[0], coordinates[1], coordinates[2])
        steps = 0
        return steps
