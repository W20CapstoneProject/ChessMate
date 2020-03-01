//Creation Date: February 2nd, 2020
//Original Author: Erik Lewis
//Description: This code will  perform the inverse kinematics calculations
//              necessary to convert the 3 dimensional
//              coordinates received from the CMController 
//              into steps for the motors such that the arm's
//              end effector will reach the desired end point.

//IK reference material: http://www.ryanjuckett.com/programming/analytic-two-bone-ik-in-2d/
//                      http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.65.5698&rep=rep1&type=pdf
//FORWARD KINEMATICS EQUATIONS
//These are what was use to derive the IK equations use here.
// NOTE: <x, y, gamma> = the end effector coordinates.
// x     = L1*cos(theta0) + L2*cos(theta0 + theta1) + L3*cos(theta0 + theta1 + theta2)
// y     = L1*sin(theta0) + L2*sin(theta0 + theta2) + L3*sin(theta0 + theta1 + theta2)
// gamma = (theta0 + theta1 + theta3)
// These can be combined to form the nonlinear equation with some helpers...
//  x_p = (x - WRIST_LEN*cos(gamma));
//  y_p = (y - WRIST_LEN*sin(gamma));
// (-2*L1*x_p)*cos(theta0) + (-2*L1*y_p)*sin(theta1) + (x_p^2 + y_p^2 + L1^2 - L2^2)

#include <math.h>
#include "stepper_config.h"
#define DEBUG 1
#define SHOULDER_LEN 30.0
#define ELBOW_LEN 30.0
#define WRIST_LEN 10.0

void calcIK_2R (double x, double y, double* theta0, double* theta1, double* theta2){
    //We are assuming the arm is always moving to a positive inner angle
    // that is to say that the joints will only ever move in a clockwise
    // rotation when reaching forward for now.
    double y_new = 0.0;
    int sigma = -1;

    
    y_new = y+WRIST_LEN;

    theta2 = 0; // For the simplified 2R solution the wrist theta is always 0.
    theta1 = sigma*acos((x^2 + y_new^2 - SHOULDER_LEN^2 - ELBOW_LEN^2)/(2*SHOULDER_LEN*ELBOW_LEN));
    theta0 = atan(y_new/x) - sigma*atan((ELBOW_LEN*sin(theta1))/(SHOULDER_LEN + ELBOW_LEN*cos(theta1)));
}

void calcIK_3R (double x, double y, double* theta0, double* theta1, double* theta2){
    
    int  sigma = -1; //Determines which solution to use for theta 1
    double gamma = 90; //This is the angle we want to wrist bone to make with the x-axis. For now it's always going to be 90 degrees.
    double x_p = 0;
    double y_p = 0;
    double zeta = 0;
    double *pargs;

    //To simplify the equations we use some intermediary equations
    x_p = (x - WRIST_LEN*cos(gamma));
    y_p = (y - WRIST_LEN*sin(gamma));
    zeta = atan2(((-1*x_p)/(x_p^2 + y_p^2)^0.5), ((-1*x)/(x_p^2 + y_p^2)^0.5));

    theta0 = zeta + sigma*acos((x_p^2 + y_p^2 + SHOULDER_LEN^2 - ELBOW_LEN^2)/(2*SHOULDER_LEN*(x_p^2 + y_p^2^0.5));
    theta1 = atan2(((y_p - SHOULDER_LEN*sin(theta0))/ELBOW_LEN), ((x_p - SHOULDER_LEN*cos(theta0))/ELBOW_LEN));
    theta2 = gamma - (theta0 - theta1);
}

void calculate_steps (double* coords, int* steps) {
    double x = coords[0];
    double y = coords[1];
    double z = coords[2];
    double shoulder_theta = 0;
    double elbow_theta = 0;
    double wrist_theta = 0;

    calcIK_2R(x, z, &shoulder_theta, &elbow_theta, &wrist_theta);
    calcIK_3R(x, z, &shoulder_theta, &elbow_theta, &wrist_theta);

    steps[0] = (int) (shoulder_theta/STEP_ANGLE);
    steps[1] = (int) (elbow_theta/STEP_ANGLE);
    steps[2] = (int) (wrist_theta/STEP_ANGLE);
    steps[3] = (int) (tan(x/y)/STEP_ANGLE); //base rotation steps
    steps[4] = 0;  //wrist joint roll rotation steps. For now this motor is not being used, it will be for controling piece orientation later
}