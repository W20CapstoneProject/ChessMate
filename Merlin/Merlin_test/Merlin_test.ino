#define stepPin1 22
#define dirPin1 24
#define enPin1 26

#define stepPin0 41
#define dirPin0 43
#define enPin0 45

#define stepPin2 32
#define dirPin2 34
#define enPin2 36

#define stepPin3 33 
#define dirPin3 35
#define enPin3 37

#define stepPin4 40
#define dirPin4 42
#define enPin4 44

#define gripperPin 46
#define gripperPulse 1500

#define MAX_SPEED 3000
#define ACCELERATION 1000
#define INTERFACE_TYPE 1 //Driver interface
#define NUM_STEPPERS 5
#define STEP_ANGLE 1.8
#define STEP_RATIO 0.5

#include <AccelStepper.h>
#include <MultiStepper.h>
#include <Servo.h>
#include <math.h>

AccelStepper stepper0(AccelStepper::DRIVER, stepPin0, dirPin0);
AccelStepper stepper1(AccelStepper::DRIVER, stepPin1, dirPin1);
AccelStepper stepper2(AccelStepper::DRIVER, stepPin2, dirPin2);
AccelStepper stepper3(AccelStepper::DRIVER, stepPin3, dirPin3);
AccelStepper stepper4(AccelStepper::DRIVER, stepPin4, dirPin4);
MultiStepper arm_steppers;

Servo gripper;
int pos = 600;
int cw = 1;

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

    gripper.attach(gripperPin);
    //gripper.write(0);

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
    arm_steppers.addStepper(stepper3);
    arm_steppers.addStepper(stepper4);  
}

void actuate_gripper (int decision) {
    //Send signal to servo to make one full rotation
    //It only moves clockwise for now. Anticlockwise rotation is trivial but hasn't been implemented.

    bool clockwise;

    if (decision){
        //clockwise
      for (int pos = 0; pos <= 180; pos++){
        gripper.write(pos);
        delay(15);
      }
    } else{//clockwise = false
        for (int pos = 180; pos >= 0; pos--){
        gripper.write(pos);
        delay(15);
      }
    }
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
    stepper3.moveTo(pos);
    stepper4.moveTo(pos);
  }

  stepper0.run();
  stepper1.run();
  stepper2.run();
  stepper3.run();
  stepper4.run();
  
//  actuate_gripper(true);
//  delay(500);
//  actuate_gripper(false);

//  if(cw == 1){
//    cw = -1;
//    }else{ cw = 1;}
  
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
