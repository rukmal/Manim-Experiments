import manim as m
from globe import Globe


class GlobeTest(m.ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * m.DEGREES, theta=30 * m.DEGREES)
        globe = Globe()
        globe_polys = globe.get_country_globe(["USA"])
        self.add(globe_polys)
