class PieceManager:
    # Manager used for all available pieces to the game.
    def get_king(self):
        return King()

    def get_queen(self):
        return Queen()

    def get_rook(self):
        return Rook()

    def get_bishop(self):
        return Bishop()

    def get_knight(self):
        return Knight()

    def get_pawn(self):
        return Pawn()

class _ChessPiece:
    # Used to track height of pieces. Potetentially other characteristics such as grip strength.
    def __init__(self, height):
        self.height = height

    def get_height(self):
        return self.height

class King(_ChessPiece):
    # King Piece Dimensions
    def __init__(self):
        super().__init__(height = 104.902)

class Queen(_ChessPiece):
    # Queen Piece Dimensions
    def __init__(self):
        super().__init__(height = 82.55)

class Rook(_ChessPiece):
     # Rook Piece Dimensions
    def __init__(self):
        super().__init__(height = 63.5)

class Bishop(_ChessPiece):
    # Bishop Piece Dimensions
    def __init__(self):
        super().__init__(height = 76.2)

class Knight(_ChessPiece):
    # Knight Piece Dimensions
    def __init__(self):
        super().__init__(height = 69.85)

class Pawn(_ChessPiece):
    # Pawn Piece Dimensions
    def __init__(self):
        super().__init__(height = 50.8)