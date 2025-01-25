import pygame


class Credits:
    def __init__(self, main):
        self.main = main
        self.quit = False
        self.font = pygame.font.SysFont("Liberation Sans", 50)


    def loop(self):
        self.render()
        pygame.display.flip()
        while not self.quit:
            self.check_events()
            self.main.clock.tick(self.main.max_fps)


    def draw_centered_text(self, font, text, relative_y):
        surface = font.render(text, True, (255, 255, 255))
        x = (self.main.screen_size[0] - surface.get_width()) // 2
        y = self.main.screen_size[1] * relative_y - surface.get_height() // 2
        self.main.screen.blit(surface, (x, y))

    def render(self):
        self.main.screen.fill((0, 0, 255))

        self.draw_centered_text(self.font, "Game created by:", .29)
        self.draw_centered_text(self.font, "Snappyink", .43)
        self.draw_centered_text(self.font, "Gabriel Etienne", .57)
        self.draw_centered_text(self.font, "Sylvain Chiron", .71)


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = self.main.quit = True
            elif event.type == pygame.KEYDOWN:
                self.quit = True
