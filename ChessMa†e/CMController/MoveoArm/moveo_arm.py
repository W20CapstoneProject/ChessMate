from .joint import BaseJoint, ShoulderJoint, ElbowJoint, WristJoint, GripJoint


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
        return (base, shoulder, elbow, wrist)


    def calculate_steps(self, base_d, shoulder_d, elbow_d, wrist_d):
        '''
        Given the desired degrees for rotation, calculate the steps for each motor.
        '''
        base_steps = self.base.calculate_steps(base_d)
        shoulder_steps = self.shoulder.calculate_steps(shoulder_d)
        elbow_steps = self.elbow.calculate_steps(elbow_d)
        wrist_steps = self.wrist.calculate_steps(wrist_d)
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
        

