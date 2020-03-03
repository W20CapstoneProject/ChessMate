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


class TestCMController(unittest.TestCase):

    def setUp(self):
        self.board = GameBoard()
        self.cm = CMController()

    def test_get_coordinate(self):
        board_map = []
        for index in range(1,65):
            cmd = self.cm.get_coordinate_command(index, "K")
            plt.plot(cmd)
            print("Square Number: " + str(index) + " " + str(cmd) +"\n")

        index = 4
        cmd = self.cm.get_coordinate_command(index, "K")
        print(cmd)
        self.assertEqual('foo'.upper(), 'FOO')

    def test_execute_move(self):
        self.cm.execute_move("Move")
        self.assertEqual('foo'.upper(), 'FOO')


if __name__ == '__main__':
    unittest.main()
