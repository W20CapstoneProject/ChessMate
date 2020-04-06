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

#include <stdio.h>      /* printf, NULL */
#include <stdlib.h>     /* strtod */
#include <string.h>     /* strtok */



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


double new_move[NEW_MOVE_SIZE];
double previous_move[NEW_MOVE_SIZE];

void setup(){
    Serial.begin(9600);

    for (int i = 0; i < NUM_STEPPERS; i++){
      pinMode(stepPins[i], OUTPUT); //step pulse pin
      pinMode(dirPins[i], OUTPUT);  //rotional direction control pin
      pinMode(enPins[i], OUTPUT);   //enable/disable pin
      digitalWrite(enPins[i], LOW); //initially disable the motors
    }

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

void poll_for_new_coords(double (&move)[NEW_MOVE_SIZE]){
    //Poll serial connection for a new command from the CMController
    //This process has not been fully designed yet.
    size_t data_len;
    char * buff;
    char * tokenized_buff;
    int coord_buff_size = (4*(NEW_MOVE_SIZE+1))+5 //NEW_MOVE_SIZE number of comma seperated values of length 4.
    int i = 0;

    while(!Serial.available()){}
    //Once we receive data
    data_len = Serial.readBytes(buff, coord_buff_size); // expects something like "1000,0200,0030,0004,0050,0000"
    tokenized_buff = strtok(buff,",");
    while(tokenized_buff != NULL){
      move[i] = strtod(tokenized_buff, NULL);
      tokenized_buff = strtok(NULL, ",");
      i++;
    }
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
    if (new_move != previous_move){
        //VARIABLE MANAGEMENT*******************************
        //variable declerations
        long joint_steps[NUM_STEPPERS] = {0, 0, 0, 0, 0};  //Array to hold the steps for the stepper motors
        long origin[NUM_STEPPERS] = {0, 0, 0, 0, 0};
        int gripper_instruction;        //open or close gripper

        gripper_instruction = (int) new_move[NEW_MOVE_SIZE-1];
        //VARIABLE MANAGEMENT*******************************

        //execute the requested move
        //Run all motors to positions
        //arm_steppers.runSpeedToPosition();

        actuate_gripper(gripper_instruction); //open or close the gripper as per

        //Move arm back to origin so it can execute it's next move
        // arm_steppers.moveTo(origin);
        // arm_steppers.runSpeedToPosition();
        for(int i=0; i < NEW_MOVE_SIZE; ++i){
          previous_move[i] = new_move[i];
        }
    }
}
