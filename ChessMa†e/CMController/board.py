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
        self.SQUARE_LENGTH = self.CONFIG['PHYSICAL']['square_length']
        self.SQUARE_WIDTH= self.CONFIG['PHYSICAL']['square_width']
        self.BORDER_WIDTH = self.CONFIG['PHYSICAL']['border_width']
        self.BASE_LENGTH = self.CONFIG['PHYSICAL']['base_length']
