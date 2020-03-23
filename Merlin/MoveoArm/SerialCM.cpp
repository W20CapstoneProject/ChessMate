#include "Arduino.h"
#include "SerialCM.h"

String _ACK;
String _incomingByte;


SerialCM::SerialCM(){
  init();
}

SerialCM::~SerialCM(){}

void SerialCM::init() {
  _ACK = "ACK";
  _incomingByte = "";
}

/*
  serialCommunication()
  Use to begin serial communication with the connected computer.
*/
void SerialCM::serialCommunication() {
    _incomingByte = Serial.readString();
    Serial.print("ACK");
    handleCommand(_incomingByte);
}


/*
  handleCommand()
  The main handler for the command. Will execute the command on the Merlin/gameboard.
*/
void SerialCM::handleCommand(String command) {
  Serial.print("OK!");
}
