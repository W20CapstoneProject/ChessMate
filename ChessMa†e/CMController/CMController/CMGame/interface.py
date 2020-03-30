from CMController.CMGame.board import GameBoard
from CMController.CMGame.move import MoveManager
from CMController.CMGame.piece import PieceManager


class CMGameInterface:

    def get_board_manager(self):
        return GameBoard()

    def get_move_manager(self):
        return MoveManager()

    def get_piece_manager(self):
        return PieceManager()