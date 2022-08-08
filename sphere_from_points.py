from manim import *
import numpy as np


class SphereFromPoints(ThreeDScene):
    def construct(self):
        ax = ThreeDAxes(
            x_range=(-2, 2),
            y_range=(-2, 2),
            z_range=(-2, 2),
            axis_config={"include_numbers": True},
        )
        radius = 2
        steps = 1000
        curve1 = ParametricFunction(
            lambda u: np.array(
                [
                    radius * np.cos(u * TAU) * np.sin(u * PI),
                    radius * np.sin(u * TAU) * np.sin(u * PI),
                    radius * np.cos(u * PI),
                ]
            ),
            color=RED,
            t_range=np.array([0, 1, 0.005]),
        ).set_shade_in_3d(True)
        self.add(ax, curve1)
        self.set_camera_orientation(phi=80 * DEGREES, theta=-60 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.25 * PI)
        # self.wait(8)
        self.interactive_embed()
