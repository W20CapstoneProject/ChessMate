from numpy import radians, degrees
from math import sin, cos, tan, asin, acos, atan, atan2, sqrt
import matplotlib.pyplot as pyplot

class MoveoGeometric3DOF:
    '''
    Alternative IK calculations based on a 3DOF model for the arm.
    '''
    precision = 3

    def __init__(self):
        self.arm = MoveoArm()
        self.d1 = self.arm.bone_1
        self.d2 = self.arm.bone_2
        self.d3 = self.arm.bone_3
        self.sigma = 1

    def calculate_r(self, x, y, z):
        ''' Calculate the distance from the origin to the end effector. '''
        r = sqrt(x*x + y*y + z*z)
        return round(r, self.precision)

    def calculate_base(self, x, y):
        ''' Returns the desired degrees of rotation for the base. '''
        base = atan(y/x)
        return round(base, self.precision)

    def calculate_elbow(self, x, y, z)
        ''' Returns the desired degrees of rotation for the elbow. '''
        elbow = -acos((x*x + y*y + z*z - self.d1*self.d1*self.d2*self.d2)/(2*self.d1*self.d2))
        return round(elbow, self.precision)

    def calculate_shoulder(self, x, y, z, elbow):
        ''' Returns the desired degrees of rotation for the shoulder. '''
        r = self.calculate_r(x,y,z)
        shoulder = asin(z/r) + atan((self.d2*sin(elbow))/(self.d1 + self.d2*cos(elbow)))
        return round(shoulder, self.precision)

    def solve_inverse(self, x, y, z):
        ''' Solves the inverse kinematics equations for a 3DOF robotic arm. '''
        base = calculate_base(x, y, z)
        elbow = calculate_elbow(x, y, z)
        shoulder = calculate_shoulder(x, y, z, elbow)
        return base, shoulder, elbow
