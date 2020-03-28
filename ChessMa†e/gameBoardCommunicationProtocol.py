
################################################################################
#                                                                              #
# Author: DMD, 2020                                                            #
#                                                                              #
#                                                                              #
# N.B. - This program can be tested in conjunction with testComm.ino
#        'Process' was used primarily for it's handy timeout functionality.
#                                                                              #
################################################################################


#Attributions:
#Referenced source code:  //https://www.instructables.com/id/Arduino-and-Python/

import serial
import time
import multiprocessing
from multiprocessing import Process
import numpy as np

transmissionArray = None
turn = None
priorTransmissionResult = None
serGameBoard = None


def requestPhysicalBoardState():

    global serGameBoard

    # ser = serial.Serial("/dev/cu.usbmodem1421", 9600)
    global turn
    # global priorTransmissionResult
    #
    # if priorTransmissionResult == '-1': # ==> Incomplete transmission
    #     print("priorTransmissionResult == '-1'\n")
    #     ser.write(priorTransmissionResult.encode())
    #     priorTransmissionResult = 1

    print("Inside requestPhysicalBoardState...\n")

    connected = False

    print('connected: \n', connected)

    while not connected:
        connected = serGameBoard.read().decode()
        # connected = True, '1' received

    print('connected2: \n', connected)

    print("turn: \n", turn)


    if turn == 'User':
        command = 'R'
    else:
        command = 'r'

    # R ==> user; r ==> robot

    # command = 'R'

    print("command: \n", command)

    serGameBoard.write(command.encode())

    response = "1"
    while response != "ACK":
        response = serGameBoard.read(3).decode()

    print("response: \n", response)
    print()



def receiveTransmission():

    global serGameBoard
    global turn
    global priorTransmissionResult

    # If it's the User's turn, the ChessMate Game Board will wait for a button press before harvesting the board state and indicating readyness to transmitt.
    # If it's the robot's turn, instructions should have already been sent to the arm to make the move - wait on confirmation that it has been completed.

    if turn == "robot" and priorTransmissionResult != "-1":
    #     robotMoveCompleted = false
    #     while not robotMoveCompleted:
    #         robotMoveCompleted = CM_controllerConfirmation()  //something like this.  Hold until confirmation essentially.
        completed = 'c'
        serGameBoard.write(completed.encode())
        print("arm move is completed: \n")
        print(completed)



    if priorTransmissionResult == "-1": # ==> Incomplete transmission
        print("priorTransmissionResult == '-1'\n")
        serGameBoard.write(priorTransmissionResult.encode())
        priorTransmissionResult = 1



    readyToTransmit = False

    while readyToTransmit != "1":
        readyToTransmit = serGameBoard.read(1).decode()

    # print("The arduino is ready to transmit...")

    transmission = serGameBoard.read(64).decode()

    # print("Transmission recieved")

    confirmReceipt = "1"

    serGameBoard.write(confirmReceipt.encode()) # Completed transaction

    print(transmission)





def generateRequestProcess_generateReceiveTransmissionProcess():

    global priorTransmissionResult

    print("in generateRequestProcess...\n")
    print("priorTransmissionResult: \n", priorTransmissionResult)

    print("turn: \n", turn)

    maxNumberOfAttemptsAllowable = 3
    currentAttemptNumber = 1
    exitCode = 1
    timeOut = 2 #[s]  ==> time-out for establishing a connection and making a request based on either a User turn, or a robot turn.

    while ((currentAttemptNumber <= maxNumberOfAttemptsAllowable) and exitCode != 0):

        makeRequest = Process(target = requestPhysicalBoardState)

        print('currentAttemptNumber: \n', currentAttemptNumber)

        startTime = time.time()
        print('startTime: \n', startTime)

        makeRequest.start()
        makeRequest.join(timeout = timeOut)
        makeRequest.terminate()

        finishTime = time.time()
        # print('FinishTime: \n', finishTime)
        elapsedTime = finishTime - startTime
        print("elapsedTime: \n", elapsedTime)

        exitCode = makeRequest.exitcode
        print("exitCode: ", exitCode)

        if exitCode is None:
            currentAttemptNumber = currentAttemptNumber + 1
            timeOut = timeOut*1.2
            if currentAttemptNumber == 4:
                userAction = input("Please check the USB connections and press ENTER when you are ready to resume.")
                currentAttemptNumber = 1  #Reset


    currentAttemptNumber = 1
    exitCode = 1
    timeOut = 3600 #[s]  ==> Time-out to receive the actual board state transmission. CHANGE THIS TO userTimeOut -- set upon initialization via user input

    while ((currentAttemptNumber <= maxNumberOfAttemptsAllowable) and exitCode != 0):

        awaitTransmission = Process(target = receiveTransmission)

        print('currentAttemptNumber: \n', currentAttemptNumber)

        startTime = time.time()
        print('startTime: \n', startTime)

        awaitTransmission.start()
        awaitTransmission.join(timeout = timeOut)
        awaitTransmission.terminate()

        finishTime = time.time()
        # print('FinishTime: \n', finishTime)
        elapsedTime = finishTime - startTime
        print("elapsedTime: \n", elapsedTime)

        exitCode = awaitTransmission.exitcode
        print("exitCode: ", exitCode)

        if transmissionArray is None:  # ==> Timeout prior to any transmission received

            if exitCode is None:
                currentAttemptNumber = currentAttemptNumber + 1
                timeOut = timeOut*1.2
                if currentAttemptNumber == 4:
                    userAction = input("Please ensure that the game pieces are centered on each of their respective game squares and press ENTER when you are ready to resume gameplay.")
                    currentAttemptNumber = 1 # Reset
            if exitCode == 1: #==> Could not open port (err [2])
                userAction = input("Please ensure that the USB cables are connected; press ENTER when you are ready to resume.")

        else:  # A partial transmission was recieved prior to the time-out.
            priorTransmissionResult = '-1'



    # print('exitcode: \n', exitcode)





if __name__ == '__main__':

    serGameBoard = serial.Serial("/dev/cu.usbmodem1421", 9600)

    turn = 'robot'

    generateRequestProcess_generateReceiveTransmissionProcess()
