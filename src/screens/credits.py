from src.draw import *
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


    def render(self):
        draw_vertical_gradient(self.main)

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
            draw_centered_text(self.main, font, text, text_y, color)
            text_y += line_height


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = self.main.quit = True
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
                self.quit = True
