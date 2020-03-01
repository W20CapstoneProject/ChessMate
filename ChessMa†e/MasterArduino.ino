
// can delay this way: delay(1000);


// PIN Numbers

#define GREEN_LED 2
#define RED_LED 4

//Button

#define PUSH_BUTTON 1

void setup() {
  Serial.begin(115200); // use the same baud-rate as the python side
  while (!Serial); {
  }
  SPI.begin();


  pinMode(GREEN_LED, OUTPUT);
  digitalWrite(GREEN_LED, LOW);

  pinMode(RED_LED, OUTPUT);
  digitalWrite(RED_LED, LOW);

  pinMode(PUSH_BUTTON, INPUT);
}

bool awaitTransmissionRequest(){

  bool request = false;

  while(request == false){
    if(Serial.available() > 0) {
      char dataByte = Serial.read();
      char requestCode[2];
      requestCode[0] = dataByte;
      data[1] = '\0';

      // if (data[0] == 'REQ'){
      // //send ACK
      // Serial.println("ACK");
      request = true
      }

   }

  }
  return requestCode
  }

// void determineMFRC522ModuleBySS() {
////    for (int i = 0; i < 2; i++) {
//    Serial.println(MFRC522.SS);
//
// }

bool waitForButtonPress(){

   press = false;
   while(press == false){
    //Find out how to read a button using Arduino
    press = true;
   }
   return true;
}

char scanBoard(perspective){
  char state[];
  if(perspective == '1'){
    //scan board squares from 0 to 63
    else:
    //scan board squares from 63 down to 0
  }
  return state
}

int transmitPhysicalBoardState(){
  return 0;
}

void loop() {

  buttonPress = false
  request = false

  requestCode = awaitTransmissionRequest()

  //Parse the requestCode to determine'perspective' and 'turn'; U ==> Users turn, E ==> engine/arms turn, WHITE = 1; BLACK = 0)
  // If E, then RED_LED should remain on.

  if (request == true){
    digitalWrite(GREEN_LED, HIGH);
    digitalWrite(RED_LED, LOW);
    //WAIT FOR BUTTON PRESS
    // buttonPress = waitForButtonPress();
    if(buttonPress == true){
      digitalWrite(GREEN_LED, LOW);
      digitalWrite(RED_LED, HIGH);
      //Scan board and transmit...
      //state = scanboard(perspective);
      //ack = transmitPhysicalBoardState(state);
      // Deal with error handling..
      Serial.println("BOARD STATE TRANSMISSION");

  }
}
