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
    123 637 812 382 732

    Commands are 3 digit step commands for the following sequence of motors
    base shoulder elbow wrist grip

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
        self.device.timeout = int(self.config['MERLIN']['timeout'])
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
        self.device.reset_input_buffer()
        self.device.reset_output_buffer()
        tx = self.device.write(cmd.encode())
        ack = self.device.read(3).decode()
        print(ack)
        complete = self.device.read(3).decode()
        print(complete)
        return complete


    def get_coordinates(self, square_number):
        '''
        Call to receive a coordinate command from the square number.
        March 2, 2020: Will work once the sub routines are verified. Also might need to change call pattern.
        '''
        x = self.board.get_coordinate_x(square_number)
        y = self.board.get_coordinate_y(square_number)
        z = self.board.get_coordinate_z()
        return [x, y, z]


    def create_commands(self, moves):
        '''
        Create the command sequence for the Merlin software.

        The each action will have a starting and ending points.

        March 2, 2020: Needs to be implemented still.
        '''
        for move in moves:
            print(move)

        return 0


    def execute_moves(self, moves):
        '''
        Main program call to chain all commands together based off of given move
        Returns success boolean.

        March 2, 2020: Needs to be implemented still.
        '''
        try:
            if (self.is_connected()):
                print('Executing command')
                self.create_commands(move)
                self.log.error("Executing command.")
        except:
            self.log.error("Could not execute command.")

        return False



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
