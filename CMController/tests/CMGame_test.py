'''
Test
Unit test suite for CMController actions.

March 2, 2020: Need to write accurate unit test cases for the CMController class.
'''
import sys
import unittest
from CMController.CMGame.board import GameBoard, BoardMapping
from CMController.CMGame.piece import Pawn


class TestCMGame(unittest.TestCase):

    def setUp(self):
        self.board = GameBoard()
        self.piece = Pawn()

    def get_coordinate(self):
        board_map = []
        for index in range(1,65):
            cmd = self.board.get_coordinates(index, self.piece)
            print("Square Number: " + str(index) + " " + str(cmd) +"\n")

        index = 4
        cmd = self.board.get_coordinates(index)
        print(cmd)

    def mapBoard(self):
        map = BoardMapping()
        map.plot_board()


if __name__ == '__main__':
    unittest.main()
