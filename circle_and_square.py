from manim import *


class CircleAndSquare(Scene):
    def construct(self):
        # Add circles
        circles = (
            VGroup(
                *[Circle(radius=0.25, fill_opacity=0.5, color=BLUE) for i in range(20)]
            )
            .arrange_in_grid(4, 5)
            .scale(0.5)
        )
        # Spawn circles in a grid
        self.play(
            AnimationGroup(*[DrawBorderThenFill(i) for i in circles], lag_ratio=0.1),
            run_time=3,
        )
        self.wait()
        # Move circles to a line on the left
        self.play(
            circles.animate.arrange_in_grid(20, 1).scale(0.45).move_to([-4, 0, 0]),
            run_time=3,
        )

        # Add squares
        squares = (
            VGroup(
                *[
                    Square(side_length=0.5, fill_opacity=0.5, color=RED)
                    for i in range(20)
                ]
            )
            .arrange_in_grid(4, 5)
            .scale(0.5)
        )
        # Spawn squares in a grid
        self.play(
            AnimationGroup(*[DrawBorderThenFill(i) for i in squares], lag_ratio=0.1),
            run_time=3,
        )
        self.wait()
        # Move squares to a line on the right
        self.play(
            squares.animate.arrange_in_grid(20, 1).scale(0.45).move_to([4, 0, 0]),
            run_time=3,
        )

        # Draw lines from each of the blue circles to the red squares
        for i in range(20):
            self.play(
                AnimationGroup(
                    *[
                        Create(
                            Line(
                                start=circles[i].get_center() + [0.1, 0, 0],
                                end=squares[j].get_center() + [-0.1, 0, 0],
                                color=BLUE,
                                stroke_width=0.5,
                            )
                        )
                        for j in range(20)
                    ],
                    lag_ratio=0.1
                ),
                run_time=0.25,
            )
