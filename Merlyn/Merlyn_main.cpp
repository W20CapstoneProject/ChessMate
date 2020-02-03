

//define pins
#include <pin.h>
#include <stepper_config.h>
#include <AccelStepper.h>
#include <MultiStepper.h>

AccelStepper steppers[NUM_STEPPERS] = {
    AccelStepper shoulder_stepper = AccelStepper(INTERFACE_TYPE ,stepPin_shoulder, dirPin_shoulder),
    AccelStepper elbow_stepper = AccelStepper(INTERFACE_TYPE ,stepPin_elbow, dirPin_elbow),
    AccelStepper wrist_stepper = AccelStepper(INTERFACE_TYPE ,stepPin_wrist, dirPin_wrist),
    AccelStepper base_stepper = AccelStepper(INTERFACE_TYPE ,stepPin_base, dirPin_base),
    AccelStepper roll_stepper = AccelStepper(INTERFACE_TYPE ,stepPin_roll, dirPin_roll)
};
MultiStepper arm_steppers;

long* new_move[4];
long* previous_move[4];

void setup(){
    //Setup all the pins for the stepper drivers
    pinMode(stepPin_shoulder, OUTPUT);
    pinMode(dirPin_shoulder, OUTPUT);
    pinMode(enPin_shoulder, OUTPUT);
    digitalWrite(enPin_shoulder, LOW);

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
    digitalWrite(enPin_, LOW);

    //Configure stepper parameters and add them all to the MultiStepper
    // controller
    for (int i = 0; i <= NUM_STEPPERS; i++)
    {
        steppers[i].setMaxSpeed(MAX_SPEED);
        steppers[i].setAcceleration(ACCELERATION);
        arm_steppers.addStepper(&(steppers[i]));
    }
}

//Main motor control loop
void loop() {
    poll_for_new_coords(new_move);
    if (new_move != previous_move){
        //VARIABLE MANAGEMENT*******************************
        //variable declerations
        int joint_steps[NUM_STEPPERS];  //Array to hold the steps for the stepper motors
        long coords[3];                 //3D coordinates of end point
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
        actuate_gripper(gripper_instruction); //open or close the gripper as per

        delay(500);

        //Move arm back to origin so it can execute it's next move
        arm_steppers.moveTo([0, 0, 0, 0, 0]);
        arm_steppers.run();
        previous_move = new_move;
    }
}

void poll_for_new_coords(long* move){
    //Poll serial connection for a new command from the CM system
}