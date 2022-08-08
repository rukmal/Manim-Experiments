from manim import *
from country_data import CountryData
from itertools import chain
from typing import List


class WorldMapTest(Scene):
    countries: List[str]
    colors = [BLUE_D, PURPLE_B, GREEN_D, YELLOW_D, RED_B, TEAL_D, ORANGE, GRAY_BROWN]

    def __init__(self, *args, **kwargs):
        self.c_data = CountryData()
        self.countries = self.c_data.list_all_countries_iso_a3()
        return super().__init__(*args, **kwargs)

    def get_color(self, idx: int) -> str:
        return self.colors[idx % len(self.colors)]

    def construct(self):
        c_data = CountryData()

        combined_geoms = c_data.get_multiple_country_geometries_scaled(
            self.countries, add_z=True
        )

        # Plot India
        combined_mobs = VGroup()
        # ind_mobs = self.create_country_polygons(ind_verts, RED)
        # lk_mobs = self.create_country_polygons(lk_verts, BLUE)
        # npl_mobs = self.create_country_polygons(npl_verts, GREEN)

        country_mobs = {}
        for idx, country in enumerate(self.countries):
            country_mobs[country] = self.create_country_polygons(
                combined_geoms[idx], self.get_color(idx)
            )
            combined_mobs += country_mobs[country]

        combined_mobs.scale(12).move_to(ORIGIN, aligned_edge=ORIGIN)

        self.play(DrawBorderThenFill(combined_mobs), run_time=12)
        self.wait(2)

        # combined_mobs.generate_target()
        # country_mobs["IND"].scale(0.5)
        # country_mobs["LKA"].scale(3)
        # country_mobs["BTN"].scale(2)
        # combined_mobs.target.arrange_in_grid(2, 4, buff=1)
        # self.play(MoveToTarget(combined_mobs), run_time=3)
        # self.wait(2)

        # text_mobs = VGroup()
        # for country in self.countries:
        #     direction = DOWN
        #     aligned_edge = ORIGIN
        #     text_mobs += Text(c_data.get_country_name(country), font_size=24).next_to(
        #         country_mobs[country],
        #         direction=direction,
        #         aligned_edge=aligned_edge,
        #     )
        # self.play(Write(text_mobs), run_time=1)
        # self.wait(2)

    def create_country_polygons(self, polys, color) -> VGroup:
        country_mobs = VGroup()
        for poly in polys:
            country_mobs += Polygon(*poly, color=color, stroke_width=1)
        return country_mobs
