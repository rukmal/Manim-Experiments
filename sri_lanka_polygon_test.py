from manim import *
from country_data import CountryData


class SriLankaPolygonTest(Scene):
    def construct(self):
        # Load Sri Lanka data
        c_data = CountryData()
        lk_polygons = c_data.get_country_geometry_scaled("LKA", add_z=True)
        lk_mobs = VGroup()
        for poly in lk_polygons:
            # p = [i * 5 for i in poly]
            lk_mobs += Polygon(*poly, color=BLUE, stroke_width=1)
        lk_mobs.scale(1).move_to(ORIGIN, aligned_edge=ORIGIN)
        # lk_mobs.move_to(ORIGIN)
        self.play(DrawBorderThenFill(lk_mobs), run_time=3)
        self.wait(2)
        lk_mobs.generate_target()
        lk_mobs.target.shift(LEFT * 4)
        lk_mobs.target.scale(1.5)
        self.play(MoveToTarget(lk_mobs), run_time=2)
        self.wait(2)


class SriLankaAndIndiaPolygonTest(Scene):
    def construct(self):
        # Load Sri Lanka data
        c_data = CountryData()
        lk_polygons = c_data.get_country_geometry_scaled("LKA", add_z=True)
        lk_mobs = VGroup()
        for poly in lk_polygons:
            # p = [i * 5 for i in poly]
            lk_mobs += Polygon(*poly, color=BLUE, stroke_width=1)
        lk_mobs.scale(1).move_to(ORIGIN, aligned_edge=ORIGIN)
        # lk_mobs.move_to(ORIGIN)
        self.play(DrawBorderThenFill(lk_mobs), run_time=3)
        self.wait(2)
        lk_mobs.generate_target()
        lk_mobs.target.shift(LEFT * 4)
        lk_mobs.target.scale(1.5)
        self.play(MoveToTarget(lk_mobs), run_time=2)
        self.wait(2)

        # India polys
        india_polygons = c_data.get_country_geometry_scaled("IND", add_z=True)
        india_mobs = VGroup()
        for poly in india_polygons:
            india_mobs += Polygon(*poly, color=RED, stroke_width=1)
        india_mobs.scale(1.5).move_to(ORIGIN, aligned_edge=ORIGIN)
        self.play(DrawBorderThenFill(india_mobs), run_time=3)
        self.wait(2)
        india_mobs.generate_target()
        india_mobs.target.shift(RIGHT * 4)
        india_mobs.target.scale(2)
        self.play(MoveToTarget(india_mobs), run_time=2)
        self.wait(2)
        # for i in test_poly:
        #     print(i)
        # self.add(Polygon(*test_poly, color=BLUE).scale(20).move_to(LEFT * 2))

        # self.interactive_embed()
        # self.add(lk_mobs)
