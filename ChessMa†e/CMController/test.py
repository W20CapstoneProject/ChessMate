'''
Test
Unit test suite for CMController actions.

March 2, 2020: Need to write accurate unit test cases for the CMController class.
'''

import unittest
from cm import CMController
from board import GameBoard
import matplotlib.pyplot as plt
import numpy as np
from ik import InverseKinematics


class TestCMController(unittest.TestCase):

    def setUp(self):
        self.board = GameBoard()
        self.cm = CMController()
        self.ik = InverseKinematics()

    def test_get_coordinate(self):
        board_map = []
        for index in range(1,65):
            cmd = self.cm.get_coordinates(index)
            plt.plot(cmd)
            print("Square Number: " + str(index) + " " + str(cmd) +"\n")

        index = 4
        cmd = self.cm.get_coordinates(index)
        print(cmd)
        self.assertEqual('foo'.upper(), 'FOO')

    def test_execute_moves(self):
        self.cm.execute_moves("Move")
        self.assertEqual('foo'.upper(), 'FOO')

    def test_inverse_kinematics(self):
        forward = self.ik.forward(12, 12, 12)
        print(forward)


if __name__ == '__main__':
    unittest.main()
