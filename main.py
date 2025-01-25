from src.entities.player import Player
import pygame
import random
import time


class Main:
    def __init__(self):
        # -- Window creation --
        pygame.init()
        pygame.display.set_caption("hello world!")
        self.screen = pygame.display.set_mode((1080, 720))
        self.clock = pygame.time.Clock()
        self.max_fps = 60

        self.playing = None
        self.player = Player()

        self.loop()

    def loop(self):
        self.playing = True
        while self.playing:

            self.calculations()
            self.render()

            pygame.display.flip()

            self.check_events()

            self.clock.tick(self.max_fps)


    def render(self):
        screen = self.screen
        player = self.player
        screen.fill((255, 0, 0))

        screen.blit(player.texture, player.pos)


    def calculations(self):
        pass

    def check_events(self):
        for event in pygame.event.get():
            # -- If the user closes the window --
            if event.type == pygame.QUIT:
                time.sleep(0.5)
                self.playing = False


if __name__ == "__main__":
    main = Main()
