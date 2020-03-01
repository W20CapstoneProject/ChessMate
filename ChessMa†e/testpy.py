
import os
import subprocess
from subprocess import call
import chess
import chess.engine

import numpy as np

def initializeChessEngine():
    # os.chdir("/usr/local/Cellar/stockfish/11/bin")
    # os.system("./stockfish")
    # os.system("isready")
    # # Insert error handling
    # os.system("uci")
    # # Insert appropriate options
    # os.system("d")

    # engine = chess.engine.SimpleEngine.popen_uci("/usr/local/Cellar/stockfish/11/bin/stockfish")
    #
    # board = chess.Board()
    #
    # print(board)
    # print('\n')
    #
    # info = engine.analyse(board, chess.engine.Limit(time=0.1))
    #
    # print("info: ", info)
    #
    #
    # board = chess.Board("r1bqkbnr/p1pp1ppp/1pn5/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 2 4")  # Use this to update the game state
    # print(board)
    # info = engine.analyse(board, chess.engine.Limit(depth=20))
    # print("Score:", info["score"])
    # # Score: #+1
    #
    # engine.quit()

    # for i in range(7,-1,-1):
    #     print(i)
    #
    # for j in range(0,8):
    #     print(j)


    masterArduinoTransmission =np.array([['P', 'n', 'b', 'q', 'k', 'b', 'n', 'r'], ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'], ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'], ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'], ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'], ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']])

    value = masterArduinoTransmission[7][4]
    print(value)


def main():
    initializeChessEngine()




if __name__ == '__main__':
    main()
