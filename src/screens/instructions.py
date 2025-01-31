from src.draw import *
import pygame


class InstructionsScreen:

    TEXTS = [
        [
            "You are the crab.",
            "You must reach the crabette.",
            "Use W, A, S, D (qwerty) as arrow keys to move.",
            "Press Space to jump.",
            "",
            "Touch the bubbles to discover the effect of each color.",
            "Once you are in a red bubble, hold one of W, A, S, D",
            "to choose the direction, and press Space to burst the bubble.",
        ],
        [
            "Starting from level 5, you will have to place bubbles yourself.",
            "Press A to toggle bubble placement mode.",
            "Move with W, A, S, D and press an arrow key to put a bubble.",
            "Press 1, 2, 3 to choose the color of the bubbles you put.",
            "You can have 3 put bubbles at most.",
            "You can burst your bubbles by going into them with the same color.",
            "",
            "THANK YOU! HAVE FUN!!!",
        ],
    ]


    def __init__(self, main):
        self.main = main
        self.font = pygame.font.SysFont("Liberation Sans", 30)
        self.cur_page = 0


    def loop(self):
        while self.cur_page < len(self.TEXTS) and not self.main.quit:
            self.render()
            pygame.display.flip()
            self.check_events()
            self.main.clock.tick(self.main.max_fps)


    def render(self):
        draw_vertical_gradient(self.main)

        texts = self.TEXTS[self.cur_page]
        line_height = .1
        text_y = .5 - line_height * (len(texts) - 1) / 2
        for text in texts:
            draw_centered_text(self.main, self.font, text, text_y, (255, 255, 255))
            text_y += line_height


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.cur_page = len(self.TEXTS)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self.cur_page += 1
                elif event.key == pygame.K_LEFT or event.key == pygame.K_PAGEUP:
                    self.cur_page = max(0, self.cur_page - 1)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_PAGEDOWN:
                    self.cur_page = min(self.cur_page + 1, len(self.TEXTS) - 1)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.cur_page += 1
                elif event.button == 3:
                    self.cur_page = max(0, self.cur_page - 1)
