from CMController.MoveoArm.ik import InverseKinematics, IKMapping
from CMController.MoveoArm.moveo_arm import MoveoArm
from numpy import radians

def visualizer_demo():  
    ik = InverseKinematics() 
    arm = MoveoArm()
    mapper = IKMapping()
    mapper.show_arm(radians(45), radians(55), radians(50))


if __name__ == "__main__":
    visualizer_demo()