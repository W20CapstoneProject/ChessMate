class MoveManager:
    '''
    Store all available commands in one class. Can be instatiated instead of the individual classes for use
    '''
    def get_move(self, piece, start, end):
        return _Move(piece, start, end)

    def get_kill(self, piece, start, end):
        return _Kill(piece, start, end)

    def get_enPassant(self, piece, start, end):
        return _enPassant(piece, start, end)

    def get_castling(self, piece, start, end):
        return _Castling(piece, start, end)

    def get_promotion(self, piece, start, end):
        return _Promotion(piece, start, end)




class _Move:
    '''
    Utilize polymorphism to hand off command creation to move class.

    Must account for the height of the pieces for each move.
    Each move requires a different sequence of commadns to fulfill the move.
    '''
    def __init__(self, piece, start, end):
        self.start = start
        self.end = end
        self.piece = piece

    def create_commands(self, handler):
        # Regular Move: Can be completed with two commands (not including reverse)
        commands = []
        commands.append(handler.create(self.piece, self.start))
        # Todo: intermediary: origin.
        commands.append(handler.create(self.piece, self.end))
        # Todo: intermediary: origin.
        return commands



class _Kill(_Move):
# Kill Move
# Remove piece at end, and move our piece to end
# Can be done in 4 commands
    pass



class _enPassant(_Move):
# enPassant Move
#need more information to determine what pawn to capture
    pass



class _Castling(_Move):
# if square number is increaing from start to end then
# castle kingside, otherwise queenside. The rook will be
# on the right most or left most square of a row.
# Move king first, then rook. 4 commands required.
    pass



class _Promotion(_Move):
# Not sure how this case is handled. Just execute command for now.
    pass

