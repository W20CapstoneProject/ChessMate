class PieceManager:
    # Manager used for all available pieces to the game.
    def get_king(self):
        return _KingPiece()

    def get_queen(self):
        return _QueenPiece()

    def get_rook(self):
        return _RookPiece()

    def get_bishop(self):
        return _BishopPiece()

    def get_knight(self):
        return _KnightPiece()

    def get_pawn(self):
        return _PawnPiece()

class _ChessPiece:
    # Used to track height of pieces. Potetentially other characteristics such as grip strength.
    def __init__(self, height):
        self.height = height

class _KingPiece(_ChessPiece):
    # King Piece Dimensions
    def __init__(self):
        super().__init__(height = 104.902)

class _QueenPiece(_ChessPiece):
    # Queen Piece Dimensions
    def __init__(self):
        super().__init__(height = 82.55)

class _RookPiece(_ChessPiece):
     # Rook Piece Dimensions
    def __init__(self):
        super().__init__(height = 63.5)

class _BishopPiece(_ChessPiece):
    # Bishop Piece Dimensions
    def __init__(self):
        super().__init__(height = 76.2)

class _KnightPiece(_ChessPiece):
    # Knight Piece Dimensions
    def __init__(self):
        super().__init__(height = 69.85)

class _PawnPiece(_ChessPiece):
    # Pawn Piece Dimensions
    def __init__(self):
        super().__init__(height = 50.8)