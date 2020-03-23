#ifndef SerialCM_h
#define SerialCM_h

#include "Arduino.h"

class SerialCM
{
  private:
    String _ACK;
    String _incomingByte;

  public:
    SerialCM();
    ~SerialCM();
    void init();
    void serialCommunication();
    void handleCommand(String command);
};

#endif
