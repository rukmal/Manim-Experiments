from country_data import CountryData
from manim import Polyhedron, ThreeDScene, DEGREES, ORIGIN, Create, PI
import csv


class CountrySurfaceTest(ThreeDScene):
    def construct(self):
        # self.move_camera(zoom=1)
        # # Create axes
        # ax = ThreeDAxes(
        #     x_range=(-2, 2),
        #     y_range=(-2, 2),
        #     z_range=(-2, 2),
        #     axis_config={"include_numbers": False},
        # )
        # # Set axis colors
        # ax.get_x_axis().set_color(RED)
        # ax.get_y_axis().set_color(GREEN)
        # ax.get_z_axis().set_color(BLUE)
        # # Add axis and move camera
        # self.play(Create(ax), run_time=2)
        # self.move_camera(theta=50 * DEGREES, phi=80 * DEGREES, run_time=2)
        # self.begin_ambient_camera_rotation(rate=PI / 4)
        # self.wait(2)
        # surf = Surface(lambda u, v: [u, v, 0], u_range=(-1, 1), v_range=(-1, 1))
        # self.play(Create(surf))
        # surf2 = Surface(
        #     lambda u, v: [u * 0.5, v * 0.5, 0],
        #     u_range=(-1, 1),
        #     v_range=(-1, 1),
        #     color=RED,
        # )
        # self.play(Create(surf2))

        # def surface_test(u, v):
        #     if v > u:
        #         return [u, u, 0]
        #     else:
        #         return [u, v, 0]

        # surf = Surface(surface_test, u_range=(-1, 1), v_range=(-1, 1))
        # self.play(Create(surf))
        # self.interactive_embed()
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        c_data = CountryData()

        # Attempt to build polygon
        verts, tris = c_data.get_country_verts_and_tris("LKA", resolution=50)
        import numpy as np

        np.savetxt("verts.csv", verts, delimiter=",", fmt="%f")
        np.savetxt("tris.csv", tris, delimiter=",", fmt="%f")

        print(verts)
        print(len(tris))
        print(tris)
        lk = Polyhedron(
            verts * 5,
            tris,
        )
        for f in lk.faces:
            f.stroke_width = 0
            f.stroke_opacity = 0
        self.add(lk)
        self.remove(lk.graph)
        lk.move_to(ORIGIN)
        self.begin_ambient_camera_rotation(rate=0.25 * PI)
        self.play(Create(lk), run_time=3)
        self.wait(4)
