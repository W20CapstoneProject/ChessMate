from CMController.MoveoArm.joint import Base, Shoulder, Elbow, Wrist, Grip

# Approximate arm dimensions:
#     - Shoulder Bone length = 220mm
#     - Elbow Bone length = 220mm
#     - Wrist Bone length = 95mm
#     - Gripper length = 70mm
#    
#     - Base radius = 80mm
#     - Shoulder radius = 60mm
#     - Elbow radius = 48mm
#     - Wrist radius = 35mm

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
        base = self.base.check_constraints(base_steps)
        shoulder = self.shoulder.check_constraints(shoulder_steps)
        elbow = self.elbow.check_constraints(elbow_steps)
        wrist = self.wrist.check_constraints(wrist_steps)
        return (base, shoulder, elbow, wrist)

    def verify_steps(self, base, shoulder, elbow, wrist):
        ''' Determines if the steps given will fall within the max and min constraints of the arm.'''
        responses = self.check_constraints(base, shoulder, elbow, wrist)
        for response in responses:
            if (response is False):
                return False
        return True


    def calculate_steps(self, base_d, shoulder_d, elbow_d, wrist_d, grip_d):
        '''
        Given the desired degrees for rotation, calculate the steps for each motor.
        This function assumes that the current position of the joints are all at zero/origin.

        Returns - steps for each controlled joint
        '''
        base_steps = round(self.base.calculate_steps(base_d), self.precision)
        shoulder_steps = round(self.shoulder.calculate_steps(shoulder_d), self.precision)
        elbow_steps = round(self.elbow.calculate_steps(elbow_d), self.precision)
        wrist_steps = round(self.wrist.calculate_steps(wrist_d), self.precision)
        grip_steps = round(self.grip.calculate_steps(grip_d), self.precision)
        return (base_steps, shoulder_steps, elbow_steps, wrist_steps, grip_steps)


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
        

