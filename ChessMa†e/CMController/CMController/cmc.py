import serial
import configparser
import re
import glob
import math
import logging
import matplotlib.pyplot as plt
import numpy as np


class CMController:
    '''
    CMController
    Used to interpret ChessMate based commands into coordinate commands for the Moveo Arm.

    Commands are 3 digit step commands for the following sequence of motors
    base shoulder elbow wrist grip

    Todo:
    - Verify send_command() is compatible with Merlin protocols.

    March 2, 2020: The main move execution command still needs to be completed. Also requires better unit testing to ensure the correct coordinate mapping and move consumption. Will be updating this code for the IO demonstration to work with the Merlin control program.
    '''
    port = "/dev/tty.usbmodemFD141"
    baudrate = 9600
    timeout = 5
    ack_code = 'ACK'
    success_code = 'OK!'
    code_size = 3

    def __init__(self):
        self.device = serial.Serial()
        #self.config = configparser.ConfigParser()
        #self.config.read('_config_.ini')
        #self.log = logging.basicConfig(filename=self.config['CM']['error_log'],level=logging.ERROR)


    def connect(self, port = None ):
        '''
        Setup the serial connection that will be used for communication with Merlin.
        March 2, 2020: Tested and working for general demo program.
        '''
        if port is None:
            port = self.port

        self.device.baudrate = self.baudrate
        self.device.timeout = self.timeout
        self.device.port = port
        try:
            self.device.open()
            print("Connected to :: " + port + "\n")
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
        Send the instruction to the connected device.
        March 2, 2020: Not tested yet. Needs to be finalized still.
        '''
        self.device.reset_input_buffer()
        self.device.reset_output_buffer()
        tx = self.device.write(cmd.encode())
        ack = self.device.read(self.code_size).decode()
        print("ACK: " + ack)
        complete = self.device.read(self.code_size).decode()
        print("Complete: " + complete)
        return complete


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
