from src.entities.player import Player
from src.settings.settings import *
from src.terrain.map import Map

import pygame
import random
import time
import math


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
        self.map = Map()

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
        grid = self.map.grid
        screen.fill((255, 0, 0))

        self.map.tiles_rect = []
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] != 0:
                    rect = pygame.rect.Rect(0, 0, self.map.tile_size, self.map.tile_size)
                    rect.topleft = (x*self.map.tile_size, y*self.map.tile_size)
                    self.map.tiles_rect.append(rect)
                    screen.blit(self.map.tiles_texture[grid[y][x]-1], (x*self.map.tile_size, y*self.map.tile_size))

        screen.blit(self.player.texture, self.player.rect)

    def calculations(self):
        player = self.player
        dt = self.dt * 60
        keys = pygame.key.get_pressed()

        # player.collide_bottom = False
        if player.rect.bottom >= 720:
            player.rect.bottom = 720
            player.collide_bottom = True

        if not player.collide_bottom:
            if player.y_momentum < player.max_y_momentum:
                player.y_momentum = min(
                    player.y_momentum + player.y_acceleration * dt,
                    player.max_y_momentum
                )
        else:
            player.y_momentum = 0

        self.controls(keys, dt)

        player.collide_bottom = False

        self.move_obj(player, dt)

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

        if keys[control_keys["JUMP"]] and self.player.collide_bottom:
            self.player.collide_bottom = False
            self.player.y_momentum = self.player.jump_power

    def move_obj(self, obj, dt):

        obj.pos[1] += obj.y_momentum * dt

        obj.update_rect()
        tls = []
        for tile in self.map.tiles_rect:
            if not obj.rect.colliderect(tile):
                if math.dist(tile.center, obj.rect.center) < self.map.tile_size:
                    tls.append(tile)
                continue
            if obj.y_momentum < 0 and tile.bottom - self.map.tile_size/2 < obj.rect.top < tile.bottom + 1:
                obj.pos[1] = tile.bottom
                obj.collide_top = True
                obj.y_momentum = 0
            if obj.y_momentum > 0 and tile.top + self.map.tile_size/2 > obj.rect.bottom > tile.top - 1:
                obj.pos[1] = tile.top - obj.rect.size[1]
                obj.collide_bottom = True
                obj.y_momentum = 0
            tls.append(tile)

        obj.pos[0] += obj.x_momentum * dt
        obj.update_rect()
        for tile in tls:
            if not obj.rect.colliderect(tile):
                continue
            if obj.x_momentum < 0 and obj.rect.left < tile.right:
                obj.pos[0] = tile.right
                obj.collide_left = True
                obj.x_momentum = 0
            if obj.x_momentum > 0 and obj.rect.right > tile.left:
                obj.pos[0] = tile.left - obj.rect.size[0]
                obj.collide_right = True
                obj.x_momentum = 0

            obj.update_rect()

    def check_events(self):
        for event in pygame.event.get():
            # -- If the user closes the window --
            if event.type == pygame.QUIT:
                time.sleep(0.5)
                self.playing = False


if __name__ == "__main__":
    main = Main()
