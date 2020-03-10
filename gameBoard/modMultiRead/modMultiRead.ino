

// may need stuff from: adafruit/Adafruit-MCP23017-Arduino-Library

// Sources: https://github.com/Annaane/MultiRfid/blob/master/FourRFID.ino
// https://www.youtube.com/watch?v=hxQYIwdZRng
// https://lastminuteengineers.com/how-rfid-works-rc522-arduino-tutorial/
//https://github.com/miguelbalboa/rfid/tree/master/examples/ReadUidMultiReader

/**
   --------------------------------------------------------------------------------------------------------------------
   Example sketch/program showing how to read data from more than one PICC to serial.
   --------------------------------------------------------------------------------------------------------------------
   This is a MFRC522 library example; for further details and other examples see: https://github.com/miguelbalboa/rfid
   Example sketch/program showing how to read data from more than one PICC (that is: a RFID Tag or Card) using a
   MFRC522 based RFID Reader on the Arduino SPI interface.
   Warning: This may not work! Multiple devices at one SPI are difficult and cause many trouble!! Engineering skill
            and knowledge are required!
   @license Released into the public domain.
   Typical pin layout used:
   -----------------------------------------------------------------------------------------
               MFRC522      Arduino       Arduino   Arduino    Arduino          Arduino
               Reader/PCD   Uno/101       Mega      Nano v3    Leonardo/Micro   Pro Micro
   Signal      Pin          Pin           Pin       Pin        Pin              Pin
   -----------------------------------------------------------------------------------------
   RST/Reset   RST          9             5         D9         RESET/ICSP-5     RST
   SPI SS 1    SDA(SS)      ** custom, take a unused pin, only HIGH/LOW required *
   SPI SS 2    SDA(SS)      ** custom, take a unused pin, only HIGH/LOW required *
   SPI MOSI    MOSI         11 / ICSP-4   51        D11        ICSP-4           16
   SPI MISO    MISO         12 / ICSP-1   50        D12        ICSP-1           14
   SPI SCK     SCK          13 / ICSP-3   52        D13        ICSP-3           15
*/



#include <SPI.h>
#include <MFRC522.h>

// PIN Numbers : RESET + SDAs
#define RST_PIN         49
#define SS_1_PIN        53
#define SS_2_PIN        33
#define SS_3_PIN        7
#define SS_4_PIN        6

// Led and Relay PINS
#define GreenLed        22
#define RedLed          24


//struct boardState {
//   byte gameSquares[64];
//};

byte gameSquares[64];

//this is the block number we will write into and then read.
int block=2;  //arbitrary

byte blockcontent[16] = {"Q"};
//byte blockcontent[16] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};  //all zeros. This can be used to delete a block.

//This array is used for reading out a block.
byte readbackblock[18];





void dump_byte_array(byte * buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}


#define NR_OF_READERS   1


byte ssPins[] = {SS_1_PIN, SS_2_PIN, SS_3_PIN, SS_4_PIN};

// Create an MFRC522 instance :
MFRC522 mfrc522[NR_OF_READERS];

MFRC522::MIFARE_Key key;          //create a MIFARE_Key struct named 'key', which will hold the card information

/**
   Initialize.
*/
void setup() {

  Serial.begin(9600);           // Initialize serial communications with the PC
  while (!Serial);              // Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)

  SPI.begin();                  // Init SPI bus

  /* Initializing Inputs and Outputs */
  pinMode(GreenLed, OUTPUT);
  digitalWrite(GreenLed, HIGH);
//  pinMode(relayIN, OUTPUT);
//  digitalWrite(relayIN, HIGH);
  pinMode(RedLed, OUTPUT);
  digitalWrite(RedLed, LOW);


  /* looking for MFRC522 readers */
  for (uint8_t reader = 0; reader < NR_OF_READERS; reader++) {
    mfrc522[reader].PCD_Init(ssPins[reader], RST_PIN);
    Serial.print(F("Reader "));
    Serial.print(reader);
    Serial.print(F(": "));
    mfrc522[reader].PCD_DumpVersionToSerial();
    //mfrc522[reader].PCD_SetAntennaGain(mfrc522[reader].RxGain_max);

      // Prepare the security key for the read and write functions.
  for (byte i = 0; i < 6; i++) {
    key.keyByte[i] = 0xFF;  //keyByte is defined in the "MIFARE_Key" 'struct' definition in the .h file of the library
    }
  }

}



//Read specific block
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

//reading a block
byte buffersize = 18;//we need to define a variable with the read buffer size, since the MIFARE_Read method below needs a pointer to the variable that contains the size...
status = mfrc522[reader].MIFARE_Read(blockNumber, arrayAddress, &buffersize);//&buffersize is a pointer to the buffersize variable; MIFARE_Read requires a pointer instead of just a number
  if (status != MFRC522::STATUS_OK) {
          Serial.print("MIFARE_read() failed: ");
          Serial.println(mfrc522[reader].GetStatusCodeName(status));
          return 4;//return "4" as error message
  }
  Serial.println("block was read");
}


//Write specific block
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
         Serial.print("PCD_Authenticate() failed: ");
         Serial.println(mfrc522[reader].GetStatusCodeName(status));
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

/*
   Main loop.
*/

void loop() {

  uint8_t reader = 0;

  for (reader = 0; reader < NR_OF_READERS; reader++) {

    // Looking for new cards
    if (mfrc522[reader].PICC_IsNewCardPresent() && mfrc522[reader].PICC_ReadCardSerial()) {
      Serial.print(F("Reader "));
      Serial.print(reader);

      // Show some details of the PICC (that is: the tag/card)
//      Serial.print(F(": Card UID:"));
//      dump_byte_array(mfrc522[reader].uid.uidByte, mfrc522[reader].uid.size);
//      Serial.println();


     // writeBlock(block, blockcontent, reader);

      readBlock(block, readbackblock, reader);

      gameSquares[reader] = *readbackblock;

       // stop communication
      mfrc522[reader].PICC_HaltA();
      mfrc522[reader].PCD_StopCrypto1();

      delay(1000);


        //print the block contents
      Serial.print("read block: ");
      for (int j=0 ; j<16 ; j++){
        Serial.write (readbackblock[j]);
        }
      Serial.println("");
//      delay(100);
    }


    int square = 0;
    for (byte reader = 0; reader < NR_OF_READERS; reader++) {
      Serial.print("gameSquare: ");
      Serial.print(square);
      Serial.println("");
      Serial.print("piece: ");
      Serial.write(gameSquares[reader]);
      Serial.println("");
      Serial.println("");
      square++;
    }



    delay(5000);


    }
  }
