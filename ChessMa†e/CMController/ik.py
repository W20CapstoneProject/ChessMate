from numpy import radians, degrees
from math import sin, cos, tan, asin, acos, atan, atan2, sqrt
import matplotlib.pyplot as pyplot
import configparser
from moveo import MoveoArm

class InverseKinematics:
    '''
    InverseKinematics

    This class calculates the required steps for the robotic action using inverse kinematics.
    '''

    def __init__(self):
        self.arm = MoveoArm()
        self.l1 = self.arm.bone_1
        self.l2 = self.arm.bone_2
        self.l3 = self.arm.bone_3
        self.sigma = 1


    def forward(self, o1, o2, o3):
        '''
        Solve the forward inverse kinematics equation.
        '''
        x = self.l1*cos(o1) + self.l2*cos(o1+o2) + self.l3*cos(o1+o2+o3)
        y = self.l1*sin(o1) + self.l2*sin(o1+o2) + self.l3*sin(o1+o2+o3)
        phi = (o1 + o2 + o3)
        return x,y,phi


    def solve2R(self, x, y):
        '''
        Solve the 2r planar manipulator inverse kinematics problem.
        '''
        #r =  sqrt(x*x + y*y)
        theta2 = (sigma)*acos((x*x + y*y - self.l1*self.l1 - self.l2*self.l2)/(2*self.l1*self.l2))
        theta1 = atan(y/x) - atan((self.l2*sin(theta2))/(self.l1+self.l2*cos(theta2)))
        return theta1, theta2


    def inverse(self, x, y, phi):
        '''
        Solve the inverse kinematics equation.
        '''
        x3 = x-l3*cos(phi)
        y3 = y-l3*sin(phi)
        o1,o2 = solve2R(x3, y3)
        o3 = phi - o1 - o2
        return [o1, o2, o3]


class IKMapping:
    '''
    Map out results from inverse kinematics.
    '''

    def plotxy(self, n, m):
        xs = list()
        ys = list()
        x1 = list()
        x2 = list()
        x3 = list()
        for i in range(0, 180):
            if (i < n):
                x1.append(radians(i))
            if (i < m):
                x2.append(radians(i))
            x3.append(radians(i))
        for o1 in x1:
            for o2 in x2:
                for o3 in x3:
                    x,y,phi = forward(o1,o2,o3)
                    if((x>0) and (y>0)):
                        xs.append(x)
                        ys.append(y)
        pyplot.scatter(ys,xs)
        pyplot.show()
