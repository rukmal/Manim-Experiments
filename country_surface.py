from country_data import CountryData
from manim import *


class CountrySurfaceTest(ThreeDScene):
    def construct(self):
        self.move_camera(zoom=1)
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
        self.move_camera(theta=50 * DEGREES, phi=80 * DEGREES, run_time=2)
        self.begin_ambient_camera_rotation(rate=PI / 4)
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

        c_data = CountryData()

        # Create 100x100 uv map for Sri Lanka
        uv = c_data.build_uv_for_country("IND", include_altitude=False)

        # Create surface
        surf = Surface(
            uv,
            u_range=(0, 1),
            v_range=(0, 1),
            resolution=(1000, 1000),
            color=BLUE,
            fill_opacity=0.75,
        ).scale(2)
        self.play(Create(surf), run_time=5)
        self.wait(4)
        # self.interactive_embed()
