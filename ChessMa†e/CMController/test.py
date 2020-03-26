'''
Test
Unit test suite for CMController actions.

March 2, 2020: Need to write accurate unit test cases for the CMController class.
'''
import sys
import unittest
from cm import CMController
from CMGame.board import GameBoard, BoardMapping
from CMGame.move import Move
from MoveoArm.command import Command
from MoveoArm.ik import InverseKinematics
from MoveoArm.moveo_arm import MoveoArm
from CMGame.piece import PieceManager


class TestCMController(unittest.TestCase):

    def setUp(self):
        self.board = GameBoard()
        self.cm = CMController()
        self.cm_command = Command(self.board)

    def get_coordinate(self):
        board_map = []
        for index in range(1,65):
            cmd = self.board.get_coordinates(index)
            print("Square Number: " + str(index) + " " + str(cmd) +"\n")

        index = 4
        cmd = self.board.get_coordinates(index)
        print(cmd)


    def test_execute_moves(self):
        pm = PieceManager()
        pawn = pm.pawn
        move = Move(piece = pawn, start = 1, end = 2)
        commands = self.cm.execute_move(move)


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



if __name__ == '__main__':
    unittest.main()
