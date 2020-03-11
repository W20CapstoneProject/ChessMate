from board import GameBoard
from cm import CMController

board = GameBoard()
cm = CMController()

class Move:
    '''
    Utilize polymorphism to hand off command creation to move class.
    '''
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def get_commands(self, handler):
        # Regular Move: Can be completed with two commands (not including reverse)
        commands = []
        commands.append(handler.create_command(self.start))
        commands.append(handler.create_command(self.end))
        return commands



class Kill(Move):
# Kill Move
# Remove piece at end, and move our piece to end
# Can be done in 4 commands
    def get_commands(self, handler):
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
    def get_commands(self, handler):
        pass


class Promotion(Move):
# Not sure how this case is handled. Just execute command for now.
    def get_commands(self, handler):
        pass
