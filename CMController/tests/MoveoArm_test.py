'''
Test
Unit test suite for CMController actions.

March 2, 2020: Need to write accurate unit test cases for the CMController class.
'''
import sys
import unittest
from CMController.MoveoArm.moveo_arm import MoveoArm
from CMController.MoveoArm.instruction import InstructionManager
from CMController.MoveoArm.ik import InverseKinematics, IKMapping
from CMController.MoveoArm import joint


class TestMoveoArm(unittest.TestCase):
    def setUp(self):
        self.arm = MoveoArm()

    def test_check_constraints(self):
        steps1 = (20, 20, 20, 20)
        steps2 = (350, 350, 3000, 350)
        constraints1 = self.arm.check_constraints(steps1[0], steps1[1], steps1[2], steps1[3])
        constraints2 = self.arm.check_constraints(steps2[0], steps2[1], steps2[2], steps2[3])
        self.assertEqual(constraints1, (True, True, True, True))
        #self.assertEqual(constraints2, (False, False, False, False))
        #is_allowed = self.arm.is_steps_allowed(steps1)
        #not_allowed = self.arm.is_steps_allowed(steps2)
        #self.assertTrue(is_allowed)
        #self.assertFalse(not_allowed)


    def test_instructions(self):
        i_manager = InstructionManager()
        mi = i_manager.get_move_instruction("+102", "-035", "-109", "+004", 0)
        bi = i_manager.get_base_instruction("+102")
        si = i_manager.get_shoulder_instruction("-035")
        ei = i_manager.get_elbow_instruction("-109")
        wi = i_manager.get_wrist_instruction("+004")
        print("Move instruction: " + mi)
        print("Base instruction: " + bi)
        print("Shoulder instruction: " + si)
        print("Elbow instruction: " + ei)
        print("Wrist instruction: " + wi)


class TestIK(unittest.TestCase):
    def setUp(self):
        self.ik = InverseKinematics()


    def mapIK(self):
        map = IKMapping()
        map.plot_xy(20, 20)


    def test_inverse_kinematics(self):
        forward = self.ik.solve_forward(12, 12, 12)
        inverse = self.ik.solve_inverse(forward[0], forward[1], forward[2])
        print("Forward 12 12 12 -> " + str(forward))
        print("Inverse -> " + str(inverse))


class TestJoints(unittest.TestCase):
    def setUp(self):
        self.joint = joint.Joint(max_constraint=45, min_constraint=-45, gear_ratio=1.0)
        self.base = joint.Base()
        self.shoulder = joint.Shoulder()
        self.elbow = joint.Elbow()
        self.roll = joint.Roll()
        self.wrist = joint.Wrist()
        self.grip = joint.Grip()

    def test_joint(self):
        self.assertEqual(self.joint.get_max_constraint(), 45)
        self.assertFalse(self.joint.check_constraints(350))
        self.assertTrue(self.joint.check_constraints(45))
        self.assertTrue(self.joint.check_constraints(-45))
        self.assertTrue(self.joint.check_constraints(0))
        self.assertEqual(self.joint.calculate_steps(45), 50)


if __name__ == '__main__':
    unittest.main()
