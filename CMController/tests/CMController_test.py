'''
Test
Unit test suite for CMController actions.

March 2, 2020: Need to write accurate unit test cases for the CMController class.
'''
import sys
import unittest
from CMController.cmc import CMController
from CMController.Integrations.cm_integration import CMIntegration
from CMController.CMGame.board import GameBoard, BoardMapping
from CMController.MoveoArm.instruction import InstructionManager, MoveInstruction, BaseInstruction
from CMController.MoveoArm.ik import InverseKinematics
from CMController.MoveoArm.moveo_arm import MoveoArm
from CMController.CMGame.piece import PieceManager
from CMController.CMGame.move import MoveManager
from CMController.CMGame.interface import CMGameInterface

class TestCMController(unittest.TestCase):
    '''
    Methods of CMController:
    - connect() [Not Tested]
    - is_connected() [Not Tested]
    - list_serial_devices() [Not Tested]
    - send_command() [Not Tested]
    '''
    pass



class TestCMMoveo(unittest.TestCase):
    def setUp(self):
        self.cmc_integration = CMIntegration()
        self.game = CMGameInterface()
        self.mm = self.game.get_move_manager()
        self.pm = self.game.get_piece_manager()

    def test_start(self):
        self.cmc_integration.start()

    def test_execute_move(self):
        print("Executing move..")
        self.cmc_integration.start()
        pawn = self.pm.get_pawn()
        move = self.mm.get_move(pawn, 1, 2)
        result = self.cmc_integration.execute_move(move)
        print(result)



if __name__ == '__main__':
    unittest.main()
