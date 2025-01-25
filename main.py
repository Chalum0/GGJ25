from src.entities.player import Player
from src.settings.settings import *

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
        self.dt = 0
        self.player = Player()

        self.loop()

    def loop(self):
        self.playing = True
        while self.playing:

            self.calculations()
            self.render()

            pygame.display.flip()

            self.check_events()

            self.dt = self.clock.tick(self.max_fps) / 1000


    def render(self):
        screen = self.screen
        screen.fill((255, 0, 0))

        screen.blit(self.player.texture, self.player.rect)

    def calculations(self):
        player = self.player
        dt = self.dt * 60
        keys = pygame.key.get_pressed()
        collide_bottom = False
        if player.rect.bottom >= 720:
            player.rect.bottom = 720
            collide_bottom = True
            player.in_jump = False

        if not collide_bottom:
            if player.y_momentum < player.max_y_momentum:
                player.y_momentum = min(
                    player.y_momentum + player.y_acceleration * dt,
                    player.max_y_momentum
                )
        else:
            player.y_momentum = 0

        self.controls(keys, dt)

        player.pos[0] += player.x_momentum * dt
        player.pos[1] += player.y_momentum * dt
        player.update_rect()

    def controls(self, keys, dt):
        # move player according to controls
        if keys[control_keys["LEFT"]] and self.player.x_momentum > -self.player.max_x_momentum:
            self.player.x_momentum -= self.player.x_acceleration * dt
        if keys[control_keys["RIGHT"]] and self.player.x_momentum < self.player.max_x_momentum:
            self.player.x_momentum += self.player.x_acceleration * dt

        # stop player slowly if no key is pressed
        if not keys[control_keys["LEFT"]] and not keys[control_keys["RIGHT"]]:
            if self.player.x_momentum > 0:
                self.player.x_momentum -= self.player.x_acceleration * dt
            elif self.player.x_momentum < 0:
                self.player.x_momentum += self.player.x_acceleration * dt

            if -0.5 < self.player.x_momentum < 0.5:
                self.player.x_momentum = 0

        if keys[control_keys["JUMP"]] and not self.player.in_jump:
            self.player.in_jump = True
            self.player.y_momentum = -7


    def check_events(self):
        for event in pygame.event.get():
            # -- If the user closes the window --
            if event.type == pygame.QUIT:
                time.sleep(0.5)
                self.playing = False


if __name__ == "__main__":
    main = Main()
