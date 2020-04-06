class Joint:
    '''
    Parent class for joint behaviour and constraint enforcement.
    Each joint will be used to keep track of its own current position based on the command history while instantiated.
    A typical command flow may be as follows:
        1. Call calculate_steps() to determine the desired stepper motions.
        2. Call issue_steps() to check the constraints of the joints, update current position

    Joint constraints represent the highest degree of movement for the joint from zero.
    '''

    step_position = 0
    degree_position = 0

    def __init__(self, max_constraint, min_constraint, gear_ratio):
        self.max_constraint = max_constraint
        self.min_constraint = min_constraint
        self.gear_ratio = gear_ratio
        self.steps_per_rev = 400
        self.step_ratio = (360/self.steps_per_rev)

    def get_max_constraint(self):
        ''' Returns the max degree constraint of the arm. '''
        return self.max_constraint

    def get_min_constraint(self):
        ''' Returns the min degree constraint of the arm. '''
        return self.min_constraint


    def get_position(self):
        return self.step_position
    
    def set_position(self, position):
        self.step_position = position



    def check_constraints(self, steps):
        ''' 
        Using the given constraint of the joint, check to see if move based on steps will fit within constraint.
        Return - True if the steps will be allowed under the joint constraint.
        '''
        degrees = (self.step_position + steps) * (self.step_ratio/self.gear_ratio)
        if (degrees <= self.max_constraint and degrees >= self.min_constraint):
            return True
        else:
            return False


    def calculate_steps(self, degrees):
        '''
        Used to calculate the steps required for the stepper motors given the desired degree increase.
        1. Divide the degrees by the step ratio of 0.9
        2. Multiply by the gear ratio
        Return steps required to achieve the given degrees of rotation
        '''
        return (degrees / self.step_ratio) * self.gear_ratio


class Base(Joint):
    ''' Base stepper of Moveo arm. '''
    def __init__(self):
        super().__init__(max_constraint = 180, min_constraint = -180, gear_ratio = 10.0)
        

class Shoulder(Joint):
    ''' Shoulder stepper of Moveo arm. '''
    def __init__(self):
        super().__init__(max_constraint = 45, min_constraint = -45, gear_ratio = 5.4)
   

class Elbow(Joint):
<<<<<<< HEAD
    ''' Elbow stepper of Moveo arm. '''
    def __init__(self):
        super().__init__(max_constraint = 35, min_constraint = -35, gear_ratio = 20)
=======
# Elbow joint of Moveo arm.
    def __init__(self, constraint = 200, position = 0, gear_ratio = 21.7):
        super().__init__(constraint, position, gear_ratio)
>>>>>>> master
   

class Roll(Joint):
    ''' Roll stepper of Moveo arm. '''
    def __init__(self):
        super().__init__(max_constraint = 35, min_constraint = -35, gear_ratio = 10.0)


class Wrist(Joint):
    ''' Wrist stepper of Moveo arm. '''
    def __init__(self):
        super().__init__(max_constraint = 35, min_constraint = -35, gear_ratio = 10.0)
        

class Grip(Joint):
    ''' Grip servo of Moveo arm. '''
    def __init__(self):
        super().__init__(max_constraint = 90, min_constraint = -90, gear_ratio = 1.0)
    