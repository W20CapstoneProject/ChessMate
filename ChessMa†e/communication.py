

#Some code excerpts from https://www.instructables.com/id/Arduino-Python-Communication-via-USB/

import serial
import time

# arduino = serial.Serial('COM1', 115200, timeout=.1)


def receiveTransmission():

    # arduino = serial.Serial('COM1', 115200, timeout=.1)


    while True:  #while arduino.readline()
        transmission = arduino.readline()[:-2] #the last bit gets rid of the new-line chars
        if transmission:
            print(transmission)

    return transmission


def requestTransmission(requestCode):
    #Need to differentiate between a transmission request following a User move, or the engine/arm.
    # Possible formatting for the requestCode: <RU#> OR  < RE#> where: U represents that the user has made a move, E represents that the engine/arm has taken its turn;
    # # is either 1 for WHITEs perspective or 2 for BLACKs perspective.

    # arduino = serial.Serial('COM1', 115200, timeout=.1)


    acknowledgment = False


    # while acknowledgment == False:
    arduino.write(requestCode)
    time.sleep(0.2)

    response = arduino.readline()

	# if response == 'ACK':
    #     # acknowledgment = True
    #     print response.rstrip('\n') #strip out the new lines for now
	# 	# (better to do .read() in the long run for this reason

    # return acknowledgment
    return response
