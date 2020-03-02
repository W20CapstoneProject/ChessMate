#define stepPin0 33
#define dirPin0 35
#define enPin0 37

#define stepPin1 40
#define dirPin1 42
#define enPin1 44

#define stepPin2 32
#define dirPin2 34
#define enPin2 36

#define stepPin3 41 
#define dirPin3 43
#define enPin3 45

#define stepPin4 22
#define dirPin4 24
#define enPin4 26

#define MAX_SPEED 3000
#define ACCELERATION 1000
#define INTERFACE_TYPE 1 //Driver interface
#define NUM_STEPPERS 5
#define STEP_ANGLE 1.8
#define STEP_RATIO 0.5

#include <AccelStepper.h>
#include <MultiStepper.h>
#include <math.h>

AccelStepper stepper0(AccelStepper::DRIVER, stepPin0, dirPin0);
AccelStepper stepper1(AccelStepper::DRIVER, stepPin1, dirPin1);
AccelStepper stepper2(AccelStepper::DRIVER, stepPin2, dirPin2);
AccelStepper stepper3(AccelStepper::DRIVER, stepPin3, dirPin3);
AccelStepper stepper4(AccelStepper::DRIVER, stepPin4, dirPin4);
MultiStepper arm_steppers;

int pos = 600;

void setup()
{
    Serial.begin(9600);
    pinMode(stepPin0, OUTPUT); //step pulse pin
    pinMode(dirPin0, OUTPUT);  //rotional direction control pin
    pinMode(enPin0, OUTPUT);   //enable/disable pin
    digitalWrite(enPin0, LOW);

    pinMode(stepPin1, OUTPUT); //step pulse pin
    pinMode(dirPin1, OUTPUT);  //rotional direction control pin
    pinMode(enPin1, OUTPUT);   //enable/disable pin
    digitalWrite(enPin1, LOW);

    pinMode(stepPin2, OUTPUT); //step pulse pin
    pinMode(dirPin2, OUTPUT);  //rotional direction control pin
    pinMode(enPin2, OUTPUT);   //enable/disable pin
    digitalWrite(enPin2, LOW);

    pinMode(stepPin3, OUTPUT); //step pulse pin
    pinMode(dirPin3, OUTPUT);  //rotional direction control pin
    pinMode(enPin3, OUTPUT);   //enable/disable pin
    digitalWrite(enPin3, LOW);

    pinMode(stepPin4, OUTPUT); //step pulse pin
    pinMode(dirPin4, OUTPUT);  //rotional direction control pin
    pinMode(enPin4, OUTPUT);   //enable/disable pin
    digitalWrite(enPin4, LOW);

    stepper0.setMaxSpeed(MAX_SPEED);
    stepper0.setAcceleration(ACCELERATION);
    stepper1.setMaxSpeed(MAX_SPEED);
    stepper1.setAcceleration(ACCELERATION);
    stepper2.setMaxSpeed(MAX_SPEED);
    stepper2.setAcceleration(ACCELERATION);
    stepper3.setMaxSpeed(MAX_SPEED);
    stepper3.setAcceleration(ACCELERATION);
    stepper4.setMaxSpeed(1000);
    stepper4.setAcceleration(ACCELERATION);

    arm_steppers.addStepper(stepper0);
    arm_steppers.addStepper(stepper1);
    arm_steppers.addStepper(stepper2);    
}

void loop(){
  if (stepper0.distanceToGo() == 0)
  {
    delay(500);
    pos = -pos;
    if (abs(pos) < 10){
      pos = -(pos + 8000);
      //digitalWrite(enPin, HIGH);
      delay(1000);
      //digitalWrite(enPin, LOW);
      }
    stepper0.moveTo(pos);
    stepper1.moveTo(pos);
    stepper2.moveTo(pos); 
    stepper3.moveTo(pos+500000);
    stepper4.moveTo(pos+5000); 
  }

  stepper0.run();
  stepper1.run();
  stepper2.run();
  stepper3.run();
  stepper4.run();
  
//  long positions[3];
//
//  positions[0] = 800;
//  positions[1] = 800;
//  positions[2] = 800;
//  
//  arm_steppers.moveTo(positions);
//  arm_steppers.runSpeedToPosition();
//  delay(1000);
//
//  positions[0] = 0;
//  positions[1] = 0;
//  positions[2] = 0;
//  
//  arm_steppers.moveTo(positions);
//  arm_steppers.runSpeedToPosition();
//  delay(1000);
//  
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
