from numpy import radians, degrees
from math import sin, cos, tan, asin, acos, atan, atan2, sqrt
import matplotlib.pyplot as pyplot
import configparser

from CMController.MoveoArm.moveo_arm import MoveoArm

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


    def solve_forward(self, o1, o2, o3):
        '''
        Solve the forward kinematics equation.
        '''
        x = self.l1*cos(o1) + self.l2*cos(o1+o2) + self.l3*cos(o1+o2+o3)
        y = self.l1*sin(o1) + self.l2*sin(o1+o2) + self.l3*sin(o1+o2+o3)
        phi = (o1 + o2 + o3)
        return x, y, phi


    def solve_2R(self, x, y):
        '''
        Solve the 2r planar manipulator inverse kinematics problem.
        '''
        #r =  sqrt(x*x + y*y)
        theta2 = (self.sigma)*acos((x*x + y*y - self.l1*self.l1 - self.l2*self.l2)/(2*self.l1*self.l2))
        theta1 = atan(y/x) - atan((self.l2*sin(theta2))/(self.l1+self.l2*cos(theta2)))
        return theta1, theta2


    def solve_inverse(self, x, y, phi):
        '''
        Solve the 3R inverse kinematics equation.
        '''
        x3 = x-self.l3*cos(phi)
        y3 = y-self.l3*sin(phi)
        o1,o2 = self.solve_2R(x3, y3)
        o3 = phi - o1 - o2
        return [o1, o2, o3]


    def jacobian(self):
        pass


class IKMapping:
    '''
    Map out results from inverse kinematics.
    '''
    def __init__(self):
        self.ik_engine = InverseKinematics()


    def plot_xy(self, n, m):
        ik = InverseKinematics()
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
                    x,y,phi = self.ik_engine.solve_forward(o1,o2,o3)
                    if((x>0) and (y>0)):
                        xs.append(x)
                        ys.append(y)
        pyplot.scatter(ys,xs)
        pyplot.show()
    
    
    def show_arm(self, o1, o2, o3, polar=False):
        x1 = self.ik_engine.l1*cos(o1)
        x2 = x1 + self.ik_engine.l2*cos(o1+o2)
        x3 = x2 + self.ik_engine.l3*cos(o1+o2+o3)
        y1 = self.ik_engine.l1*sin(o1)
        y2 = y1 + self.ik_engine.l2*sin(o1+o2)
        y3 = y2 + self.ik_engine.l3*sin(o1+o2+o3)

        r1 = self.ik_engine.l1
        r2 = (x2*x2 + y2*y2)**0.5
        r3 = (x3*x3 + y3*y3)**0.5

        if(polar):
            y_vals = [0, r1, r2, r3]
            x_vals = [0, o1, o1+o2, o1+o2+o3]
            pyplot.polar(x_vals, y_vals)
        else:
            x_vals = [0, x1, x2, x3]
            y_vals = [0, y1, y2, y3]
            pyplot.plot(y_vals, x_vals)
        pyplot.show()

        return x_vals, y_vals
