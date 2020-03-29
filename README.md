# ChessMate

ChessMate is a student Capstone project from the University of Alberta. Our objective was to design and create an open source based program that would enable a robotic arm to compete in a game of chess.

### ChessMate
Python program that allows a game of Chess to be played between the 3D BCN Moveo Arm and a human user. 

### Merlin
Firmware for the 3D BCN Moveo Arm. Utilizes an Arduino Mega 2560. 

### CMController
CMController was created for use with our own custom Merlin firmware for control of the 3D BCN Moveo Arm. 
It enables serial communication with Merlin to send instructions based on cartesian coordinates. The CMController is also used by the ChessMate program for it's integration with Merlin. Contains a combination of commands to enable ChessMate to play a game of chess with the 3D Moveo Arm.

### gameBoard
Arduino code for running the RFID chess board. Polls and collects RFID information from the game board to determine the current status of the game. 


