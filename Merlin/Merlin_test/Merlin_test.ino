#define stepPin1 26
#define dirPin1 24
#define enPin1 22

#define stepPin0 38
#define dirPin0 36
#define enPin0 34

#define stepPin2 52
#define dirPin2 50
#define enPin2 48

#define stepPin3 35
#define dirPin3 33
#define enPin3 31

#define stepPin4 43
#define dirPin4 41
#define enPin4 39

#define stepPin5 43
#define dirPin5 41
#define enPin5 39


#define gripperPin 42
#define gripperPulse 1500

#define MAX_SPEED 600
#define ACCELERATION 200
#define INTERFACE_TYPE 1 //Driver interface
#define NUM_STEPPERS 5
#define STEP_ANGLE 1.8
#define STEP_RATIO 0.5

#include <AccelStepper.h>
#include <MultiStepper.h>
#include <Servo.h>
#include <math.h>

AccelStepper stepper0(AccelStepper::DRIVER, stepPin0, dirPin0);  //shoulder
AccelStepper stepper1(AccelStepper::DRIVER, stepPin1, dirPin1);  //elbow
AccelStepper stepper2(AccelStepper::DRIVER, stepPin2, dirPin2);  //wrist
AccelStepper stepper3(AccelStepper::DRIVER, stepPin3, dirPin3);  //base
AccelStepper stepper4(AccelStepper::DRIVER, stepPin4, dirPin4);  //

MultiStepper arm_steppers;

Servo gripper;
int pos0 = 200;
int pos1 = 1081;
int pos2 = -315;
int pos3 = 1100;
int pos4 = 1400;

int cw = 1;
bool flag = true;

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
    gripper.write(0);

    stepper0.setMaxSpeed(MAX_SPEED);
    stepper0.setAcceleration(ACCELERATION);
    stepper1.setMaxSpeed(MAX_SPEED);
    stepper1.setAcceleration(ACCELERATION);
    stepper2.setMaxSpeed(MAX_SPEED);
    stepper2.setAcceleration(ACCELERATION);
    stepper3.setMaxSpeed(MAX_SPEED);
    stepper3.setAcceleration(ACCELERATION);
    stepper4.setMaxSpeed(300);
    stepper4.setAcceleration(ACCELERATION);

    arm_steppers.addStepper(stepper0);
    arm_steppers.addStepper(stepper1);
    arm_steppers.addStepper(stepper2);
    arm_steppers.addStepper(stepper3);
    arm_steppers.addStepper(stepper4);  
}

void actuate_gripper (bool decision) {
    //Send signal to servo to make one full rotation
    //It only moves clockwise for now. Anticlockwise rotation is trivial but hasn't been implemented.

    bool clockwise;

    if (decision){
        //clockwise
      for (int pos = 0; pos <= 20; pos++){
        gripper.write(pos);
        delay(15);
      }
    } else{//clockwise = false
        for (int pos = 20; pos >= 0; pos--){
        gripper.write(pos);
        delay(15);
      }
    }
}


void loop(){
  if (flag == true)
  {
//    Serial.print("moveTo\n");
    delay(500);
//    stepper0.moveTo(pos0);
//    stepper1.moveTo(pos1);
//    stepper2.moveTo(pos2);
      stepper3.moveTo(pos3);
//      stepper4.moveTo(pos4);
//    actuate_gripper(true);
//    delay(500);
//    actuate_gripper(false);
    flag = false;


//    stepper4.moveTo(pos);
  }
//  Serial.print("run\n");
//  stepper0.run();
//  stepper1.run();
//  stepper2.run();
    stepper3.runToPosition();
//  stepper4.runToPosition();
//  

}
