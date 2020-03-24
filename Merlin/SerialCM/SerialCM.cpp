#include "Arduino.h"
#include "SerialCM.h"

String ACK;
String incomingByte;


SerialCM::SerialCM(){
  init();
}

SerialCM::~SerialCM(){}

void SerialCM::init() {
  ACK = "ACK";
  incomingByte = "";
}

/*
  serialCommunication()
  Use to begin serial communication with the connected computer.
*/
void SerialCM::serialCommunication() {
    incomingByte = Serial.readString();
    Serial.print("ACK");
    handleCommand(incomingByte);
}


/*
  handleCommand()
  The main handler for the command. Will execute the command on the Merlin/gameboard.
*/
void SerialCM::handleCommand(String command) {
  Serial.print("OK!");
}
