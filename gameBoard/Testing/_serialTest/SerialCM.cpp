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


void SerialCM::serialCommunication() {
    _incomingByte = Serial.readString();
    Serial.print("ACK");
    handleCommand(_incomingByte);
}

void SerialCM::handleCommand(String command) {
  Serial.print("OK!");
}

void SerialCM::helloWorld() {
  Serial.print("Hello World!");
}

