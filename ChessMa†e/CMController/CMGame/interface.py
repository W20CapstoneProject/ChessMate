from .board import GameBoard
from .move import MoveManager
from .piece import PieceManager


class CMGameInterface:

    def get_board_manager(self):
        return GameBoard()

    def get_move_manager(self):
        return MoveManager()

    def get_piece_manager(self):
        return PieceManager()