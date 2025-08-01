from manim import *

class ScrollingText(Scene):
    def construct(self):
        # Initial three lines
        lines = [
            Text("Line 1", font_size=36),
            Text("Line 2", font_size=36),
            Text("Line 3", font_size=36),
        ]

        # Position them vertically spaced
        for i, line in enumerate(lines):
            line.move_to(0.5*UP * (1 - i))  # positions: 1, 0, -1

        # Create a VGroup
        text_group = VGroup(*lines)
        self.play(FadeIn(text_group))

        # New lines to add one-by-one
        new_texts = [
            "Line 4",
            "Line 5",
            "Line 6",
        ]

        for new_line_str in new_texts:
            # 1. Fade out the top line
            self.play(FadeOut(text_group[0]))

            # 2. Remove the top line from the group
            text_group.remove(text_group[0])

            # 3. Move the remaining lines up
            self.play(*[line.animate.shift(0.5*UP) for line in text_group])

            # 4. Create the new line and move it to the bottom position
            new_line = Text(new_line_str, font_size=36).move_to(0.5*DOWN)
            self.play(FadeIn(new_line))

            # 5. Add new line to the group
            text_group.add(new_line)

        self.wait(1)