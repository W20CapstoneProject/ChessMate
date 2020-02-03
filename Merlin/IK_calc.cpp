//Creation Date: February 2nd, 2020
//Original Author: Erik Lewis
//Description: This code will  perform the inverse kinematics calculations
//              necessary to convert the 3 dimensional
//              coordinates received from the CMController 
//              into steps for the motors such that the arm's
//              end effector will reach the desired end point.

//IK reference material http://www.ryanjuckett.com/programming/analytic-two-bone-ik-in-2d/

#include <math.h>
#include <stepper_config.h>
#define WRIST_LEN 10.0

void calculate_steps (long* coords, int* steps){
    //We are assuming the arm is always moving to a positive inner angle
    // that is to say that the joints will only ever move in a clockwise
    // rotation for now.
    long x = coords[0];
    long y = coords[1];
    long z = coords[2];
    long dist_to_target = 0;
    long height = 0;
    long hypotenous;
    long negative_shoulder_theta0;
    long negative_shoulder_theta1;
    long *pargs;

    dist_to_target = (x^2 + y^2)^(0.5);
    height = z+WRIST_LEN;

    hypotenous = (dist_to_target^2 + height^2);

    negative_shoulder_theta0 = tan(height/dist_to_target);
    negative_shoulder_theta1 = arccos((hypotenous^2 + r^2 - height^2)/(2*hypotenous*dist_to_target));

    shoulder_theta = 90-(negative_shoulder_theta0 + negative_shoulder_theta1);
    elbow_theta = 180-(arccos((height^2 + hypotenous^2 - dist_to_target^2)/(2*height*hypotenous)));
    wrist_theta = calc_wrist_theta(pargs);

    steps[0] = (int) (shoulder_theta/STEP_ANGLE);
    steps[1] = (int) (elbow_theta/STEP_ANGLE);
    steps[2] = (int) (wrist_theta/STEP_ANGLE);
    steps[3] = (int) (tan(x/y)/STEP_ANGLE); //base rotation steps
    steps[4] = 0;  //wrist joint roll rotation steps. For now this motor is not being used, it will be for controling piece orientation later
}

//Helper function
void calc_wrist_theta(long* pargs){
    //Caculate the angle the wrist needs to move relative
    // to elbow joint such that it is parallel to y-axis
    //This calculation is slightly complex and is still being
    // optimized.
}