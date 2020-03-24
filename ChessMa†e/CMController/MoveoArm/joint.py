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

    def issue_steps(self, steps):
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
