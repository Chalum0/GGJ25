import pygame
import random


class Win:
    def __init__(self, main):
        self.main = main

        self.font = pygame.font.SysFont("Liberation Sans", 100)
        self.crab = pygame.image.load('src/textures/crab.png').convert_alpha()
        self.crab = pygame.transform.scale_by(self.crab, 3)
        self.bubble_imgs = [
            pygame.image.load(f'src/textures/bubble-{color}.png').convert_alpha()
            for color in ('red', 'green', 'blue')
        ]
        self.bubble_imgs = [pygame.transform.scale(img, (40, 40)) for img in self.bubble_imgs]

        self.bubbles = []
        self.bubble_time = 1

        self.quit = False
        self.dt = 0
        self.loop()


    def loop(self):
        while not self.quit and not self.main.quit:
            self.calculations()

            self.render()
            pygame.display.flip()

            self.check_events()

            self.dt = self.main.clock.tick(self.main.max_fps) / 1000


    def draw_centered_text(self, font, text, relative_y, color):
        surface = font.render(text, True, color)
        x = (self.main.screen_size[0] - surface.get_width()) // 2
        y = self.main.screen_size[1] * relative_y - surface.get_height() // 2
        self.main.screen.blit(surface, (x, y))

    def render(self):
        screen = self.main.screen
        screen.fill((0, 0, 128))
        self.draw_centered_text(self.font, "YOU WIN", .45, (255, 255, 255))

        crab_x = self.main.screen_size[0] * .5 - self.crab.get_width() / 2
        crab_y = self.main.screen_size[1] * .6
        screen.blit(self.crab, (crab_x, crab_y))

        for bubble_img, x, y in self.bubbles:
            screen.blit(bubble_img, (x, y))


    def calculations(self):
        bubble_speed = 200

        for bubble in self.bubbles:
            bubble[2] -= self.dt * bubble_speed
        while len(self.bubbles) > 0 and self.bubbles[0][2] < -100:
            self.bubbles.pop(0)

        self.bubble_time -= self.dt
        if self.bubble_time < 0:
            bubble_img = random.choice(self.bubble_imgs)
            bubble_w = bubble_img.get_width()
            x = (self.main.screen_size[0] - bubble_w) * random.random()
            y = self.main.screen_size[1] + bubble_speed * self.bubble_time
            self.bubbles.append([bubble_img, x, y])
            self.bubble_time += .5


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN \
                        or event.key == pygame.K_KP_ENTER:
                    self.quit = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.quit = True
