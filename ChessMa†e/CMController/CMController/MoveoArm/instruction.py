class InstructionManager():
    def get_move_instruction(self, base, shoulder, elbow, wrist, grip):
        mi = MoveInstruction()
        instruction = mi.create(base, shoulder, elbow, wrist, grip)
        return instruction

    def get_base_instruction(self, steps):
        bi = BaseInstruction()
        return bi.create(steps) 

    def get_shoulder_instruction(self, steps):
        si = ShoulderInstruction()
        return si.create(steps) 

    def get_elbow_instruction(self, steps):
        ei = ElbowInstruction()
        return ei.create(steps) 

    def get_wrist_instruction(self, steps):
        wi = WristInstruction()
        return wi.create(steps) 


class MerlinInstruction():
    depth = 4

    def create(self, base, shoulder, elbow, wrist, grip):
        base = str(base).zfill(self.depth)
        shoulder = str(shoulder).zfill(self.depth)
        elbow = str(elbow).zfill(self.depth)
        wrist = str(wrist).zfill(self.depth)
        grip = str(grip).zfill(self.depth)
        return "{0},{1},{2},{3},{4}\n".format(base, shoulder, elbow, wrist, grip)


class MoveInstruction():
    def __init__(self):
        self.instruction = "move"

    def create(self, base, shoulder, elbow, wrist, grip):
        return "{0} ({1}, {2}, {3}, {4}, {5})".format(self.instruction, base, shoulder, elbow, wrist, grip)


class _Instruction():
    def __init__(self):
        self.instruction = ""

    def set_type(self, type):
        self.instruction = type

    def get_type(self):
        return self.instruction

    def create(self, steps):
        type = self.instruction
        return "{0} ({1})\n".format(type, steps)


class BaseInstruction(_Instruction):
    def __init__(self):
        super().__init__()
        self.instruction = "base"
        

class ShoulderInstruction(_Instruction):
    def __init__(self):
        super().__init__()
        self.instruction = "shoulder"


class ElbowInstruction(_Instruction):
    def __init__(self):
        super().__init__()
        self.instruction = "elbow"


class WristInstruction(_Instruction):
    def __init__(self):
        super().__init__()
        self.instruction = "wrist"
        