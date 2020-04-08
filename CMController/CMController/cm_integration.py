from CMController.cmc import CMController 
from CMController.CMGame.interface import CMGameInterface
from CMController.MoveoArm.interface import MoveoInterface


class CMIntegration:
    '''
    This class serves as the ChessMate software and Moveo/Merlin integration program. It contains the three methods required for communication
    between the two.

    On startup, ChessMate calls start() to connect to the Moveo arm via serial comms.

    When ChessMate needs to send a move to the Moveo it will call execute_move(). This will take in 
    one Move class as an argument. The function will then create a command for the arm based off of this move.

    When the game is over ChessMate will call end() as a destructor for this class.
    '''
    success_code = "OK!"
    ack_code = "ACK"

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
        March 2, 2020: Needs to be implemented still.
        '''
        is_alive = self.cmc.is_connected()

        if (is_alive == True):
            cmds = move.create_commands(self.command_handler)
            cmds_are_allowed = self.moveo_interface.is_within_constraints(cmds)
            if (cmds_are_allowed is True):
                for cmd in cmds:
                    serialized = self.moveo_interface.serialize_command(cmd)
                    print("\nSerialized instructions: " + str(serialized))
                    #response = self.cmc.send_command(serialized)
                    '''
                    print(response)
                    if (response == self.success_code):
                        self.cmd_history.append(cmd)
                        print(' ')
                    else: 
                       
                        raise Exception ("Communication Error", "Merlin failed to execute command")  
                    '''
                print('Done.')
                return True
            else:
                print("Command sequence does not fit within constraints.")

        else:
            print("Controller is not connected to Merlin firmwware. Attempting to connect now.")
            #TODO: add reconnect here.

        return False


    def end(self):
        print('Completed')


class CommandHandler:
    '''
    Contains method for converting moves into step commands.
    '''
    def __init__(self):
        self.moveo_interface = MoveoInterface()
        self.platform = CMGameInterface().get_board_manager()


    def create(self, piece, square_index):
        '''
        Used to create the individual commands for the Merlin system.
        Calculating steps requires:
            1. Get cartesian coordinates of square number (index) from the platform (chess board).
            2. Use inverse kinematics to determine the required joint rotations.
            3. Convert joint rotations angles to steps.
        '''
        coord = self.platform.get_coordinates(square_index, piece)
        base, shoulder, elbow, wrist, grip = self.moveo_interface.get_degrees_from_coordinates(coord[0], coord[1], coord[2])
        steps = self.moveo_interface.get_steps_from_degrees(base, shoulder, elbow, wrist, grip)
        print("Coordinates: " + str(coord))
        print("Degrees (base, shoulder, elbow, wrist): " + str((base, shoulder, elbow, wrist, grip)))
        print("Steps: " + str(steps))
        return steps
