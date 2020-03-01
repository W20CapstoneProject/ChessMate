#define stepPin 10
#define dirPin 9
#define enPin 8

#define MAX_SPEED 3000
#define ACCELERATION 1000
#define INTERFACE_TYPE 1 //Driver interface
#define NUM_STEPPERS 5
#define STEP_ANGLE 1.8
#define STEP_RATIO 0.5

#include <AccelStepper.h>
#include <math.h>

AccelStepper stepper(AccelStepper::DRIVER, stepPin, dirPin);

int pos = 8000;

void setup()
{
    Serial.begin(9600);
    pinMode(stepPin, OUTPUT); //step pulse pin
    pinMode(dirPin, OUTPUT);  //rotional direction control pin
    pinMode(enPin, OUTPUT);   //enable/disable pin
    digitalWrite(enPin, LOW);

    stepper.setMaxSpeed(MAX_SPEED);
    stepper.setAcceleration(ACCELERATION);
}

void loop(){
  if (stepper.distanceToGo() == 0)
  {
    delay(500);
    pos = (pos/STEP_ANGLE);
    if (abs(pos) < 10){
      pos = -(pos + 8000);
      //digitalWrite(enPin, HIGH);
      delay(10000);
      //digitalWrite(enPin, LOW);
      }
    stepper.moveTo(pos);    
  }

  stepper.run();
//    digitalWrite(dirPin, HIGH);
//    printf("loop\n");
//
//    for(int i = 0; i < 10; i++){
//        digitalWrite(stepPin, HIGH);
//        delayMicroseconds(500);
//        digitalWrite(stepPin, LOW);
//        delayMicroseconds(500);
//        printf("loop\n");
//    }
//    delayMicroseconds(5000);
}