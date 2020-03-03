import serial
import configparser
import re
import glob
import math
from board import GameBoard
import logging
import matplotlib.pyplot as plt
import numpy as np


class CMController:
    '''
    CMController
    Used to interpret ChessMate based commands into coordinate commands for the Moveo Arm.

    Example command:
    cmd = [3.0, 48.0, 0, 'K']

    March 2, 2020: The main move execution command still needs to be completed. Also requires better unit testing to ensure the correct coordinate mapping and move consumption. Will be updating this code for the IO demonstration to work with the Merlin control program.
    '''

    def __init__(self):
        self.device = serial.Serial()
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.board = GameBoard()
        self.log = logging.basicConfig(filename=self.config['CM']['error_log'],level=logging.ERROR)


    def connect(self, port = None ):
        '''
        Setup the serial connection that will be used for communication with Merlin.
        March 2, 2020: Tested and working for general demo program.
        '''
        if port is None:
            port = self.config['MERLIN']['port']

        self.device.baudrate = self.config['MERLIN']['baudrate']
        self.device.port = port
        try:
            self.device.open()
            print("Connected to ->" + port + "\n")
        except:
            print("\nCould not connect to device.")


    def is_connected(self):
        '''
        Returns True if the serial connection is still active.
        March 2, 2020: Tested and working for general demo program.
        '''
        if (self.device.is_open):
            return True
        return False


    def send_command(self, cmd):
        '''
        Send the decoded command to the connected device.
        March 2, 2020: Not tested yet. Needs to be finalized still.
        '''
        regex = r'^\d*\.?\d*$'
        p = re.compile(regex)
        m = p.match(cmd)
        result = re.findall(p, cmd)
        print(result)

        if (m):
            print("Match found " + m.group())
            #m.encode()
            #self.device.write(cmd)
        else:
            print("Not matched")

        return 1


    def get_coordinate_x(self, index):
        '''
        Call to calculate the x coordinate of the chess board square.
        March 2, 2020: Not verfied yet. Need to test with Merlin program. Need to get accurate board dimensions.
        '''
        column = index % 8
        if column == 0:
            column=8

        if (column % 2) == 0:
            x = int(self.board.SQUARE_WIDTH)/2 + (column - 5) * (int(self.board.SQUARE_WIDTH))
        else:
            x = - int(self.board.SQUARE_WIDTH)/2 - (4 - column) * (int(self.board.SQUARE_WIDTH))

        return x


    def get_coordinate_y(self, index):
        '''
        Call to calculate the y coordinate of the chess board square.
        March 2, 2020: Not verfied yet. Need to test with Merlin program. Need to get accurate board dimensions.
        '''
        row = math.floor((index-1)/8)
        y = (int(self.board.BASE_LENGTH)) + (int(self.board.BORDER_WIDTH)) + int(self.board.SQUARE_LENGTH)/2 + row * (int(self.board.SQUARE_LENGTH))
        return y

    def get_coordinate_z(self):
        '''
        Call to calculate the z coordinate of the chess board square.
        March 2, 2020: Not verfied yet. Need to test with Merlin program. Need to get accurate board dimensions.
        '''
        return 0


    def get_coordinate_command(self, square_number, action):
        '''
        Call to receive a coordinate command from the square number.
        March 2, 2020: Will work once the sub routines are verified. Also might need to change call pattern.
        '''
        x = self.get_coordinate_x(square_number)
        y = self.get_coordinate_y(square_number)
        z = self.get_coordinate_z()
        return [x, y, z, action]


    def create_commands(self):
        '''
        Create the command sequence for the Merlin software.

        The each action will have a starting and ending points.

        March 2, 2020: Needs to be implemented still.
        '''
        return 0


    def execute_move(self, move):
        '''
        Main program call to chain all commands together based off of given move
        Returns success boolean.

        March 2, 2020: Needs to be implemented still.
        '''
        try:
            if (self.is_connected()):
                print('Executing command')
                self.log.error("Executing command.")
        except:
            self.log.error("Could not execute command.")

        return False


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
        return 0



def list_serial_devices():
    '''
    Lists all devices connected via USB.

    March 2, 2020: Works and has been tested.
    '''
    i = 0
    devices = glob.glob(('/dev/tty.*'))
    for device in devices:
        print('[' + str(i) + '] ' + device)
        i += 1
    return devices
