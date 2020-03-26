import board
import move 
import piece


class CmGame:
    def __init__(self):
        self.board_manager = board.GameBoard()
        self.move_manager = move.MoveManager()
        self.piece_manager = piece.PieceManager()