    from manim import *
    from manim_physics import *


    class ElectricFieldExample(Scene):
        def construct(self):
            charge1 = Charge(-1, LEFT + DOWN)
            charge2 = Charge(2, RIGHT + DOWN)
            charge3 = Charge(-1, UP)
            field = ElectricField(charge1, charge2, charge3)
            self.add(charge1, charge2, charge3)
            self.add(field)

            # Add a fourth charge
            charge4 = Charge(2, LEFT * 3 + 2 * UP)
            field2 = ElectricField(charge1, charge2, charge3, charge4)
            self.play(Create(charge4))
            self.play(Transform(field, field2))
            self.wait(2)

            # Add animation of the field
            stream_line = StreamLines(field2.func, colors=[PURPLE, PINK, ORANGE])
            self.add(stream_line)
            stream_line.start_animation(warm_up=False, flow_speed=1.5, time_width=0.5)
            self.wait(5)
            self.play(stream_line.end_animation())
            self.play(FadeOut(VGroup(*self.mobjects)))
