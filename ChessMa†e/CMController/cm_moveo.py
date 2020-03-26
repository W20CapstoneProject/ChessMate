from cmc import CMController 
from CMGame.interface import CMGameInterface
from MoveoArm.interface import MoveoInterface


class CMMoveo:
    '''
    This class serves as the ChessMate software and Moveo/Merlin integration program. It contains the three methods required for communication
    between the two.

    On startup, ChessMate calls start() to connect to the Moveo arm via serial comms.

    When ChessMate needs to send a move to the Moveo it will call execute_move(). This will take in 
    one Move class as an argument. The function will then create a command for the arm based off of this move.

    When the game is over ChessMate will call end() as a destructor for this class.
    '''

    def __init__(self):
        self.cmc = CMController()
        self.game = CMGameInterface()
        self.moveo_interface = MoveoInterface()
        self.command_handler = CommandHandler()
        self.cmd_history = list()

    def start(self):
        '''
        Connect to the Moveo Arm. If the arm is connected then return true otherwise false.
        '''
        self.cmc.connect()
        return self.cmc.is_connected()

    
    def execute_move(self, move):
        '''
        Main program call to chain all commands together based off of one given move
        Returns success boolean when move is completed.
        Procedure
        ---
        1. Receive a Move() from the ChessMate program.
        2. Generate commands list from the Move() object.
        ---
        3. Ensure that the commands are feasible for the Moveo Arm.
        4. Send the command to the Moveo Arm via the serial lines.
        5. Wait for ACK then continue sending commands until the move is completed.
        ---

        Moves - array of moves that need to be executed in order for the chess action
        March 2, 2020: Needs to be implemented still.
        '''
        success = "OK!"
        if (self.cmc.is_connected()):
            cmds = move.create_commands(self.command_handler)
            #TODO: Fix to actually verify commands
            self.moveo_interface.verify_commands((0, 0, 0, 0, 0))
            
            for cmd in cmds:
                print("cmd: " + str(cmd))
                serialized = str(cmd)
                response = self.cmc.send_command(serialized)
                print(response)
                if (response == success):
                    self.cmd_history.append()
                else: 
                    raise Exception ("Merlin", "Merlin failed to execute command")  

            print('Done.')
            return True

        else:
            print("Controller is not connected to Merlin firmwware. Attempting to connect now.")
            #TODO: add reconnect here.

        return False


    def end(self):
        pass


class CommandHandler:
    '''
    Contains method for converting moves into commands.
    '''
    def __init__(self):
        self.moveo_interface = MoveoInterface()
        self.platform = CMGameInterface().get_board_manager()


    def create(self, index):
        '''
        Used to create the individual commands for the Merlin system.

        1. Get cartesian coordinates of square number (index) from the platform (chess board).
        2. Use inverse kinematics to determine the required joint rotations.
        3. Convert joint rotations angles to steps.
        '''
        coordinates = self.platform.get_coordinates(index)
        degrees = self.moveo_interface.get_inverse(coordinates[0], coordinates[1], coordinates[2])
        steps = self.moveo_interface.get_steps_from_degrees(degrees[0], degrees[1], degrees[2], 0)
        return steps
