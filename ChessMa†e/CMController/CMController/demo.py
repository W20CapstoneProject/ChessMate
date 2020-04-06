from CMController.cm_integration import CMIntegration
from CMController.MoveoArm.instruction import MerlinInstruction

def demo1():
    '''
    Demo of ChessMate and Merlin integration methods. 
    This program cycles through a moves list from 1 to 64 moving the pawn one square number higher with each iteration.
    '''
    cmi = CMIntegration()
    response = cmi.start()
    print(response)
    piece_manager = cmi.game.get_piece_manager()
    move_manager = cmi.game.get_move_manager()

    pawn = piece_manager.get_pawn()
    cmi.test()
    for index in range(1, 64):
        print("Moving pawn from " + str(index) + " to " + str(index+1))
        move = move_manager.get_move(pawn, index, index+1)
        response = cmi.execute_move(move)
        print(str(response) + "\n")

    cmi.end()

def demo2():
    manager = MerlinInstruction()
    cmd = manager.create(12, 200, 3432, 43, 325)
    print(cmd)

if __name__ == "__main__":
    demo1()