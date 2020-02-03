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

void loop() {
    poll_for_new_coords(new_move);
    if (new_move != previous_move){
        //variable declerations
        int joint_steps[NUM_STEPPERS];
        long coords[3];
        int gripper_instruction;
        //get new move data
        gripper_instruction = (int) new_move[4];
        for (int i = 0; i <= 3; i++)
        {
            coords[i] = new_move[i];
        }

        calculate_steps(coords, joint_steps);
        
        //
        arm_steppers.moveTo(joint_steps);
        arm_steppers.run();
        actuate_gripper(gripper_instruction);

        arm_steppers.moveTo([0, 0, 0, 0, 0]);
        arm_steppers.run();
        previous_move = new_move; //
    }
}

// void control_steppers(int* joint_steps) {

    
//     // for (int i = 0; i <= NUM_STEPPERS; i++)
//     // {
//     //     //Eventually this should be threaded per stepper
//     //     steppers[i].moveTo(joint_steps[i])
//     // }
// }
