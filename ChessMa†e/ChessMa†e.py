
#*******************************************************************************
#*                                                                             *
#*                                  ChessMa†e                                  *
#*                                 –––––––––––                                 *
#* Damian Douziech                                                             *
#* Feb. 1, 2020                                                                *
#*                                                                             *
#* Abstract:
#*
#*
#*
#*
#*
#*
#*******************************************************************************


#  ATTRIBUTIONS
#  Code excerpts taken from:
#  [1] https://python-chess.readthedocs.io/en/latest/
#  [2] https://stackoverflow.com/questions/4760215/running-shell-command-and-capturing-the-output

import chess
import chess.engine

import subprocess
from subprocess import call
# import constants
import io
import sys

import numpy as np
import time

import communication



WHITE = True
BLACK = False

FEN_userWhite = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"  # The default, initial board-state FEN
FEN_userBlack = "RNBQKBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbqkbnr"  # Non-standard, board-state FEN - only suitable to this program for initially determining the user's colour

boardSetUpError = -1




def receiveMasterArduinoTransmission():
    # masterArduinoTransmission : a 2 dimensional array (8x8) consisting of game pieces or empty squares,
    # encoded in alignment with FEN notation ('P','R','N','B','K, 'Q', 'p', 'r', 'n', 'b', 'k', 'q'). Empty squares are designated with 'e'.

    # Insert handshake protocol between ChessMa†e and the MasterArduino
    print('Ok')
    return 0

def generatePhysicalBoardStateDictionary(transmissionArray_2D):

    physicalBoardStateDictionary = {}

    index = 0
    for number in range(7,-1,-1):
        for letter in range(0,8):
            key = str(index)
            value = str(transmissionArray_2D[number][letter])
            physicalBoardStateDictionary[key] = value
            index = index+1

    return physicalBoardStateDictionary

def findLastMove(currentStateDictionary, previousStateDictionary):
    difference_currentMinusPrevious = list(currentStateDictionary.items() - previousStateDictionary.items())
    difference_previousMinusCurrent = list(previousStateDictionary.items() - currentStateDictionary.items())

    if difference_currentMinusPrevious[0][1] == 'e':
        fromLocation = int(difference_currentMinusPrevious[0][0])
        toLocation = int(difference_currentMinusPrevious[1][0])
    else:
        fromLocation = int(difference_currentMinusPrevious[1][0])
        toLocation = int(difference_currentMinusPrevious[0][0])

    print('fromLocation: \n', fromLocation)
    print('toLocation: \n', toLocation)

    calculatedMove = chess.Move(fromLocation, toLocation, None,  None)
    print('calculatedMove: \n', calculatedMove)

    # last = l[0] # Provides for indexing capability by converting from a set to list
    # lastMove = last[0]+previousStateDictionary.get(str(last[0]))+last[0]+last[1]

    return calculatedMove

def getCurrentState_fen():
    output = subprocess.getoutput("")  # Attribution [2]

class gameBoard:
     def __init__(self, currentStateFEN, previousStateFEN, timeLastMove):
        self.currentStateFEN = currentStateFEN  # string
        self.previousStateFEN = previousStateFEN # string
        self.timeLastMove = timeLastMove  # The time at which the most recent move was registered

# class gamePiece:  #Probably don't need this (chess.piece instead)
#     def _init_(self, pieceType, colour, startingLocation, previousLocation, currentLocation):
#         self.pieceType = pieceType
#         self.colour =  colour
#         self.startingLocation = startingLocation
#         self.previousLocation = previousLocation
#         self.currentLocation  = currentLocation

def requestPhysicalBoardState():

    masterArduinoTransmission = receiveMasterArduinoTransmission()

    # currentStateDictionary = generatePhysicalBoardStateDictionary(MasterArduinoTransmission)

    return masterArduinoTransmission, currentStateDictionary

def initializeChessEngine():
    # Reference [1]

    # # call("pwd")
    # # call("cd /usr/local/Cellar/stockfish/11/bin")
    #
    # os.chdir("/usr/local/Cellar/stockfish/11/bin")
    # call("./stockfish")
    # call("isready")
    # # Insert error handling
    # call("uci")
    # # Insert appropriate options
    # call("d")

    engine = chess.engine.SimpleEngine.popen_uci("/usr/local/Cellar/stockfish/11/bin/stockfish")  # Insert the appropriate directory as required.

    engineGameBoard = chess.Board()

    # print('\n')
    # print(gameBoard)
    # print('\n')

    return engineGameBoard, engine

def awaitingTransmissionRequest():
    print('Awaiting transmission request from the MasterArduino...')


def convertPhysicalBoardStateToFEN(masterArduinoTransmission):  #For 2D array format
    with io.StringIO() as FEN:
        for letter in range(8):
            empty = 0
            for number in range(8):
                current = masterArduinoTransmission[letter][number]
                # FEN.write(masterArduinoTransmission[letter][number])
                if empty > 0:
                    if current == 'e':
                        empty = empty + 1
                        if empty == 8:
                            FEN.write(str(empty))
                        # print('empty: \n', empty)
                    else:
                        # print('here')
                        FEN.write(str(empty))
                        FEN.write(current)
                        empty = 0
                else:
                    if current == 'e':
                        empty = empty + 1
                    else:
                        FEN.write(current)
            FEN.write('/')
        # FEN.seek(FEN.tell() - 1)
        physicalBoardStateFEN = FEN.getvalue()
        physicalBoardStateFEN = str(physicalBoardStateFEN[0:-1])  #Drop the last backslash
        return physicalBoardStateFEN


def confirmInitialBoardState_establishColour(FEN):


    print('FEN: \n', FEN)
    print('FEN_userWhite: \n', FEN_userWhite)

    if FEN == FEN_userWhite:
        userColour = WHITE

    elif FEN == FEN_userBlack:
        userColour = BLACK

    else:
        userColour = boardSetUpError

    return userColour

def userMode(engine, engineGameBoard, currentPhysicalStateDictionary, perspective):

    print('In userMode...')

    #ack = requestTransmission()
    #transmission = recieveTransmission()  (==> button pressed by user)

    transmissionArray_2D_sampleMove =np.array([['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'], ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'], ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'], ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'], ['P', 'e', 'e', 'e', 'e', 'e', 'e', 'e'], ['e', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']])

    previousPhysicalStateDictionary = currentPhysicalStateDictionary
    currentPhysicalStateDictionary = generatePhysicalBoardStateDictionary(transmissionArray_2D_sampleMove)

    userMove = findLastMove(currentPhysicalStateDictionary, previousPhysicalStateDictionary)

    #Check move for validity
    legalMoves = engineGameBoard.legal_moves

    if userMove in engineGameBoard.legal_moves:
         print('\nLegal move\n')

         print('\nCurrent engineGameBoard: \n')
         print(engineGameBoard)

         previousGameStateFEN = engineGameBoard.fen() #Store the previous gameState

         #Register the move
         move = chess.Move.from_uci(str(userMove))
         engineGameBoard.push(move)
         print('\nThe engineGameBoard has now been updated and matches the physical game board: \n')
         print("Updated engineGameboard: \n")
         print(engineGameBoard)
         print()

         print("engineGameBoard.fen(): \n", engineGameBoard.fen())
         print()

         #DECLARE IF THE COMPUTER HAPPENS TO BE IN CHECK
         if engineGameBoard.is_check():
             print("The black king is in check!")

         turn = BLACK

    else:
        print('Illegal move! Please adjust your move and press the button again.')
        userMode(engine, engineGameBoard, currentPhysicalStateDictionary)


    return turn, engine, engineGameBoard, currentPhysicalStateDictionary, previousGameStateFEN


def robotMode(engine, engineGameBoard, currentPhysicalStateDictionary, perspective, searchTime):

    print('In robotMode...')

    requestCode = "RE"+str(perspective)

    engineMove = engine.play(engineGameBoard, chess.engine.Limit(time=searchTime))  #The engine has half of a second to determine its next move.


    print('\nA legal move has been generated...\n')

    print('\nCurrent engineGameBoard: \n')
    print(engineGameBoard)

    # engine/arm executes the move...
    # confirmation = CM_controller(engineMove)  # CM_controller --> Merlin --> Arm; Merlin --> CM_controller --> chessMa†e
    # Error handling should be delineated within the CM_controller.

    # acknowledgment = requestTransmission(requestCode)
    # transmission = recieveTransmission()

    #Autogenerated transmission for testing purposes...
    # transmission =

    previousPhysicalStateDictionary = currentPhysicalStateDictionary
    currentPhysicalStateDictionary = generatePhysicalBoardStateDictionary(transmissionArray_2D_sampleMove)

    userMove = findLastMove(currentPhysicalStateDictionary, previousPhysicalStateDictionary)



    previousGameStateFEN = engineGameBoard.fen() #Store the previous gameState

    engineGameBoard.push(engineMove.move)

    turn = WHITE

    return turn, engine, engineGameBoard, currentPhysicalStateDictionary, previousGameStateFEN


def battleMode(engine, engineGameBoard, currentPhysicalStateDictionary, turn, perspective, searchTime):

    while not engineGameBoard.is_game_over():

        if turn == WHITE:
            turn, engine, engineGameBoard, currentPhysicalStateDictionary, previousGameStateFEN = userMode(engine, engineGameBoard, currentPhysicalStateDictionary, perspective)

        else:
            turn, engine, engineGameBoard, currentPhysicalStateDictionary, previousGameStateFEN = robotMode(engine, engineGameBoard, currentPhysicalStateDictionary, perspective, searchTime)

    #Determine the winner
    winner = WHITE


    return winner

# def fenToboardState(FEN):
#
#
# 





def main():

    requestCode = 'R'
    turn = WHITE  # WHITE must make the first move.

    # Sample masterArduinoTransmission (Default initial gameboard, user = WHITE)
    masterArduinoTransmission =np.array([['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'], ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'], ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'], ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'], ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'], ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']])
    # Transmission will be in 1D format

    #For testing the function convertPhysicalBoardStateToPhysicalBoardStateFENS
    # masterArduinoTransmission =np.array([['r', 'e', 'b', 'q', 'k', 'e', 'e', 'r'], ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'], ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'], ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'], ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'], ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], ['e', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']])

    masterArduinoTransmission_sampleMove =np.array([['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'], ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'], ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'], ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'], ['P', 'e', 'e', 'e', 'e', 'e', 'e', 'e'], ['e', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']])


    print('\n')
    print('masterArduinoTransmission: \n', masterArduinoTransmission)
    print('\n')

    transmissionArray_1D = masterArduinoTransmission.flatten()
    transmissionArray_2D = np.reshape(transmissionArray_1D,(-1,8))

    print('transmissionArray_1D: \n', transmissionArray_1D)

    print('\n')
    print('transmissionArray_2D: \n')
    print(transmissionArray_2D)

    engineGameBoard, engine = initializeChessEngine() # Todo: Implement default options

    searchTime = 0.5 # ==> The engine will have just half of a second to determine its next move.

    print('\n')
    print('Initial engineGameboard: ')
    print(engineGameBoard)
    print('\n')

    print("Initial game state FEN: \n", engineGameBoard.fen())


    print('\n')
    print('masterArduinoTransmission_sampleMove: \n', masterArduinoTransmission_sampleMove)
    print('\n')

    awaitingTransmission = True

    while awaitingTransmission == True:

        # acknowledgment = requestTransmission(requestCode)
        acknowledgment = True  # TEMPORARY

        if acknowledgment == True:
            #transmission = receiveTransmission()
            physicalBoardStateFEN = convertPhysicalBoardStateToFEN(transmissionArray_2D)
            print('boardStateFEN: \n', physicalBoardStateFEN)
            print('\n')
            userColour = confirmInitialBoardState_establishColour(physicalBoardStateFEN) # Check to see if the initial setup is correct  (2 cases, due to colour selection)
            print('userColour: \n', userColour)

            if type(userColour) != bool:
                print('\nThe board has been incorrectly set up; please adjust it and press the button when ready.\n')
            else:
                awaitingTransmission = False


    currentGameStateFEN = chess.STARTING_FEN

    currentPhysicalStateDictionary = generatePhysicalBoardStateDictionary(transmissionArray_2D)

    print('\n')
    print('currentPhysicalStateDictionary[4]: \n', currentPhysicalStateDictionary['4'])

    if userColour == True:
        perspective = True  # ==> The masterArduino will scan the game board from the user's perspective.

    if userColour == False:
        perspective = False  # ==> The arm is white; the masterArduino will scan the board from the arms perspective, to conform with FEN notation.

    winner = battleMode(engine, engineGameBoard, currentPhysicalStateDictionary, turn, perspective, searchTime)

    print("The winner is: ", winer)

    engine.quit()


if __name__ == '__main__':
    main()
