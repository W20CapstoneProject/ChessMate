class PieceManager:
    # Manager used for all available pieces to the game.
    def __init__(self):
        self.king = KingPiece()
        self.queen = QueenPiece()
        self.rook = RookPiece()
        self.bishop = BishopPiece()
        self.knight = KnightPiece()
        self.pawn = PawnPiece()


class ChessPiece:
    # Used to track height of pieces. Potetentially other characteristics such as grip strength.
    def __init__(self, height):
        self.height = height

class KingPiece(ChessPiece):
    # King Piece Dimensions
    def __init__(self):
        super().__init__(height = 104.902)

class QueenPiece(ChessPiece):
    # Queen Piece Dimensions
    def __init__(self):
        super().__init__(height = 82.55)

class RookPiece(ChessPiece):
     # Rook Piece Dimensions
    def __init__(self):
        super().__init__(height = 63.5)

class BishopPiece(ChessPiece):
    # Bishop Piece Dimensions
    def __init__(self):
        super().__init__(height = 76.2)

class KnightPiece(ChessPiece):
    # Knight Piece Dimensions
    def __init__(self):
        super().__init__(height = 69.85)

class PawnPiece(ChessPiece):
    # Pawn Piece Dimensions
    def __init__(self):
        super().__init__(height = 50.8)