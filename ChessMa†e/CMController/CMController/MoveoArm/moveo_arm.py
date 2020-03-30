from CMController.MoveoArm.joint import Base, Shoulder, Elbow, Wrist, Grip


class MoveoArm:
    '''
    MoveoArm

    Data class for moveo arm. Will be used to enforce constraints on motor steps.
    '''

    def __init__(self):
        self.postion = (0,0,0,0,0)
        self.bone_1 = 220
        self.bone_2 = 220
        self.bone_3 = 95
        self.base = Base()
        self.shoulder = Shoulder()
        self.elbow = Elbow()
        self.wrist = Wrist()
        self.grip = Grip()
        self.precision = 5
        

    def check_constraints(self, base_steps, shoulder_steps, elbow_steps, wrist_steps):
        '''
        Check constraints for each joint and return the allowed steps.

        Move to dictionary format for issuing steps.
        '''
        base = self.base.check_constraint(base_steps)
        shoulder = self.shoulder.check_constraint(shoulder_steps)
        elbow = self.elbow.check_constraint(elbow_steps)
        wrist = self.wrist.check_constraint(wrist_steps)
        return (base, shoulder, elbow, wrist)

    def is_steps_allowed(self, steps):
        responses = self.check_constraints(steps[0], steps[1], steps[2], steps[3])
        for response in responses:
            if (response is False):
                return False
        return True


    def calculate_steps(self, base_d, shoulder_d, elbow_d, wrist_d):
        '''
        Given the desired degrees for rotation, calculate the steps for each motor.
        This function assumes that the current position of the joints are all at zero/origin.

        Returns steps for each controlled joint
        '''
        base_steps = round(self.base.calculate_steps(base_d), self.precision)
        shoulder_steps = round(self.shoulder.calculate_steps(shoulder_d), self.precision)
        elbow_steps = round(self.elbow.calculate_steps(elbow_d), self.precision)
        wrist_steps = round(self.wrist.calculate_steps(wrist_d), self.precision)
        return (base_steps, shoulder_steps, elbow_steps, wrist_steps)


    def update_position(self, new_position):
        '''
        Updates the current position of the stepper motors. The position object 
        contains the current step position of each motor.
        '''
        base = self.base.get_position()
        shoulder = self.shoulder.get_position()
        elbow = self.elbow.get_position()
        wrist = self.wrist.get_position()
        grip = self.grip.get_position()
        self.position = (base, shoulder, elbow, wrist, grip)
        

