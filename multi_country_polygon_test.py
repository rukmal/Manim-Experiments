import manim as m
from country_data import CountryData


class MultiCountryTest(m.Scene):
    countries = ["LKA", "IND", "NPL", "PAK", "BGD", "AFG", "MDV", "BTN"]
    colors = [
        m.BLUE_D,
        m.PURPLE_B,
        m.GREEN_D,
        m.YELLOW_D,
        m.RED_B,
        m.TEAL_D,
        m.ORANGE,
        m.GRAY_BROWN,
    ]

    def construct(self):
        c_data = CountryData()

        combined_geoms = c_data.get_multiple_country_geometries_scaled(
            self.countries, add_z=True
        )

        # Plot India
        # combined_mobs = m.VDict()
        # ind_mobs = self.create_country_polygons(ind_verts, RED)
        # lk_mobs = self.create_country_polygons(lk_verts, BLUE)
        # npl_mobs = self.create_country_polygons(npl_verts, GREEN)

        country_mobs = m.VDict()
        for idx, country in enumerate(self.countries):
            country_mobs[country] = self.create_country_polygons(
                combined_geoms[idx], self.colors[idx]
            )
            # combined_mobs += country_mobs[country]

        # combined_mobs.scale(6).move_to(m.ORIGIN, aligned_edge=m.ORIGIN)
        country_mobs.scale(6).move_to(m.ORIGIN, aligned_edge=m.ORIGIN)

        self.play(m.DrawBorderThenFill(country_mobs), run_time=3)

        country_mobs.generate_target()

        # Scaling countries
        country_mobs.target.arrange_in_grid(2, 4, buff=1)
        self.play(
            m.MoveToTarget(country_mobs),
            run_time=2,
        )

        # # Scaling countries
        # a = country_mobs["IND"].scale(0.5)
        # b = country_mobs["LKA"].scale(3)
        # c = country_mobs["BTN"].scale(2)
        self.play(
            m.AnimationGroup(
                *[
                    m.ApplyMethod(country_mobs[i].scale, j)
                    for i, j in zip(
                        ["LKA", "IND", "BTN", "PAK", "BGD", "NPL"],
                        [3, 0.5, 2.5, 0.8, 1.5, 2],
                    )
                ],
                m.AnimationGroup(
                    m.ApplyMethod(country_mobs["MDV"].scale, 2.5),
                    m.Rotate(country_mobs["MDV"], 0.25 * m.PI),
                    lag_ratio=0,
                ),
                lag_ratio=0.2
            ),
            run_time=2,
        )

        self.play(
            m.AnimationGroup(
                *[m.Uncreate(country_mobs[i]) for i in self.countries], lag_ratio=0.2
            )
        )

    def create_country_polygons(self, polys, color) -> m.VGroup:
        country_mobs = m.VGroup()
        for poly in polys:
            country_mobs += m.Polygon(*poly, color=color, stroke_width=2)
        return country_mobs
