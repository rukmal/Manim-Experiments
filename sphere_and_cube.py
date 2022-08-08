from manim import *
from manim.opengl import *


class SphereAndCube(ThreeDScene):
    def construct(self):
        # sphere = Sphere(radius=1, fill_opacity=0.5, color=BLUE)
        # self.play(Create(sphere), run_time=3)
        self.play(
            self.camera.animate.set_euler_angles(phi=50 * DEGREES, theta=40 * DEGREES)
        )

        # # Add 3d axes
        # axes = ThreeDAxes(x_rage=[-2, 2], y_range=[-2, 2], z_range=[-2, 2])
        # self.add(axes)

        # Add cubes
        cubes = VGroup(
            *[
                Cube(side_length=0.5, fill_opacity=0.5, fill_color=PURPLE)
                for _ in range(20)
            ]
        )
        cubes.arrange_in_grid(4, 5).move_to([0, 0, -2])
        self.play(AnimationGroup(*[Create(cube) for cube in cubes], lag_ratio=0.1))

        self.wait()

        # Add spheres
        spheres = VGroup()
        for i in range(20):
            spheres.add(Cube(side_length=0.5, fill_color=RED))
        spheres.arrange_in_grid(4, 5).move_to([0, 0, 2])
        self.play(
            AnimationGroup(*[Create(sphere) for sphere in spheres], lag_ratio=0.1)
        )

        self.play(
            self.camera.animate.set_euler_angles(phi=60 * DEGREES, theta=40 * DEGREES)
        )
        self.begin_ambient_camera_rotation(rate=0.2)

        # Draw lines from each of the cubes to spheres
        for i in range(20):
            self.play(
                AnimationGroup(
                    *[
                        Create(
                            Line(
                                start=cubes[i].get_center(),
                                end=spheres[j].get_center(),
                                stroke_width=0.5,
                            )
                        )
                        for j in range(0, 20)
                    ],
                    lag_ratio=0.1,
                )
            )
