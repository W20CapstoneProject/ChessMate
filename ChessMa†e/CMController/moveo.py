from numpy import radians, degrees
from math import sin, cos, tan, asin, acos, atan, atan2, sqrt
import matplotlib.pyplot as pyplot
import configparser

class MoveoArm:
    '''
    MoveoArm

    Data class for moveo arm. Will be used to enforce constraints on motor steps.
    '''

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.bone_1 = int(self.config['MOVEO']['bone_1'])
        self.bone_2 = int(self.config['MOVEO']['bone_2'])
        self.bone_3 = int(self.config['MOVEO']['bone_3'])
        self.base = BaseJoint(int(self.config['MOVEO']['base_constraint']))
        self.shoulder = ShoulderJoint(int(self.config['MOVEO']['shoulder_constraint']))
        self.elbow = ElbowJoint(int(self.config['MOVEO']['elbow_constraint']))
        self.wrist = WristJoint(int(self.config['MOVEO']['wrist_constraint']))
        self.grip = GripJoint(int(self.config['MOVEO']['grip_constraint']))


    def issueStepCommands(self, step1, step2, step3, step4, step5):
        '''
        Check constraints for each joint and return the allowed steps.
        '''
        base = self.base.issueSteps(step1)
        shoulder = self.shoulder.issueSteps(step2)
        elbow = self.elbow.issueSteps(step3)
        wrist = self.wrist.issueSteps(step4)
        grip = self.grip.issueSteps(step5)
        return base, shoulder, elbow, wrist, grip


class Joint:
    '''
    Parent class for joint behaviour and constraint enforcement.
    '''
    def __init__(self, constraint, position):
        self.constraint = constraint
        self.position = position

    def check_constraint(self, steps):
        if (self.position + steps <= self.constraint):
            return True
        else:
            return False

    def issueSteps(self, steps):
        if (self.check_constraint(steps) is True):
            return steps
        else:
            return self.constraint - self.position


class BaseJoint(Joint):

    def __init__(self, constraint):
        super().__init__(constraint, 0)


class ShoulderJoint(Joint):

    def __init__(self, constraint):
        super().__init__(constraint, 0)


class ElbowJoint(Joint):

    def __init__(self, constraint):
        super().__init__(constraint, 0)


class WristJoint(Joint):

    def __init__(self, constraint):
        super().__init__(constraint, 0)


class GripJoint(Joint):

    def __init__(self, constraint):
        super().__init__(constraint, 0)
