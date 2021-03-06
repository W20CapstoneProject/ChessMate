import configparser
import math
import matplotlib.pyplot as pyplot

class GameBoard:
    '''
    GameBoard
    Physical board parameters used to map square number index to coordinates.

    March 2, 2020: Currently working.
    '''

    def __init__(self):
        self.SQUARE_LENGTH = 60.452
        self.SQUARE_WIDTH= 60.452
        self.BORDER_WIDTH = 64.0
        self.BASE_LENGTH = 85.0
        self.X_BIAS = 0
        self.Y_BIAS = 0
        self.Z_BIAS = 38.0


    def add_z_bias(self, increment):
        self.Z_BIAS = self.Z_BIAS + increment

    def add_y_bias(self, increment):
        self.Y_BIAS = self.Y_BIAS + increment

    def add_x_bias(self, increment):
        self.X_BIAS = self.X_BIAS + increment


    def get_coordinate_x(self, index):
        ''' Call to calculate the x coordinate of the chess board square. '''
        column = index % 8
        if column == 0:
            column=8

        if (column % 2) == 0:
            x = self.SQUARE_WIDTH/2 + (column - 5) * self.SQUARE_WIDTH
        else:
            x = - self.SQUARE_WIDTH/2 - (4 - column) * self.SQUARE_WIDTH

        return x + self.X_BIAS


    def get_coordinate_y(self, index):
        ''' Call to calculate the y coordinate of the chess board square. '''
        row = math.floor((index-1)/8)
        y = self.BASE_LENGTH + self.BORDER_WIDTH + self.SQUARE_LENGTH/2 + row * self.SQUARE_LENGTH
        return y + self.Y_BIAS


    def get_coordinate_z(self, piece_height):
        ''' Call to calculate the z coordinate of the chess board square.'''
        z = piece_height
        return z + self.Z_BIAS


    def get_coordinates(self, square_number, piece):
        '''
        Call to receive a coordinate command from the square number.
        March 2, 2020: Will work once the sub routines are verified. Also might need to change call pattern.
        '''
        x = self.get_coordinate_x(square_number)
        y = self.get_coordinate_y(square_number)
        z = self.get_coordinate_z(piece.get_height())
        return (x, y, z)


class BoardMapping:
    '''
    BoardMapping

    Maps out the coordinates of the game board.

    '''
    def __init__(self):
        self.board = GameBoard()


    def plot_board(self):
        '''
        Plot all squares on the board with their corrseponding coordinate.

        March 2, 2020: Needs to be implemented still. Only used to verify coordinate map.
        '''
        xs = list()
        ys = list()
        for index in range(1,65):
            xs.append(self.board.get_coordinate_x(index))
            ys.append(self.board.get_coordinate_y(index))
        pyplot.scatter(xs, ys)
        pyplot.show()
