/*
 * Serial Test for Arduino and Python communication.
 */
 #include "SerialCM.h"

String incomingByte = "";
int baudRate = 9600;
String ACK = "ACK";

SerialCM cm;

void setup() {
  Serial.begin(baudRate);
}


void loop() {
  delay(150);

  if (Serial.available() > 0) {
    delay(150);
    cm.serialCommunication();
  }

}
