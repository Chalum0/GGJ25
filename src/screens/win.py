import pygame


class Win:
    def __init__(self, main):
        self.main = main

        self.font = pygame.font.SysFont("Liberation Sans", 60)
        self.crab = pygame.image.load('src/textures/crab.png').convert_alpha()
        self.crab = pygame.transform.scale_by(self.crab, 3)

        self.quit = False
        self.loop()


    def loop(self):
        while not self.quit and not self.main.quit:
            self.render()
            pygame.display.flip()

            self.check_events()

            self.main.clock.tick(self.main.max_fps)


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
