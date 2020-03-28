
// Attributions:
// Excerpt taken from: https://os.mbed.com/questions/53962/How-do-I-copy-the-contents-of-a-byte-arr/





#include <SPI.h>
#include <stdio.h>
#include <string.h>
#include <Stream.h>



// Variables will change:
int buttonState;             // the current reading from the input pin
int lastButtonState = LOW;   // the previous reading from the input pin

// the following variables are unsigned longs because the time, measured in
// milliseconds, will quickly become a bigger number than can be stored in an int.
unsigned long lastDebounceTime = 0;  // the last time the output pin was toggled
unsigned long debounceDelay = 50;    // the debounce time; increase if the output flickers





#define GREEN_LED 34
#define RED_LED 35

//Button

#define PUSH_BUTTON 36  


int scanButton(); 
int transmitBoardState();
bool awaitTransmissionRequest_transmitBoardState();

void setup() { //For testing this module separately
  Serial.begin(9600); // use the same baud-rate as the python side 
  while (!Serial); { 
  }
  SPI.begin();

  pinMode(GREEN_LED, OUTPUT);
  digitalWrite(GREEN_LED, LOW);

  pinMode(RED_LED, OUTPUT);
  digitalWrite(RED_LED, LOW);


  pinMode(PUSH_BUTTON, INPUT);


  
}


bool awaitTransmissionRequest_transmitBoardState(){

  
  bool userRequest = false;
  bool robotRequest = false;
  int result;


  //Anounce that the arduino is ready for a request
  Serial.write('1');
  
  while(userRequest == false && robotRequest == false){
    if(Serial.available() > 0) {
      char data;
      char dataString[2];
      data = Serial.read();
      dataString[0] = data;
      dataString[1] = '\0';
      if(strcmp(dataString, "R") == 0){
        userRequest = true;
       
        digitalWrite(GREEN_LED, HIGH);  //Green light for user
        digitalWrite(RED_LED,LOW);
         
        char acknowledgment[] = "ACK";
        Serial.write(acknowledgment);
        
        bool buttonPress = false;
        
        buttonPress = scanButton(); // Holds until true
      
        Serial.println("The button was pressed.");
        digitalWrite(GREEN_LED, LOW);  
        digitalWrite(RED_LED,HIGH);
          
//        obtainBoardState();

        transmitBoardState();   
      }
        
      if(strcmp(dataString, "r") == 0){
        
        robotRequest = true;
        
        // Immediately scan the game board (no press of the pushbutton) upon receiving confirmation that the move has been made.
        
        digitalWrite(GREEN_LED, LOW);  // This should already be LOW
        digitalWrite(RED_LED,HIGH);  // This should already be HIGH
         
        char acknowledgment[] = "ACK";
        Serial.write(acknowledgment);

        int robotMoveComplete = false;
        
        while(robotMoveComplete == false){
          if(Serial.available() > 0) {
            char data;
            char dataString[2];
            data = Serial.read();
            dataString[0] = data;
            dataString[1] = '\0';
            if(strcmp(dataString, "c") == 0){  //==> robot has completed it's move
              robotMoveComplete = true;
            }
          }
         }
       
        //obtainBoardState();
        result = transmitBoardState();     
       }
    }
  }
  return result;
 }



        



void loop() {

  bool request = false;
  
  request = awaitTransmissionRequest_transmitBoardState();


//  while(1);

  

}



int transmitBoardState(){
  
  //sample transmission
  byte gameSquares[65] = {'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','$','*','&'};
  
  char gameSquares_chars[129];
  char gameSquares_ch[65];
  int arrayLength = sizeof(gameSquares);
  
  
  for (int s = 0; s < arrayLength; s++){
   // convert byte to its ascii representation
    sprintf(&gameSquares_chars[s * 2], "%c", gameSquares[s]);   // ==> Each stored entry separated by an extra char sized address 
  }
  
  //        for (int cnt = 0; s < arrayLength; s++){ // Reformatting - not necessary; removes the extra address space between entries
  //          gameSquares_ch[s] = gameSquares_chars[s*2];
  //        }
  
  
  Serial.write('1');  // ==> Ready for transmission
  
  for (int s = 0; s < arrayLength; s++){   // Board state transmission
    Serial.write(gameSquares_chars[s*2]);
  }

 bool transactionComplete = false;

 while(transactionComplete == false){
    if(Serial.available() > 0) {
      char receipt;
      char receiptString[2];
      receipt = Serial.read();
      receiptString[0] = receipt;
      receiptString[1] = '\0';
      if(strcmp(receiptString, "1") == 0){
        transactionComplete = true;
      }
      if(strcmp(receiptString, "-1") == 0){  //  ==> Timeout on the python side during the transmission. 
        transmitBoardState();
        break;
      }
    }
 }

 return transactionComplete;
      
}
  

void obtainBoardState(){

  //scan the board...
  
  
  }



int scanButton(){
 /*
  Debounce

  Each time the input pin goes from LOW to HIGH (e.g. because of a push-button
  press), the output pin is toggled from LOW to HIGH or HIGH to LOW. There's a
  minimum delay between toggles to debounce the circuit (i.e. to ignore noise).

  The circuit:
  - LED attached from pin 13 to ground
  - pushbutton attached from pin 2 to +5V
  - 10 kilohm resistor attached from pin 2 to ground

  - Note: On most Arduino boards, there is already an LED on the board connected
    to pin 13, so you don't need any extra components for this example.

  created 21 Nov 2006
  by David A. Mellis
  modified 30 Aug 2011
  by Limor Fried
  modified 28 Dec 2012
  by Mike Walters
  modified 30 Aug 2016
  by Arturo Guadalupi
  modified March 27, 2020
  by DMD

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/Debounce
*/


  int pushed = false;

  while( pushed == false) {
  
  // read the state of the switch into a local variable:
  int reading = digitalRead(PUSH_BUTTON);

  // check to see if you just pressed the button
  // (i.e. the input went from LOW to HIGH), and you've waited long enough
  // since the last press to ignore any noise:

  // If the switch changed, due to noise or pressing:
  if (reading != lastButtonState) {
    // reset the debouncing timer
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    // whatever the reading is at, it's been there for longer than the debounce
    // delay, so take it as the actual current state:

    // if the button state has changed:
    if (reading != buttonState) {
      buttonState = reading;

      // only toggle the LED if the new button state is HIGH
      if (buttonState == HIGH) {
          pushed = true;
      }
    }
  }


  // save the reading. Next time through the loop, it'll be the lastButtonState:
  lastButtonState = reading;

  }


  return pushed;
  
}
