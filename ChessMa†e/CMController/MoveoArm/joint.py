class Joint:
    '''
    Parent class for joint behaviour and constraint enforcement.
    '''
    def __init__(self, constraint, position, gear_ratio):
        self.constraint = constraint
        self.step_position = position
        self.gear_ratio = gear_ratio
        self.steps_per_rev = 400
        self.step_ratio = 0.9

    def check_constraint(self, steps):
        '''
        Using the given constraint of the joint, check to see if move based on steps will fit within constraint.
        '''
        if (self.step_position + steps <= self.constraint):
            return True
        else:
            return False

    def issue_steps(self, steps):
        '''
        Not sure if this is require as of yet.
        '''
        if (self.check_constraint(steps) is True):
            return steps
        else:
            return self.constraint - self.step_position

    def calculate_steps(self, degrees):
        '''
        Used to calculate the steps required for the stepper motors given the desired degree increase.
        1. Divide the degrees by the step ratio of 0.9
        2. Multiply by the gear ratio
        '''
        return (degrees / self.step_ratio) * self.gear_ratio



class BaseJoint(Joint):
# Base joint of Moveo arm.
    def __init__(self, constraint = 30, position = 0, gear_ratio = 1.0):
        super().__init__(constraint, position, gear_ratio)
        


class ShoulderJoint(Joint):
# Shoulder joint of Moveo arm.
    def __init__(self, constraint = 30, position = 0, gear_ratio = 5.4):
        super().__init__(constraint, position, gear_ratio)
   

class ElbowJoint(Joint):
# Elbow joint of Moveo arm.
    def __init__(self, constraint = 30, position = 0, gear_ratio = 1.0):
        super().__init__(constraint, position, gear_ratio)
   


class WristJoint(Joint):
# Wrist joint of Moveo arm.
    def __init__(self, constraint = 30, position = 0, gear_ratio = 1.0):
        super().__init__(constraint, position, gear_ratio)
        


class GripJoint(Joint):
# Grip joint of Moveo arm.
    def __init__(self, constraint = 30, position = 0, gear_ratio = 1.0):
        super().__init__(constraint, position, gear_ratio)
    
