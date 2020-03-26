from numpy import radians, degrees
from math import sin, cos, tan, asin, acos, atan, atan2, sqrt
import matplotlib.pyplot as pyplot
import configparser
import serial
from .joint import BaseJoint, ShoulderJoint, ElbowJoint, WristJoint, GripJoint


class MoveoArm:
    '''
    MoveoArm

    Data class for moveo arm. Will be used to enforce constraints on motor steps.
    '''

    def __init__(self):
        self.bone_1 = 220
        self.bone_2 = 220
        self.bone_3 = 95
        self.base = BaseJoint()
        self.shoulder = ShoulderJoint()
        self.elbow = ElbowJoint()
        self.wrist = WristJoint()
        self.grip = GripJoint()

    def check_constraints(self, steps):
        '''
        Check constraints for each joint and return the allowed steps.

        Move to dictionary format for issuing steps.
        '''
        base = self.base.issue_steps(steps[0])
        shoulder = self.shoulder.issue_steps(steps[1])
        elbow = self.elbow.issue_steps(steps[2])
        wrist = self.wrist.issue_steps(steps[3])
        grip = self.grip.issue_steps(steps[4])
        return (base, shoulder, elbow, wrist, grip)

    def calculate_steps(self, degrees):
        pass

    def update_position(self):
        pass

    def calibrate(self):
        pass
