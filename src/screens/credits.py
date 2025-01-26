import pygame


class Credits:
    def __init__(self, main):
        self.main = main
        self.quit = False
        self.font = pygame.font.SysFont("Liberation Sans", 40)
        self.smaller_font = pygame.font.SysFont("Liberation Sans", 35)


    def loop(self):
        self.render()
        pygame.display.flip()
        while not self.quit:
            self.check_events()
            self.main.clock.tick(self.main.max_fps)


    def draw_centered_text(self, font, text, relative_y, color):
        surface = font.render(text, True, color)
        x = (self.main.screen_size[0] - surface.get_width()) // 2
        y = self.main.screen_size[1] * relative_y - surface.get_height() // 2
        self.main.screen.blit(surface, (x, y))

    def draw_vertical_gradient(self):
        top_color = (10, 125, 180)  # LightSkyBlue
        bottom_color = (0, 25, 60)  # MidnightBlue
        """Draws a vertical gradient on the given surface."""
        # Pre-calculate color differences
        delta_r = bottom_color[0] - top_color[0]
        delta_g = bottom_color[1] - top_color[1]
        delta_b = bottom_color[2] - top_color[2]

        for y in range(self.main.screen_size[1]):
            # Compute interpolation factor from 0.0 (top) to 1.0 (bottom)
            t = y / self.main.screen_size[1]

            # Interpolate color channel by channel
            r = int(top_color[0] + (delta_r * t))
            g = int(top_color[1] + (delta_g * t))
            b = int(top_color[2] + (delta_b * t))

            # Draw a horizontal line for this row
            pygame.draw.line(self.main.screen, (r, g, b), (0, y), (self.main.screen_size[0], y))

    def render(self):
        self.draw_vertical_gradient()

        texts = [
            ("Game created by:", False),
            ("Snappyink (development)", True),
            ("Gabibel (art, design)", True),
            ("Frigory33 (development)", True),
            ("Krozt (music)", True),
            ("during Global Game Jam 2025", False),
            ("at Université de Bordeaux", False),
            ("CC BY-NC-SA 4.0", False),
        ]
        line_height = .12
        text_y = .5 - line_height * (len(texts) - 1) / 2
        for text, other_style in texts:
            font = self.smaller_font if other_style else self.font
            color = (255, 255, 0) if other_style else (255, 255, 255)
            self.draw_centered_text(font, text, text_y, color)
            text_y += line_height


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = self.main.quit = True
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
                self.quit = True
