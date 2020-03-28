/**************************************************************************************************
 *                                                                                                *
 *                         ChessMa†eGameBoard, D.M.Douziech 2020                                  *
 *                                                                                                *
 *                                                                                                *
 * This program is intened for use with a ChessMa†e game board and in conjuction with ChessMa†e.py*
 *                                                                                                *
 **************************************************************************************************/

/*NOTES:

For the arduinoMega 2560:
SPI MOSI - pin 51
SPI MISO - pin 50
SPI SCK - pin 52

Game piece IDs are taken from FE Notation:

white king  - K
white queen - Q
white bishop - B
white knight - N
white rook - R

black king  - k
black queen - q
black bishop - b
black knight - n
black rook - r

N.B. - Transmission codes: R ==> User; r ==> robot */

using namespace std;

#include <SPI.h>
#include <MFRC522.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <limits.h> // Used for INT_MAX
#include <Stream.h>

// PIN Numbers: RESETs & SDA (SS) signals
#define RST_PIN         49  
#define RST_PIN2        53

// 32 pins,  64 SS lines:

#define SS_1        2   // Used when RST_PIN is LOW, RST_PIN2 is HIGH
#define SS_2        3  
#define SS_3        4
#define SS_4        5
#define SS_5        6 
#define SS_6        7  
#define SS_7        8
#define SS_8        9

#define SS_9        2 // Used when RST_PIN is HIGH, RST_PIN2 is LOW
#define SS_10       3   
#define SS_11       4 
#define SS_12       5 
#define SS_13       6    
#define SS_14       7   
#define SS_15       8  
#define SS_16       9 

#define SS_17       10  // Used when RST_PIN is LOW, RST_PIN2 is HIGH
#define SS_18       11   
#define SS_19       12
#define SS_20       13
#define SS_21       14   
#define SS_22       15
#define SS_23       16 
#define SS_24       17
           
#define SS_25       10   // Used when RST_PIN is HIGH, RST_PIN2 is LOW
#define SS_26       11
#define SS_27       12 
#define SS_28       13   
#define SS_29       14   
#define SS_30       15 
#define SS_31       16
#define SS_32       17

#define SS_33       18 // Used when RST_PIN is LOW, RST_PIN2 is HIGH
#define SS_34       19
#define SS_35       20
#define SS_36       21
#define SS_37       22
#define SS_38       23
#define SS_39       24
#define SS_40       25

#define SS_41       18  // Used when RST_PIN is HIGH, RST_PIN2 is LOW
#define SS_42       19
#define SS_43       20
#define SS_44       21
#define SS_45       22
#define SS_46       23
#define SS_47       24
#define SS_48       25

#define SS_49       26 // Used when RST_PIN is LOW, RST_PIN2 is HIGH
#define SS_50       27
#define SS_51       28
#define SS_52       29
#define SS_53       30
#define SS_54       31
#define SS_55       32
#define SS_56       33

#define SS_57       26  // Used when RST_PIN is HIGH, RST_PIN2 is LOW
#define SS_58       27
#define SS_59       28
#define SS_60       29
#define SS_61       30
#define SS_62       31
#define SS_63       32
#define SS_64       33

#define GREEN_LED    34     
#define RED_LED      35    

#define PUSH_BUTTON  36    


//Primary level multiplexor and demultiplexor select lines:
#define DM_S1_P           48  // 'D' on the data sheets for both the mux and demux  (i.e., the MSB)
#define DM_S2_P           46  // 'C'
#define DM_S3_P           44  // 'B'
#define DM_S4_P           42  // 'A' (LSB)


//Secondary Level multiplexor and demultiplexor select lines:
#define DM_S1           47  // 'D' on the data sheets for both the mux and demux  (i.e., the MSB)
#define DM_S2           45  // 'C'
#define DM_S3           43  // 'B'
#define DM_S4           41  // 'A' (LSB)

//N.B. - Pins [37, 40] remain free for other use (Arduino Mega 2560).


int buttonState;             // the current reading from the input pin
int lastButtonState = LOW;   // the previous reading from the input pin

unsigned long lastDebounceTime = 0;  // the last time the output pin was toggled
unsigned long debounceDelay = 50;    // the debounce time



byte gameSquares[64];



//The (arbitrary) block number used for writing and reading piece IDs.
int block=2; 

byte empty[2] = {"e"}; // Used for describing an empty game square

byte blockcontent[16] = {}; //{"r"};  //Used for writing  
//byte blockcontent[16] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};  //all zeros. This can be used to delete a block.

//A buffer used for reading 
byte readbackblock[18];

#define NR_OF_READERS   0 //64

// An array of MFRC522 modules:
MFRC522 mfrc522[NR_OF_READERS];

MFRC522::MIFARE_Key key; //MIFARE_Key struct, used to store the PICC data

byte SSlines[] = {SS_1, SS_2, SS_3, SS_4, SS_5, SS_6, SS_7, SS_8, SS_9, SS_10, SS_11, SS_12, SS_13, SS_14, SS_15, SS_16, SS_17, SS_18, SS_19, SS_20, SS_21, SS_22, SS_23, SS_24, SS_25, SS_26, SS_27, SS_28, SS_29, SS_30, SS_31, SS_32, SS_33, SS_34, SS_35, SS_36, SS_37, SS_38, SS_39, SS_40, SS_41, SS_42, SS_43, SS_44, SS_45, SS_46, SS_47, SS_48, SS_49, SS_50, SS_51, SS_52, SS_53, SS_54, SS_55, SS_56, SS_57, SS_58, SS_59, SS_60, SS_61, SS_62, SS_63, SS_64};



//Function Declarations:
void select_Mux_deMux_Lines(uint8_t reader);
void dump_byte_array(byte * buffer, byte bufferSize);
int readBlock(int blockNumber, byte arrayAddress[], uint8_t reader);
int writeBlock(int blockNumber, byte arrayAddress[], uint8_t reader);
const char** toBinary( unsigned int a );
void select_Mux_deMux_Lines(uint8_t reader);
void selectResetLine(uint8_t reader);
void obtainBoardState();
bool awaitTransmissionRequest_transmitBoardState();
int transmitBoardState();
int scanButton();
void piecePromotion(uint8_t reader, char colour);  //Extra queens came with the set, so this can probably be avoided altogether.
void encodePieceID(uint8_t reader, char pieceName);


/*
   Initialization
*/
void setup() {

  Serial.begin(9600);           // Initialize serial communication with the PC
  while (!Serial);              // Do nothing if the serial port is not opened (added for Arduinos based on ATMEGA32U4)

  SPI.begin();                  // Init SPI bus

// Initialization of pins used by the MUX/DEMUX ICs
  pinMode(DM_S1_P, OUTPUT);
  pinMode(DM_S2_P, OUTPUT);
  pinMode(DM_S3_P, OUTPUT);
  pinMode(DM_S4_P, OUTPUT);
  
  pinMode(DM_S1, OUTPUT);
  pinMode(DM_S2, OUTPUT);
  pinMode(DM_S3, OUTPUT);
  pinMode(DM_S4, OUTPUT);

  digitalWrite(DM_S1_P, LOW);   
  digitalWrite(DM_S2_P, LOW);
  digitalWrite(DM_S3_P, LOW);
  digitalWrite(DM_S4_P, LOW);
  
  digitalWrite(DM_S1, LOW);   
  digitalWrite(DM_S2, LOW);
  digitalWrite(DM_S3, LOW);
  digitalWrite(DM_S4, LOW);

  //LEDs and Button:
  pinMode(GREEN_LED, OUTPUT);
  digitalWrite(GREEN_LED, LOW);

  pinMode(RED_LED, OUTPUT);
  digitalWrite(RED_LED, LOW);

  pinMode(PUSH_BUTTON, INPUT);


  for (byte i = 0; i < 6; i++) {
    key.keyByte[i] = 0xFF;  //keyByte is defined in the "MIFARE_Key" 'struct' definition in the .h file of the MFRC522 library.
    }

} //end setup

  

// Main
void loop() {

awaitTransmissionRequest_transmitBoardState();
   
}



//FUNCTIONS

void select_Mux_deMux_Lines(uint8_t reader){  //Self-explanatory

   //  INDICES (binaryRep):          0   1   2   3
   //  DATA SHEET CORRESPONDENCE:   'D' 'C' 'B' 'A'
   //  DM SELECTS:                   1   2   3   4
  

    const char** binaryRep = (const char **)malloc(sizeof(const char*)*7);
    binaryRep = toBinary(reader);

//    Serial.println("Current binaryRep:" );
//    for (int i=0; i<4; ++i) {
//      Serial.print(binaryRep[i]);
//    }
//    Serial.println();

    int readerInt = (int)reader;

//Select primary lines:

    if( reader < 16){  // ==> line 0
      digitalWrite(DM_S1_P, LOW);
      digitalWrite(DM_S2_P, LOW);
      digitalWrite(DM_S3_P, LOW);
      digitalWrite(DM_S4_P, LOW);    
//      Serial.println("Primary line 0 selected");
     }  

    else if( 15 < reader < 32){  // ==> line 1
      digitalWrite(DM_S1_P, LOW);
      digitalWrite(DM_S2_P, LOW);
      digitalWrite(DM_S3_P, LOW);
      digitalWrite(DM_S4_P, HIGH);    
//      Serial.println("Primary line 1 selected");
     } 

    else if( 31 < reader < 48){  // ==> line 2
      digitalWrite(DM_S1_P, LOW);
      digitalWrite(DM_S2_P, LOW);
      digitalWrite(DM_S3_P, HIGH);
      digitalWrite(DM_S4_P, LOW);    
//      Serial.println("Primary line 2 selected");
     } 


    else if ( 31 < reader < 48){  // ==> line 3
      digitalWrite(DM_S1_P, LOW);
      digitalWrite(DM_S2_P, LOW);
      digitalWrite(DM_S3_P, HIGH);
      digitalWrite(DM_S4_P, HIGH);    
//      Serial.println("Primary line 3 selected");
     }
   
  
 delay(50);

   
//Select secondary lines:

    if( strcmp(binaryRep[0], "1") == 0){
      digitalWrite(DM_S1, HIGH);
//      Serial.println("DM_S1, HIGH");
     }  
    
    else{
      digitalWrite(DM_S1, LOW); 
//      Serial.println("DM_S1, LOW"); 
      }
  
  
    if( strcmp(binaryRep[1], "1") == 0){
      digitalWrite(DM_S2, HIGH);
//      Serial.println("DM_S2, HIGH");
    } 
      
    else{
      digitalWrite(DM_S2, LOW);
//      Serial.println("DM_S2, LOW");  
    }
   
    if( strcmp(binaryRep[2], "1") == 0){ 
      digitalWrite(DM_S3, HIGH);
//      Serial.println("DM_S3, HIGH");
    }
    
    else{
      digitalWrite(DM_S3, LOW);
//      Serial.println("DM_S3, LOW");  
    }
    
   
    if( strcmp(binaryRep[3], "1") == 0){
      digitalWrite(DM_S4, HIGH);
//      Serial.println("DM_S4, HIGH");  
    }
    
    else{
      digitalWrite(DM_S4, LOW);
//      Serial.println("DM_S4, LOW");  
    }

      delay(50);
  
  }



//To read a specific block:
int readBlock(int blockNumber, byte arrayAddress[], uint8_t reader) 
{
  int largestModulo4Number=blockNumber/4*4;
  int trailerBlock=largestModulo4Number+3;//determine trailer block for the sector

  //authentication of the desired block for access
  byte status = mfrc522[reader].PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, trailerBlock, &key, &(mfrc522[reader].uid));

  if (status != MFRC522::STATUS_OK) {
         Serial.print("PCD_Authenticate() failed (read): ");
         Serial.println(mfrc522[reader].GetStatusCodeName(status));
         return 3;//return "3" as error message
  }

//reading 
byte buffersize = 18;//we need to define a variable with the read buffer size, since the MIFARE_Read method below needs a pointer to the variable that contains the size... 
status = mfrc522[reader].MIFARE_Read(blockNumber, arrayAddress, &buffersize);//&buffersize is a pointer to the buffersize variable; MIFARE_Read requires a pointer instead of just a number
  if (status != MFRC522::STATUS_OK) {
          Serial.print("MIFARE_read() failed: ");
          Serial.println(mfrc522[reader].GetStatusCodeName(status));
          return 4;//return "4" as error message
  }
//  Serial.println("block was read :");
  Serial.println("");
}


//To write to a specific block:    
int writeBlock(int blockNumber, byte arrayAddress[], uint8_t reader) 
{
  //this makes sure that we only write into data blocks. Every 4th block is a trailer block for the access/security info.
  int largestModulo4Number=blockNumber/4*4;
  int trailerBlock=largestModulo4Number+3;//determine trailer block for the sector
  if (blockNumber > 2 && (blockNumber+1)%4 == 0){Serial.print(blockNumber);Serial.println(" is a trailer block:");return 2;}
  Serial.print(blockNumber);
  Serial.println(" is a data block:");
  
  //authentication of the desired block for access
  byte status = mfrc522[reader].PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, trailerBlock, &key, &(mfrc522[reader].uid));
  if (status != MFRC522::STATUS_OK) {
//         Serial.print("PCD_Authenticate() failed: ");
//         Serial.println(mfrc522[reader].GetStatusCodeName(status));
         return 3;//return "3" as error message
  }
  
  //writing the block 
  status = mfrc522[reader].MIFARE_Write(blockNumber, arrayAddress, 16);
  //status = mfrc522[reader].MIFARE_Write(9, value1Block, 16);
  if (status != MFRC522::STATUS_OK) {
           Serial.print("MIFARE_Write() failed: ");
           Serial.println(mfrc522[reader].GetStatusCodeName(status));
           return 4;//return "4" as error message
  }
  Serial.println("block was written");
}


void dump_byte_array(byte * buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}


// This is code that I wrote in another class, slightly modified. 

const char** toBinary( unsigned int a ) {
  
  const char** binRep = (const char **)malloc(sizeof(const char*)*5);
  unsigned int b = 1<<3;
  for (int i=0; i<4; ++i) {
    if ((a&b)!=0) {
      binRep[i] = "1";
      
    }
    else {
      binRep[i] = "0";
    }
    b = b >> 1; // b = b / 2
  }
//  Serial.println();
//
//  Serial.println("binaryRep:" );
//  for (int i=0; i<4; ++i) {
//    Serial.print(binRep[i]);
//  }
//  Serial.println();
  
  return binRep;

}


int selectResetLine(uint8_t reader, int currentRST_PIN){

    if( (reader < 8) || (15 < reader < 24) || (31 < reader < 40) || (47 < reader < 56)){
      digitalWrite(RST_PIN2, HIGH);   //Hold all even rows {2,4,6,8} in an INACTIVE state; activate all odd rows {1,3,5,7}
      digitalWrite(RST_PIN, LOW);
      currentRST_PIN = RST_PIN;
      delay(50);
      return currentRST_PIN;
      
    }

    else{
      digitalWrite(RST_PIN, HIGH);   // Hold all odd rows in an INACTIVE state; activate all even rows 
      digitalWrite(RST_PIN2, LOW);
      currentRST_PIN = RST_PIN2;
      delay(50);
      return currentRST_PIN;
    }
  
  }




bool awaitTransmissionRequest_transmitBoardState(){  //Self-explanatory
  
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
          
        obtainBoardState();

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
       
        obtainBoardState();
        result = transmitBoardState();     
       }
    }
  }
  return result;
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
  
  uint8_t reader = 0;
  byte buffer_ATR[2];  //Used to Acknowledge a Transfer Request
  byte buffer_ATR_size = sizeof(buffer_ATR);

  for (reader = 0; reader < NR_OF_READERS; reader++) { 

    int currentRST_PIN = 0;

    currentRST_PIN = selectResetLine(reader, currentRST_PIN);

    if(currentRST_PIN == 0){
      //Error
      Serial.print("RST_PIN = 0");
      }
      
    select_Mux_deMux_Lines(reader);  // The correct lines have been selected, now we can intialize and read using the specific module
     
    mfrc522[reader].PCD_Init(SSlines[reader], currentRST_PIN);  



   if (mfrc522[reader].PICC_IsNewCardPresent() && mfrc522[reader].PICC_ReadCardSerial()) {
//      Serial.println("new card section");
//      Serial.print(F("Reader: "));
      Serial.print(reader);
      
//      writeBlock(block, blockcontent, reader);  // Was just testing write functionality here
//
//      delay(1000);

      readBlock(block, readbackblock, reader);

      gameSquares[reader] = *readbackblock;

       // stop communication
      mfrc522[reader].PICC_HaltA();
      mfrc522[reader].PCD_StopCrypto1();
      delay(50);


        //print the block contents
//      Serial.print("read block: ");
//      for (int j=0 ; j<16 ; j++){
//        Serial.write (readbackblock[j]);
//        }
//      Serial.println("");

    }
    
    else{ 
       int largestModulo4Number=block/4*4;
       int trailerBlock=largestModulo4Number+3;//determine trailer block for the sector
       mfrc522[reader].PICC_WakeupA(buffer_ATR, &buffer_ATR_size);
       mfrc522[reader].PICC_ReadCardSerial();
       byte status = mfrc522[reader].PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, trailerBlock, &key, &(mfrc522[reader].uid));  //If the PICC cannot be authenticated, the game square must now be empty.
       if (status != MFRC522::STATUS_OK) {
//        Serial.print("PCD_Authenticate() failed (read): ");
//        Serial.println(mfrc522[reader].GetStatusCodeName(status));
          // Cease communication (necessary)
          mfrc522[reader].PICC_HaltA();
          mfrc522[reader].PCD_StopCrypto1();
          delay(50);
          gameSquares[reader] = empty[0];
        }  // Otherwise the PICC can be authenticated ==> the game square has the same game piece as the last cycle.
         
            // Cease communication (necessary)
        mfrc522[reader].PICC_HaltA();
        mfrc522[reader].PCD_StopCrypto1();
        delay(50);
    }
 
      
    
    }

    for (byte reader = 0; reader < NR_OF_READERS; reader++) {
      Serial.print("gameSquare: ");
      Serial.print(reader);
      Serial.println("");
      Serial.print("piece: ");
      Serial.write(gameSquares[reader]);
      Serial.println("");
      Serial.println("");
    }
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

void piecePromotion(uint8_t reader, char* colour){ // Extra queens came with the set, so this can probably just be avoided altogether.

  if(strcmp(colour,"W") == 0){
     byte queen[16] = {"Q"};
     writeBlock(block, queen, reader);
     }
  
  else{
    byte queen[16] = {"q"};
    writeBlock(block, queen, reader);
    }
   
  }


 
 void encodePieceID(uint8_t reader, byte pieceName){
  
  blockcontent[0] = pieceName;
  
  int currentRST_PIN = 0;

  currentRST_PIN = selectResetLine(reader, currentRST_PIN);

  if(currentRST_PIN == 0){
    //Error
    Serial.print("RST_PIN = 0");
    }
    
  select_Mux_deMux_Lines(reader);  // The correct lines have been selected, now we can intialize and write to a specific module.
   
  mfrc522[reader].PCD_Init(SSlines[reader], currentRST_PIN);  

  writeBlock(block, blockcontent, reader);  // Was just testing write functionality here

  delay(100);

  readBlock(block, readbackblock, reader);

  gameSquares[reader] = *readbackblock;

   // stop communication
  mfrc522[reader].PICC_HaltA();
  mfrc522[reader].PCD_StopCrypto1();
  delay(50);

 }


  


 
  
