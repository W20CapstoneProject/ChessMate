import configparser

class GameBoard:
    '''
    GameBoard
    Physical board parameters used to map square number index to coordinates.

    March 2, 2020: Currently working.
    '''

    def __init__(self):
        self.CONFIG = configparser.ConfigParser()
        self.CONFIG.read('config.ini')
        self.SQUARE_LENGTH = int(self.CONFIG['BOARD']['square_length'])
        self.SQUARE_WIDTH= int(self.CONFIG['BOARD']['square_width'])
        self.BORDER_WIDTH = int(self.CONFIG['BOARD']['border_width'])
        self.BASE_LENGTH = int(self.CONFIG['BOARD']['base_length'])
        self.X_BIAS = int(self.CONFIG['BOARD']['x_bias'])
        self.Y_BIAS = int(self.CONFIG['BOARD']['y_bias'])
        self.Z_BIAS = int(self.CONFIG['BOARD']['z_bias'])


    def get_coordinate_x(self, index):
        '''
        Call to calculate the x coordinate of the chess board square.

        March 2, 2020: Not verfied yet. Need to test with Merlin program. Need to get accurate board dimensions.
        '''
        column = index % 8
        if column == 0:
            column=8

        if (column % 2) == 0:
            x = self.SQUARE_WIDTH/2 + (column - 5) * self.SQUARE_WIDTH
        else:
            x = - self.SQUARE_WIDTH/2 - (4 - column) * self.SQUARE_WIDTH

        return x + self.X_BIAS


    def get_coordinate_y(self, index):
        '''
        Call to calculate the y coordinate of the chess board square.

        March 2, 2020: Not verfied yet. Need to test with Merlin program. Need to get accurate board dimensions.
        '''
        row = math.floor((index-1)/8)
        y = self.BASE_LENGTH + self.BORDER_WIDTH + self.SQUARE_LENGTH/2 + row * self.SQUARE_LENGTH
        return y + self.Y_BIAS


    def get_coordinate_z(self):
        '''
        Call to calculate the z coordinate of the chess board square.

        March 2, 2020: Not verfied yet. Need to test with Merlin program. Need to get accurate board dimensions.
        '''
        z = 0
        return z + self.Z_BIAS


class Mapping:
    '''
    Mapping

    Maps out the game board.

    '''
    def __init__(self):
        self.board = GameBoard()



    def plot_board(self):
        '''
        Plot all squares on the board with their corrseponding coordinate.

        March 2, 2020: Needs to be implemented still. Only used to verify coordinate map.
        '''

        '''
        board_map = []
        for index in range(1,65):
            cmd = self.cm.get_coordinate_command(index, "K")
            plt.plot(cmd)
            print("Square Number: " + str(index) + " " + str(cmd) +"\n")
        '''

        '''
        label = "{:.2f}".format(y)
        plt.annotate(label, # this is the text
                 (x,y), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center
        plt.scatter([-3.0], [48.0], label="Some Point")
        plt.xlabel('X Displacement')
        plt.ylabel('Y Displacement')
        plt.show()
        '''
        return 0
