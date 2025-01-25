from src.screens.game import Game
from src.screens.credits import Credits
import pygame


class MainMenu:
    def __init__(self, main):
        self.main = main

        self.title_font = pygame.font.SysFont("Liberation Sans", 60)
        self.button_font = pygame.font.SysFont("Liberation Sans", 40)

        self.buttons = [(.43, "Play"), (.63, "Credits"), (.83, "Quit")]
        self.button_height = self.main.screen_size[1] * .15
        self.cursor = 0


    def loop(self):
        while not self.main.quit:
            self.render()
            pygame.display.flip()

            self.check_events()

            self.main.clock.tick(self.main.max_fps)


    def draw_centered_text(self, font, text, relative_y):
        surface = font.render(text, True, (255, 255, 255))
        x = (self.main.screen_size[0] - surface.get_width()) // 2
        y = self.main.screen_size[1] * relative_y - surface.get_height() // 2
        self.main.screen.blit(surface, (x, y))

    def render(self):
        screen = self.main.screen
        screen.fill((0, 0, 255))

        self.draw_centered_text(self.title_font, "Bubble Passage", .2)

        for index, (button_y, label) in enumerate(self.buttons):
            if index == self.cursor:
                y = self.main.screen_size[1] * button_y
                rect = (0, y - self.button_height / 2, self.main.screen_size[0], self.button_height)
                pygame.draw.rect(screen, (0, 128, 0), rect)
            self.draw_centered_text(self.button_font, label, button_y)


    def press_button(self):
        match self.cursor:
            case 0:
                Game(self.main).loop()
            case 1:
                Credits(self.main).loop()
            case 2:
                self.main.quit = True

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.cursor = (self.cursor - 1) % len(self.buttons)
                elif event.key == pygame.K_DOWN:
                    self.cursor = (self.cursor + 1) % len(self.buttons)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self.press_button()
            elif event.type == pygame.MOUSEMOTION:
                self.cursor = -1
                for index, (button_y, _) in enumerate(self.buttons):
                    _, mouse_y = event.pos
                    button_y *= self.main.screen_size[1]
                    if button_y - self.button_height / 2 <= mouse_y < button_y + self.button_height / 2:
                        self.cursor = index
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.press_button()
