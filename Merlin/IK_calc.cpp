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

void calcIK_2R (double x, double y, double& theta0, double& theta1, double& theta2) {
    //Calculate the thetas for a 2 bone, 2 joint solutions. This is for test purposes
    // only at the moment.
    //INPUTS:
    // x = the 3D x coordinate for the end effector.
    // y = the 3D z coordinate for the end effector.
    // theta0,1,2 = the angles that the shoulder, elbow and wrist motors must achieve respectively.
    int sigma = 1;

    theta1 = sigma*acos((x*x + y*y - SHOULDER_LEN*SHOULDER_LEN - ELBOW_LEN*ELBOW_LEN)/(2*SHOULDER_LEN*ELBOW_LEN)); // For the simplified 2R solution the wrist theta is always 0.
    theta0 = atan(y/x) - atan((ELBOW_LEN*sin(theta2))/(SHOULDER_LEN+ELBOW_LEN*cos(theta2)));
}

void calcIK_3R (double x, double y, double phi, double& theta0, double& theta1, double& theta2) {
    //Calculate the thetas for a 3 bone, 3 joint solutions. For reference for these
    // equations check the documentation at the top of this file.
    //INPUTS:
    // x = the 3D x coordinate for the end effector.
    // y = the 3D z coordinate for the end effector.
    // theta0,1,2 = the angles that the shoulder, elbow and wrist motors must achieve respectively.

    int  sigma = 1; //Determines which solution to use for theta 1, we always want the one that give a theta < 90 degrees.
    double x_3 = 0;
    double y_3 = 0;

    //To simplify the equations we use some intermediary equations
    x_3 = (x - WRIST_LEN*cos(phi));
    y_3 = (y - WRIST_LEN*sin(phi));

    calcIK_2R(x_3, y_3, theta0, theta1, theta2);
    theta2 = phi - theta0 - theta1;

    // zeta = atan2(((-1*x_p)/pow((pow(x_p,2) + pow(y_p,2)), 0.5)), ((-1*x)/pow((pow(x_p, 2) + pow(y_p, 2)), 0.5)));

    // theta0 = zeta + sigma*acos((pow(x_p, 2) + pow(y_p, 2) + pow(SHOULDER_LEN, 2) - pow(ELBOW_LEN, 2))/(2*SHOULDER_LEN*pow((pow(x_p, 2) + pow(y_p, 2)), 0.5)));
    // theta1 = atan2(((y_p - SHOULDER_LEN*sin(theta0))/ELBOW_LEN), ((x_p - SHOULDER_LEN*cos(theta0))/ELBOW_LEN)) - theta0;
    // theta2 = gamma - (theta0 - theta1);
}

void calculate_steps (double* coords, long* steps) {
    double x = coords[0];
    double y = coords[1];
    double z = coords[2];
    double phi = coords[3];
    double shoulder_theta = 0;
    double elbow_theta = 0;
    double wrist_theta = 0;

//    shoulder_theta = x;
//    elbow_theta = y;
//    wrist_theta = z;

    //calcIK_2R(x, z, shoulder_theta, elbow_theta, wrist_theta);
    //calcIK_3R(z, x, phi, shoulder_theta, elbow_theta, wrist_theta);
    

//    steps[0] = (long) ((180.0*shoulder_theta)/(M_PI*STEP_ANGLE));
//    steps[1] = (long) ((180.0*elbow_theta)/(M_PI*STEP_ANGLE));
//    steps[2] = (long) ((180.0*wrist_theta)/(M_PI*STEP_ANGLE));
    steps[0] = (long) shoulder_theta;
    steps[1] = (long) elbow_theta;
    steps[2] = (long) wrist_theta;
    steps[3] = (long) ((180*atan(x/y))/(M_PI*STEP_ANGLE)); //base rotation steps
    steps[4] = 360;  //Wrist joint roll rotation steps. For now this motor is not being used, it will be for controling piece orientation later.
}
