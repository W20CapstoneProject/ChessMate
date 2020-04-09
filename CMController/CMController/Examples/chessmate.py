from CMController.Integrations.cm_integration import CMIntegration
from CMController.MoveoArm.instruction import MerlinInstruction
from CMController.cmc import CMController
from CMController.MoveoArm.ik import InverseKinematics, IKMapping
from CMController.MoveoArm.moveo_arm import MoveoArm
from CMController.MoveoArm.interface import MoveoInterface
from numpy import radians, degrees
import time


def chessmate_integration_example():
    '''
    Demo of ChessMate and Merlin integration methods. 
    This program cycles through a moves list from 1 to 64 moving the pawn one square number higher with each iteration.
    '''
    cmi = CMIntegration()
    response = cmi.start()
    print(response)
    piece_manager = cmi.game.get_piece_manager()
    move_manager = cmi.game.get_move_manager()

    piece = piece_manager.get_pawn()
    cmi.test()
    for index in range(1, 64):
        print("Moving pawn from " + str(index) + " to " + str(index+1))
        move = move_manager.get_move(piece, index, index+1)
        response = cmi.execute_move(move)
        print(str(response) + "\n")

    cmi.end()


def video_calculations():
    cmi = CMIntegration()
    response = cmi.start()
    print(response)
    piece_manager = cmi.game.get_piece_manager()
    move_manager = cmi.game.get_move_manager()

    pawn = piece_manager.get_pawn()
    knight = piece_manager.get_knight()
    i_setup = "0,0,0,0,180"
    
    # Pawn Move -> 12 to 28
    print("Moving pawn from " + str(12) + " to " + str(28))
    move1 = move_manager.get_move(pawn, 12, 28)
    response = cmi.execute_move(move1)
    print(str(response) + "\n")
    # Knight Move -> 2 to 19
    print("Moving knight from " + str(2) + " to " + str(19))
    move2 = move_manager.get_move(knight, 2, 19)
    response = cmi.execute_move(move2)


def video_demo():
    #Video Demonstration of ChessMate arm
    i_setup = "0,0,0,0,180"
    i1 = "-84.0,35.0,2250.0,-422.0,0"
    i2 = "-56.0,239.0,1114.0,-490.0,180"
    i3 = "-468.0,-63.0,2521.0,-449.0,0"
    i4 = "-196.0,128.0,1680.0,-465.0,0"

    cmc = CMController()
    cmc.connect()
    if(cmc.is_connected()):
        cmc.send_command("0,0,0,0,0")
        cmc.send_command(i_setup)
        cmc.send_command(i1)
        cmc.send_command("-84.0, -300, 1500, -600, 0")
        cmc.send_command(i2)
        cmc.send_command(i_setup)
        time.sleep(5)


 

if __name__ == "__main__":
    #chessmate_integration_example()
    #video_calculations()
    video_demo()