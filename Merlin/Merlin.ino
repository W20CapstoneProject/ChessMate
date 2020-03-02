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

//define pins
#include "Arduino.h"
#include "pin.h"
#include "IK_calc.h"
#include <AccelStepper.h>
#include <MultiStepper.h>


int stepPins[NUM_STEPPERS] = {stepPin_shoulder, stepPin_elbow, stepPin_wrist, stepPin_base, stepPin_roll};
int dirPins[NUM_STEPPERS] = {dirPin_shoulder, dirPin_elbow, dirPin_wrist, dirPin_base, dirPin_roll};
 
AccelStepper stepper_shoulder(AccelStepper::DRIVER, stepPins[0], dirPins[0]);
AccelStepper stepper_elbow(AccelStepper::DRIVER, stepPins[1], dirPins[1]);
AccelStepper stepper_wrist(AccelStepper::DRIVER, stepPins[2], dirPins[2]);
AccelStepper stepper_base(AccelStepper::DRIVER, stepPins[3], dirPins[3]);
AccelStepper stepper_roll(AccelStepper::DRIVER, stepPins[4], dirPins[4]);

MultiStepper arm_steppers;

double new_move[4];
double previous_move[4];

void setup(){
    //Setup all the pins for the stepper drivers
    pinMode(stepPin_shoulder, OUTPUT); //step pulse pin
    pinMode(dirPin_shoulder, OUTPUT);  //rotional direction control pin
    pinMode(enPin_shoulder, OUTPUT);   //enable/disable pin
    digitalWrite(enPin_shoulder, LOW); //initially disable the motors

    pinMode(stepPin_elbow, OUTPUT);
    pinMode(dirPin_elbow, OUTPUT);
    pinMode(enPin_elbow, OUTPUT);
    digitalWrite(enPin_elbow, LOW);

    pinMode(stepPin_wrist, OUTPUT);
    pinMode(dirPin_wrist, OUTPUT);
    pinMode(enPin_wrist, OUTPUT);
    digitalWrite(enPin_wrist, LOW);

    pinMode(stepPin_base, OUTPUT); 
    pinMode(dirPin_base, OUTPUT);
    pinMode(enPin_base, OUTPUT);
    digitalWrite(enPin_base, LOW);

    pinMode(stepPin_roll, OUTPUT); 
    pinMode(dirPin_roll, OUTPUT);
    pinMode(enPin_roll, OUTPUT);
    digitalWrite(enPin_roll, LOW);

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
}

//Main motor control loop
void loop() {

    poll_for_new_coords(new_move);
    if (new_move != previous_move){
        //VARIABLE MANAGEMENT*******************************
        //variable declerations
        long joint_steps[NUM_STEPPERS];  //Array to hold the steps for the stepper motors
        double coords[3];                 //3D coordinates of end point
        long origin[NUM_STEPPERS] = {0, 0, 0, 0, 0};
        int gripper_instruction;        //open or close gripper
        
        //get new move data
        gripper_instruction = (int) new_move[4];
        for (int i = 0; i <= 3; i++)
        {
            coords[i] = new_move[i];
        }
        //VARIABLE MANAGEMENT*******************************
        calculate_steps(coords, joint_steps);
        
        //execute the requested move
        arm_steppers.moveTo(joint_steps);
        arm_steppers.run();
        delay(500);
        //actuate_gripper(gripper_instruction); //open or close the gripper as per

        delay(500);

        //Move arm back to origin so it can execute it's next move
        arm_steppers.moveTo(origin);
        arm_steppers.run();
        for(int i=0; i<10; ++i){
          previous_move[i] = new_move[i];
        }
    }
}

void poll_for_new_coords(double* move){
    //Poll serial connection for a new command from the CMController
    //This process has not been fully designed yet.
}
