#ifndef _IK_calc_h_
#define _IK_calc_h_

#include "math.h"
#include "stepper_config.h"
#define DEBUG 1
#define SHOULDER_LEN 30.0
#define ELBOW_LEN 30.0
#define WRIST_LEN 10.0

//Function prototypes
void calcIK_2R(double, double, double*, double*, double*);
void calcIK_3R(double, double, double*, double*, double*);
void calculate_steps(double*, long*);
#endif
