import unittest
from cm import CMController
from board import GameBoard


class TestCMController(unittest.TestCase):

    def setUp(self):
        self.board = GameBoard()
        self.cm = CMController()

    def test_get_coordinate(self):
        #index = 1
        for index in range(1,65):
            x = self.cm.get_coordinate_x(index)
            y = self.cm.get_coordinate_y(index)
            print("Square Number: " + str(index) + " ( "+str(x)+", " + str(y) + ")\n")

        index = 4
        cmd = self.cm.get_coordinate_command(index)
        print(cmd)
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()
