//Creation Date: February 2nd, 2020
//Last Edited: March 2nd, 2020
//Original Author: Erik Lewis
//Edited by: Erik Lewis
//Description: This code will  perform the inverse kinematics calculations
//              necessary to convert the 3 dimensional
//              coordinates received from the CMController 
//              into steps for the motors such that the arm's
//              end effector will reach the desired end point.

//IK reference material: http://www.ryanjuckett.com/programming/analytic-two-bone-ik-in-2d/
//                      https://www.seas.upenn.edu/~meam520/notes02/IntroRobotKinematics5.pdf
//                      http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.65.5698&rep=rep1&type=pdf
//FORWARD KINEMATICS EQUATIONS
//These are what was use to derive the IK equations we use here.
// NOTE: <x, y, gamma> = the end effector coordinates.
// x     = L1*cos(theta0) + L2*cos(theta0 + theta1) + L3*cos(theta0 + theta1 + theta2)
// y     = L1*sin(theta0) + L2*sin(theta0 + theta2) + L3*sin(theta0 + theta1 + theta2)
// gamma = (theta0 + theta1 + theta3)
// These can be combined to form the nonlinear equation with some helpers...
//  x_p = (x - L3*cos(gamma));
//  y_p = (y - L3*sin(gamma));
// (-2*L1*x_p)*cos(theta0) + (-2*L1*y_p)*sin(theta1) + (x_p^2 + y_p^2 + L1^2 - L2^2)

#include "IK_calc.h"

void calcIK_2R (double x, double y, double* theta0, double* theta1, double* theta2) {
    //Calculate the thetas for a 2 bone, 2 joint solutions. This is for test purposes
    // only at the moment.
    //INPUTS:
    // x = the 3D x coordinate for the end effector.
    // y = the 3D z coordinate for the end effector.
    // theta0,1,2 = the angles that the shoulder, elbow and wrist motors must achieve respectively.

    double y_new = 0.0;
    int sigma = -1;

    
    y_new = y+WRIST_LEN;

    *theta2 = 0; // For the simplified 2R solution the wrist theta is always 0.
    *theta1 = sigma*acos((pow(x, 2) + pow(y_new, 2) - pow(SHOULDER_LEN, 2) - pow(ELBOW_LEN, 2))/(2*SHOULDER_LEN*ELBOW_LEN));
    *theta0 = atan(y_new/x) - sigma*atan((ELBOW_LEN*sin((*theta1)))/(SHOULDER_LEN + ELBOW_LEN*cos((*theta1))));
}

void calcIK_3R (double x, double y, double* theta0, double* theta1, double* theta2) {
    //Calculate the thetas for a 3 bone, 3 joint solutions. For reference for these
    // equations check the documentation at the top of this file.
    //INPUTS:
    // x = the 3D x coordinate for the end effector.
    // y = the 3D z coordinate for the end effector.
    // theta0,1,2 = the angles that the shoulder, elbow and wrist motors must achieve respectively.

    int  sigma = -1; //Determines which solution to use for theta 1, we always want the one that give a theta < 90 degrees.
    double gamma = 90; //This is the angle we want to wrist bone to make with the x-axis. For now it's always going to be 90 degrees.
    double x_p = 0;
    double y_p = 0;
    double zeta = 0;
    double *pargs;

    //To simplify the equations we use some intermediary equations
    x_p = (x - WRIST_LEN*cos(gamma));
    y_p = (y - WRIST_LEN*sin(gamma));
    zeta = atan2(((-1*x_p)/pow((pow(x_p,2) + pow(y_p,2)), 0.5)), ((-1*x)/pow(( pow(x_p, 2) + pow(y_p, 2)), 0.5)));

    *theta0 = zeta + sigma*acos((pow(x_p, 2) + pow(y_p, 2) + pow(SHOULDER_LEN, 2) - pow(ELBOW_LEN, 2))/(2*SHOULDER_LEN*pow((pow(x_p, 2) + pow(y_p, 2)), 0.5)));
    *theta1 = atan2(((y_p - SHOULDER_LEN*sin((*theta0)))/ELBOW_LEN), ((x_p - SHOULDER_LEN*cos((*theta0)))/ELBOW_LEN));
    *theta2 = gamma - ((*theta0) - (*theta1));
}

void calculate_steps (double* coords, long* steps) {
    double x = coords[0];
    double y = coords[1];
    double z = coords[2];
    double shoulder_theta = 0;
    double elbow_theta = 0;
    double wrist_theta = 0;

    //calcIK_2R(x, z, &shoulder_theta, &elbow_theta, &wrist_theta);
    calcIK_3R(x, z, &shoulder_theta, &elbow_theta, &wrist_theta);

    steps[0] = (long) (shoulder_theta/STEP_ANGLE);
    steps[1] = (long) (elbow_theta/STEP_ANGLE);
    steps[2] = (long) (wrist_theta/STEP_ANGLE);
    steps[3] = (long) (tan(x/y)/STEP_ANGLE); //base rotation steps
    steps[4] = 0;  //Wrist joint roll rotation steps. For now this motor is not being used, it will be for controling piece orientation later.
}
