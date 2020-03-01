import serial
import configparser
import re
import glob
import math
from board import GameBoard


class CMController:
    '''
    CMController

    Used to interpret ChessMate based commands into coordinate commands for the Moveo Arm.

    Example command:
    cmd = [3.0, 48.0, 0, 'K']
    '''

    def __init__(self):
        self.device = serial.Serial()
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.board = GameBoard()


    def connect(self, port = None ):
        '''
        Setup the serial connection that will be used for communication with Merlin.
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
        ''' Returns True if the serial connection is still active. '''
        if (self.device.is_open):
            return True
        return False


    def send_command(self, cmd):
        ''' Send the decoded command to the connected device. '''
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
        '''
        row = math.floor((index-1)/8)
        y = (int(self.board.BASE_LENGTH)) + (int(self.board.BORDER_WIDTH)) + int(self.board.SQUARE_LENGTH)/2 + row * (int(self.board.SQUARE_LENGTH))
        return y

    def get_coordinate_Z(self):
        '''
        Call to calculate the z coordinate of the chess board square.
        '''
        return 0


    def get_coordinate_command(self, square_number, action):
        '''
        Call to receive a coordinate command from the square number.
        '''
        x = self.get_coordinate_x(square_number)
        y = self.get_coordinate_y(square_number)
        z = self.get_coordinate_z()
        return [x, y, z, action]


    def create_commands(self, action):
        '''
        Create the command sequence for the Merlin software.

        The each action will have a starting and ending points
        '''



def list_serial_devices():
    ''' Lists all devices connected via USB '''
    i = 0
    devices = glob.glob(('/dev/tty.*'))
    for device in devices:
        print('[' + str(i) + '] ' + device)
        i += 1
    return devices
