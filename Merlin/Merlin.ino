//Creation Date: February 2nd, 2020
//Updated: April 8th, 2020
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
#define NEW_MOVE_SIZE 29
#define shoulder_speed 600
#define shoulder_acc 150

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



int stepPins[NUM_STEPPERS] = {stepPin_base, stepPin_shoulder, stepPin_elbow, stepPin_wrist};
int dirPins[NUM_STEPPERS]  = {dirPin_base, dirPin_shoulder, dirPin_elbow, dirPin_wrist};
int enPins[NUM_STEPPERS]   = {enPin_base, enPin_shoulder, enPin_elbow, enPin_wrist};
//Unfortunately there is no way to initlize these as an array. It must be individual objects.
AccelStepper stepper_base(AccelStepper::DRIVER, stepPins[0], dirPins[0]);
AccelStepper stepper_shoulder(AccelStepper::DRIVER, stepPins[1], dirPins[1]);
AccelStepper stepper_elbow(AccelStepper::DRIVER, stepPins[2], dirPins[2]);
AccelStepper stepper_wrist(AccelStepper::DRIVER, stepPins[3], dirPins[3]);

MultiStepper arm_steppers;

Servo gripper;


int new_move[NEW_MOVE_SIZE];
double previous_move[NEW_MOVE_SIZE];
int pos = 180;

bool flag = true;


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
    stepper_shoulder.setMaxSpeed(shoulder_speed);
    stepper_shoulder.setAcceleration(shoulder_acc);
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

//    stepper_roll.setMaxSpeed(MAX_SPEED); //would normally include, but roll joint is disabled
//    stepper_roll.setAcceleration(ACCELERATION);
//    arm_steppers.addStepper(stepper_roll);

    gripper.attach(gripperPin);
}

void poll_for_new_coords(){
    //Poll serial connection for a new command from the CMController
    //This process has not been fully designed yet.]
    String input;
    int data_len;
    int len = 34;
    char buff[50];
    char * tokenized_buff;
    int i = 0;



    while(!Serial.available()){}
    //Once we receive data
      input = Serial.readString();
      strcpy(buff, input.c_str()); 
      tokenized_buff = strtok(buff,",");
      while(tokenized_buff != NULL){
        new_move[i] = strtod(tokenized_buff, NULL);
        tokenized_buff = strtok(NULL, ",");
        i++;
      }
      Serial.println("ACK");

}

void actuate_gripper (int decision) {
    //Send signal to servo to make one full rotation
    while(!(pos==decision)){
      gripper.write(pos);
      delay(5);
      if(pos>decision){pos--;}
      else{pos++;}
      }
}

//Main motor control loop
void loop() {


    poll_for_new_coords();
    //VARIABLE MANAGEMENT*******************************
    //variable declerations
    int joint_steps[NUM_STEPPERS] = {0, 0, 0, 0};  //Array to hold the steps for the stepper motors
    int origin[NUM_STEPPERS] = {0, 0, 0, 0};
    int gripper_instruction;        //open or close gripper
    
    for (int i = 0; i < NUM_STEPPERS; i++){
      joint_steps[i] = new_move[i];
    }
    gripper_instruction = new_move[4];
    //VARIABLE MANAGEMENT*******************************

    //execute the requested move
    //Run all motors to positions

    delay(100);
    
    stepper_base.moveTo(joint_steps[0]);
    stepper_shoulder.moveTo(joint_steps[1]);
    stepper_elbow.moveTo(joint_steps[2]);
    stepper_wrist.moveTo(joint_steps[3]);

    //wait for all moves to finish then actuate_gripper
    while( !((stepper_shoulder.distanceToGo()+stepper_elbow.distanceToGo()+stepper_wrist.distanceToGo()+stepper_base.distanceToGo()) == 0)){
      stepper_shoulder.run();
      stepper_elbow.run();
      stepper_wrist.run();
      stepper_base.run();
      }

      actuate_gripper(gripper_instruction); //1:open 0:close

    Serial.println("OK!");
}
