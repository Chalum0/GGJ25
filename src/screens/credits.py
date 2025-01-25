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

    def render(self):
        self.main.screen.fill((0, 0, 255))

        texts = [
            ("Game created by:", False),
            ("Snappyink", True),
            ("Gabibel", True),
            ("Frigory33", True),
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
