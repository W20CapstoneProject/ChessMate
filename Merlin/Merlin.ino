//Creation Date: February 2nd, 2020
//Original Author: Erik Lewis
//Description: This code will set up the Arduino Mega so that
//              it can communicate with the stepper motor driver
//              array that drives the stepper motors of the Moveo
//              robot arm. It additionaly will convert the 3 dimensional
//              coordinates received from the CMController
//              into steps for the motors such that the arm's
//              end effector will reach the desired end point.
//**A NOTE ON MEMORY MANAGEMENT: I am avoiding dynamic memory allocation
//                               for the Arduino specifically, as some personal
//                               research has suggested it would cause heap fragmentation.
//                               More personal research is needed to clarify this
//                               so for now we are going with the prevailing public opinion.

#define debug 1

#include "Arduino.h"
#include "pin.h"
#include "IK_calc.h"
#include "SerialCM/SerialCM.h"
#include "MoveoArm/MoveoArm.h"
#include <AccelStepper.h>
#include <MultiStepper.h>
#include <Servo.h>



int stepPins[NUM_STEPPERS] = {stepPin_shoulder, stepPin_elbow, stepPin_wrist, stepPin_base, stepPin_roll};
int dirPins[NUM_STEPPERS]  = {dirPin_shoulder, dirPin_elbow, dirPin_wrist, dirPin_base, dirPin_roll};
int enPins[NUM_STEPPERS]   = {enPin_shoulder, enPin_elbow, enPin_wrist, enPin_base, enPin_roll};
//Unfortunately there is no way to initlize these as an array. It must be individual objects.
AccelStepper stepper_shoulder(AccelStepper::DRIVER, stepPins[0], dirPins[0]);
AccelStepper stepper_elbow(AccelStepper::DRIVER, stepPins[1], dirPins[1]);
AccelStepper stepper_wrist(AccelStepper::DRIVER, stepPins[2], dirPins[2]);
AccelStepper stepper_base(AccelStepper::DRIVER, stepPins[3], dirPins[3]);
AccelStepper stepper_roll(AccelStepper::DRIVER, stepPins[4], dirPins[4]);

MultiStepper arm_steppers;

Servo gripper;
int NEW_MOVE_SIZE = 4;

double new_move[4];
double previous_move[5];

void setup(){
    Serial.begin(9600);

    for (int i = 0; i < NUM_STEPPERS; i++){
      pinMode(stepPins[i], OUTPUT); //step pulse pin
      pinMode(dirPins[i], OUTPUT);  //rotional direction control pin
      pinMode(enPins[i], OUTPUT);   //enable/disable pin
      digitalWrite(enPins[i], LOW); //initially disable the motors
    }

//    //Setup all the pins for the stepper drivers
//    pinMode(stepPin_shoulder, OUTPUT); //step pulse pin
//    pinMode(dirPin_shoulder, OUTPUT);  //rotional direction control pin
//    pinMode(enPin_shoulder, OUTPUT);   //enable/disable pin
//    digitalWrite(enPin_shoulder, LOW); //initially disable the motors
//
//    pinMode(stepPin_elbow, OUTPUT);
//    pinMode(dirPin_elbow, OUTPUT);
//    pinMode(enPin_elbow, OUTPUT);
//    digitalWrite(enPin_elbow, LOW);
//
//    pinMode(stepPin_wrist, OUTPUT);
//    pinMode(dirPin_wrist, OUTPUT);
//    pinMode(enPin_wrist, OUTPUT);
//    digitalWrite(enPin_wrist, LOW);
//
//    pinMode(stepPin_base, OUTPUT);
//    pinMode(dirPin_base, OUTPUT);
//    pinMode(enPin_base, OUTPUT);
//    digitalWrite(enPin_base, LOW);
//
//    pinMode(stepPin_roll, OUTPUT);
//    pinMode(dirPin_roll, OUTPUT);
//    pinMode(enPin_roll, OUTPUT);
//    digitalWrite(enPin_roll, LOW);

    pinMode(gripperPin, OUTPUT);

    //Configure stepper base parameters and add them all to the MultiStepper
    // controller
    stepper_shoulder.setMaxSpeed(MAX_SPEED);
    stepper_shoulder.setAcceleration(ACCELERATION);
    arm_steppers.addStepper(stepper_shoulder);

    stepper_elbow.setMaxSpeed(MAX_SPEED);
    stepper_elbow.setAcceleration(ACCELERATION);
    arm_steppers.addStepper(stepper_elbow);

    stepper_wrist.setMaxSpeed(MAX_SPEED);
    stepper_wrist.setAcceleration(ACCELERATION);
    arm_steppers.addStepper(stepper_wrist);

    stepper_base.setMaxSpeed(MAX_SPEED);
    stepper_base.setAcceleration(ACCELERATION);
    arm_steppers.addStepper(stepper_base);

    stepper_roll.setMaxSpeed(MAX_SPEED);
    stepper_roll.setAcceleration(ACCELERATION);
    arm_steppers.addStepper(stepper_roll);

    gripper.attach(gripperPin);
}

void poll_for_new_coords(double (&move)[4]){
    //Poll serial connection for a new command from the CMController
    //This process has not been fully designed yet.
    move[0] = 25;
    move[1] = 10;
    move[2] = 7;
    move[3] = 180;
    move[4] = 1;
}

void actuate_gripper (int decision) {
    //Send signal to servo to make one full rotation
    //It only moves clockwise for now. Anticlockwise rotation is trivial but hasn't been implemented.

    if (decision > 0){
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

//Main motor control loop
void loop() {

    poll_for_new_coords(new_move);
    int w = 0;
    while(!Serial.available()){
      Serial.print("/rWaiting...");
      Serial.print(w);
      Serial.flush();
      w++;
    }
    if (new_move != previous_move){
        //VARIABLE MANAGEMENT*******************************
        //variable declerations
        long joint_steps[NUM_STEPPERS] = {0, 0, 0, 0, 0};  //Array to hold the steps for the stepper motors
        double coords[4];                 //3D coordinates of end point
        long origin[NUM_STEPPERS] = {0, 0, 0, 0, 0};
        int gripper_instruction;        //open or close gripper

        //get new move data
        Serial.print("\nPRE-CALC coords ********************\n");
        gripper_instruction = (int) new_move[4];
        for (int i = 0; i <= 4; i++)
        {
            coords[i] = new_move[i];
          if(debug){
              Serial.print("coords[");
              Serial.print(i);
              Serial.print("] = ");
              Serial.print(coords[i]);
              Serial.print("\n");
          }
        }
        //VARIABLE MANAGEMENT*******************************
        if(debug){
          Serial.print("\nPRE-CALC STEPS ********************\n");
          for(int i = 0; i < NUM_STEPPERS; i++)
          {
             Serial.print("steps[");
             Serial.print(i);
             Serial.print("] = ");
             Serial.print(joint_steps[i]);
             Serial.print("\n");
          }
        }
        calculate_steps(coords, joint_steps);
        if(debug){
          Serial.print("\nPOST-CALC STEPS ********************\n");
          for (int i = 0; i < NUM_STEPPERS; i++)
          {
             Serial.print("steps[");
             Serial.print(i);
             Serial.print("] = ");
             Serial.print(joint_steps[i]);
             Serial.print("\n");
          }
        }

        //execute the requested move
        arm_steppers.moveTo(joint_steps);
        arm_steppers.runSpeedToPosition();

        delay(500);
        actuate_gripper(gripper_instruction); //open or close the gripper as per
        delay(500);

        //Move arm back to origin so it can execute it's next move
        arm_steppers.moveTo(origin);
        arm_steppers.runSpeedToPosition();
        for(int i=0; i <= 3; ++i){
          previous_move[i] = new_move[i];
        }
    }
}
