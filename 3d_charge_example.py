from manim import *
from manim_physics import *


class ThreeDCharges(ThreeDScene):
    def construct(self):
        ax = ThreeDAxes()
        charge1 = Charge(-1, [0, 0, 0])
        charge2 = Charge(2, [4, 3, 2])
        self.add(ax)
        self.play(Create(charge1), Create(charge2))
        self.wait(2)
        self.move_camera(theta=50 * DEGREES, phi=80 * DEGREES, run_time=2)
        self.begin_ambient_camera_rotation(rate=0.25 * PI)
        field = ElectricField(charge1, charge2)
        # self.play(Create(field))
        self.add(field)
        self.wait(4)
