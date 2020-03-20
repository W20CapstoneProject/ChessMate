'''
Test
Unit test suite for CMController actions.

March 2, 2020: Need to write accurate unit test cases for the CMController class.
'''

import unittest
import matplotlib.pyplot as plt
import numpy as np

from ik import InverseKinematics, IKMapping
from cm import CMController
from board import GameBoard, BoardMapping
import cm_move
from cm_command import CMCommand


class TestCMController(unittest.TestCase):

    def setUp(self):
        self.board = GameBoard()
        self.cm = CMController()
        self.ik = InverseKinematics()
        self.cm_command = CMCommand()

    def get_coordinate(self):
        board_map = []
        for index in range(1,65):
            cmd = self.board.get_coordinates(index)
            print("Square Number: " + str(index) + " " + str(cmd) +"\n")

        index = 4
        cmd = self.board.get_coordinates(index)
        print(cmd)


    def test_execute_moves(self):
        move = cm_move.Move(1, 2)
        commands = self.cm.execute_move(move)


    def test_mapBoard(self):
        map = BoardMapping()
        map.plot_board()



class TestIK(unittest.TestCase):
    def setUp(self):
        self.ik = InverseKinematics()


    def mapIK(self):
        map = IKMapping()
        map.plot_xy(20, 20)


    def test_inverse_kinematics(self):
        forward = self.ik.solve_forward(12, 12, 12)
        inverse = self.ik.solve_inverse(266.81, -411.49, 36)
        print(forward)
        print(inverse)




if __name__ == '__main__':
    unittest.main()
