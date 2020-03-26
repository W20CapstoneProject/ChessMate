'''
Test
Unit test suite for CMController actions.

March 2, 2020: Need to write accurate unit test cases for the CMController class.
'''
import sys
import unittest
from cmc import CMController
from cm_moveo import CMMoveo
from CMGame.board import GameBoard, BoardMapping
from MoveoArm.instruction import InstructionManager, MoveInstruction, BaseInstruction
from MoveoArm.ik import InverseKinematics
from MoveoArm.moveo_arm import MoveoArm
from CMGame.piece import PieceManager
from CMGame.move import MoveManager
from CMGame.interface import CMGameInterface

class TestCMController(unittest.TestCase):
    '''
    Methods of CMController:
    - connect() [Not Tested]
    - is_connected() [Not Tested]
    - list_serial_devices() [Not Tested]
    - send_command() [Not Tested]
    '''
    pass



class TestCMGame(unittest.TestCase):

    def setUp(self):
        self.board = GameBoard()

    def get_coordinate(self):
        board_map = []
        for index in range(1,65):
            cmd = self.board.get_coordinates(index)
            print("Square Number: " + str(index) + " " + str(cmd) +"\n")

        index = 4
        cmd = self.board.get_coordinates(index)
        print(cmd)

    def mapBoard(self):
        map = BoardMapping()
        map.plot_board()


class TestMoveoArm(unittest.TestCase):
    def setUp(self):
        self.arm = MoveoArm()
        self.show_joints()

    def show_joints(self):
        print("Base constraint set to " + str(self.arm.base.constraint))
        print("Should constraint set to " + str(self.arm.shoulder.constraint))
        print("Elbow constraint set to " + str(self.arm.elbow.constraint))
        print("Wrist constraint set to " + str(self.arm.wrist.constraint))
        print("Grip constraint set to " + str(self.arm.grip.constraint))

    def test_check_constraints(self):
        steps1 = (20, 20, 20, 20, 20)
        steps2 = (99, 99, 99, 99, 99)
        constraints1 = self.arm.check_constraints(steps1)
        constraints2 = self.arm.check_constraints(steps2)
        print(constraints1)
        print(constraints2)

    def test_instructions(self):
        i_manager = InstructionManager()
        mi = i_manager.get_move_instruction("+102", "-035", "-109", "+004", 0)
        bi = i_manager.get_base_instruction("+102")
        si = i_manager.get_shoulder_instruction("-035")
        ei = i_manager.get_elbow_instruction("-109")
        wi = i_manager.get_wrist_instruction("+004")
        print("Move instruction: " + mi)
        print("Base instruction: " + bi)
        print("Shoulder instruction: " + si)
        print("Elbow instruction: " + ei)
        print("Wrist instruction: " + wi)


class TestIK(unittest.TestCase):
    def setUp(self):
        self.ik = InverseKinematics()


    def mapIK(self):
        map = IKMapping()
        map.plot_xy(20, 20)


    def test_inverse_kinematics(self):
        forward = self.ik.solve_forward(12, 12, 12)
        inverse = self.ik.solve_inverse(forward[0], forward[1], forward[2])
        print("Forward 12 12 12 -> " + str(forward))
        print("Inverse -> " + str(inverse))



class TestCMMoveo(unittest.TestCase):
    def setUp(self):
        self.cmc_moveo = CMMoveo()
        self.game = CMGameInterface()
        self.mm = self.game.get_move_manager()
        self.pm = self.game.get_piece_manager()

    def test_start(self):
        self.cmc_moveo.start()

    def test_execute_move(self):
        print("Executing move..")
        self.cmc_moveo.start()
        pawn = self.pm.get_pawn()
        move = self.mm.get_move(pawn, 1, 2)
        result = self.cmc_moveo.execute_move(move)
        print(result)



if __name__ == '__main__':
    unittest.main()
