class MoveManager:
    '''
    Store all available commands in one class. Can be instatiated instead of the individual classes for use
    '''
    def __init__(self):
        self.move = Move()
        self.kill = Kill()
        self.enPassant = enPassant()
        self.castling = Castling()
        self.promotion = Promotion()


class Move:
    '''
    Utilize polymorphism to hand off command creation to move class.

    Must account for the height of the pieces for each move.
    Each move requires a different sequence of commadns to fulfill the move.
    '''
    def __init__(self, piece, start, end):
        self.start = start
        self.end = end
        self.piece = piece

    def get_commands(self, handler):
        # Regular Move: Can be completed with two commands (not including reverse)
        commands = []
        commands.append(handler(self.start))
        # Todo: intermediary: origin.
        commands.append(handler(self.end))
        # Todo: intermediary: origin.
        return commands



class Kill(Move):
# Kill Move
# Remove piece at end, and move our piece to end
# Can be done in 4 commands
    pass



class enPassant(Move):
# enPassant Move
#need more information to determine what pawn to capture
    pass



class Castling(Move):
# if square number is increaing from start to end then
# castle kingside, otherwise queenside. The rook will be
# on the right most or left most square of a row.
# Move king first, then rook. 4 commands required.
    pass



class Promotion(Move):
# Not sure how this case is handled. Just execute command for now.
    pass

