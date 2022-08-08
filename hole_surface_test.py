from manim import Create, ThreeDScene, Surface, DEGREES, RED, Polyhedron, Point


class HoleSurfaceTest(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        vertex_coords = [[1, 1, 0], [1, -1, 0], [-1, -1, 0], [-1, 1, 0], [0, 0, 2]]
        # faces_list = [[0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4], [0, 1, 2, 3]]
        faces_list = [[0, 1, 4], [1, 2, 4], [0, 1, 2, 3]]
        pyramid = Polyhedron(
            vertex_coords,
            faces_list,
        )
        self.add(pyramid)
        self.remove(pyramid.graph)
