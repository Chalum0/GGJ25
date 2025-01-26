from src.entities.player import Player
from src.settings.settings import *
from src.terrain.map import Map

import pygame
import time
import math


class Game:
    def __init__(self, main, level_num=1):
        self.main = main
        self.level_num = level_num
        self.playing = True
        self.dt = 0
        self.font = pygame.font.SysFont("Liberation Sans", 30)

        self.map = Map(str(level_num), self.main.screen_size)
        player_pos = (coord * self.map.tile_size for coord in self.map.player_pos)
        self.player = Player(player_pos)
        self.checkpoint_time = None

    def loop(self):
        while self.playing:
            self.calculations()

            self.render()
            pygame.display.flip()

            self.check_events()

            self.dt = self.main.clock.tick(self.main.max_fps) / 1000

    def render(self):
        screen = self.main.screen
        grid = self.map.grid
        screen.fill((0, 0, 128))

        self.map.tiles_rect = []
        self.map.interaction_tiles_rect = []
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                block = grid[y][x]
                if block != 0:
                    # display
                    if block not in self.map.HIDDEN_BLOCKS:
                        screen.blit(self.map.tiles_texture[block - 1], (self.map.current_offset_x + x * self.map.tile_size, self.map.current_offset_y + y * self.map.tile_size))

                    # add collision
                    rect = pygame.rect.Rect(0, 0, self.map.tile_size, self.map.tile_size)
                    rect.topleft = (self.map.current_offset_x + x * self.map.tile_size, self.map.current_offset_y + y * self.map.tile_size)
                    if block not in self.map.TRANSPARENT_BLOCKS:
                        self.map.tiles_rect.append(rect)
                    if block in self.map.INTERACTION_BLOCKS:
                        self.map.interaction_tiles_rect.append({"type": block, "rect": rect, "pos": (x, y)})

        screen.blit(self.player.texture, self.player.rect)

        if self.checkpoint_time != None:
            black = pygame.Surface(self.main.screen_size)
            black.fill((0, 0, 0))
            black.set_alpha((pygame.time.get_ticks() - self.checkpoint_time) * 255 // 2000)
            screen.blit(black, (0, 0))

        fps_text = self.font.render(f"FPS: {int(self.main.clock.get_fps())}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))

    def calculations(self):
        player = self.player
        previous_player_pos = list(player.rect.topleft)
        dt = self.dt * 60
        keys = pygame.key.get_pressed()
        screen_size = self.main.screen_size

        if not player.in_bubble:
            if player.rect.bottom >= screen_size[1] + player.rect.height and self.map.current_offset_y < self.map.max_offset_y:
                self.__init__(self.main, self.level_num)
                return

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

            current_player_pos = player.pos

            # Scrolling
            if player.pos[0] > screen_size[0] - screen_size[0]/2.5 and self.map.current_offset_x > self.map.max_offset_x:
                self.map.current_offset_x += previous_player_pos[0] - current_player_pos[0]
                player.pos[0] = previous_player_pos[0] - 1

            if player.pos[0] < screen_size[0]/2.5 and self.map.current_offset_x < self.map.min_offset_x:
                self.map.current_offset_x += previous_player_pos[0] - current_player_pos[0]
                player.pos[0] = previous_player_pos[0] + 1


            if player.pos[1] > screen_size[1] - screen_size[1]/2.5 and self.map.current_offset_y > self.map.max_offset_y:
                self.map.current_offset_y += previous_player_pos[1] - current_player_pos[1]
                player.pos[1] = previous_player_pos[1]

            if player.pos[1] < screen_size[1]/2.5 and self.map.current_offset_y < self.map.min_offset_y:
                self.map.current_offset_y += previous_player_pos[1] - current_player_pos[1]
                player.pos[1] = previous_player_pos[1]

            for tile in self.map.interaction_tiles_rect:
                rect = tile["rect"]
                t = tile["type"]
                p = tile["pos"]
                if player.rect.colliderect(rect):
                    if t == self.map.INTERACTION_TILES_ID["red-bubble"]:
                        player.pos = [rect.x, rect.y + player.rect.height/2]
                        player.in_bubble = True
                        player.x_momentum = 0
                        player.bubble_pos = p
                    if t == self.map.INTERACTION_TILES_ID["green-bubble"]:
                        player.bubble_pos = p
                        player.x_momentum = -player.x_momentum * 2
                        player.y_momentum = -min(player.y_momentum * 1.3, player.max_y_momentum/1.2)
                        x, y = self.player.bubble_pos
                        self.map.grid[y][x] = 0
                    if t == self.map.INTERACTION_TILES_ID["checkpoint"] and self.checkpoint_time == None:
                        self.checkpoint_time = pygame.time.get_ticks()

        else:
            player.pos = previous_player_pos
            self.controls_in_bubble(keys)

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

        # if player goes over the speed limit (exemple: dashes)
        if self.player.x_momentum > self.player.max_x_momentum + 2:
            self.player.x_momentum -= self.player.x_acceleration * dt * 2
        if self.player.x_momentum < -self.player.max_x_momentum - 2:
            self.player.x_momentum += self.player.x_acceleration * dt * 2
        if self.player.y_momentum > self.player.max_y_momentum + 2:
            self.player.y_momentum -= self.player.y_acceleration * dt
        if self.player.y_momentum < -self.player.max_y_momentum - 2:
            self.player.y_momentum += self.player.y_acceleration * dt

        if keys[control_keys["JUMP"]] and self.player.collide_bottom:
            self.player.collide_bottom = False
            self.player.y_momentum = self.player.jump_power

    def controls_in_bubble(self, keys):
        if keys[control_keys["RIGHT"]] and keys[control_keys["JUMP"]]:
            self.player.x_momentum = 20
            self.player.pos[0] += self.player.x_momentum

        if keys[control_keys["LEFT"]] and keys[control_keys["JUMP"]]:
            self.player.x_momentum = -20
            self.player.pos[0] += self.player.x_momentum

        if keys[control_keys["UP"]] and keys[control_keys["JUMP"]]:
            self.player.y_momentum = -7
            self.player.pos[1] += self.player.y_momentum

        if keys[control_keys["DOWN"]] and keys[control_keys["JUMP"]]:
            self.player.y_momentum = 10
            self.player.pos[1] += self.player.y_momentum

        if (keys[control_keys["RIGHT"]] or keys[control_keys["LEFT"]] or keys[control_keys["UP"]] or keys[control_keys["DOWN"]]) and keys[control_keys["JUMP"]]:
            self.player.in_bubble = False
            x, y = self.player.bubble_pos
            self.map.grid[y][x] = 0


    def move_obj(self, obj, dt):
        # collisions y
        obj.pos[1] += obj.y_momentum * dt
        obj.update_rect()
        tls = []
        for tile in self.map.tiles_rect:
            if not obj.rect.colliderect(tile):
                if math.dist(tile.center, obj.rect.center) <= self.map.tile_size * 2:
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

        # collisions x
        obj.pos[0] += obj.x_momentum * dt
        obj.update_rect()
        def bound_on_left(bound_x):
            if obj.x_momentum < 0 and obj.rect.left < bound_x:
                obj.pos[0] = bound_x
                obj.collide_left = True
                obj.x_momentum = 0
        def bound_on_right(bound_x):
            if obj.x_momentum > 0 and obj.rect.right > bound_x:
                obj.pos[0] = bound_x - obj.rect.size[0]
                obj.collide_right = True
                obj.x_momentum = 0
        bound_on_left(0)
        bound_on_right(self.main.screen_size[0])
        for tile in tls:
            if not obj.rect.colliderect(tile):
                continue
            bound_on_left(tile.right)
            bound_on_right(tile.left)
        obj.update_rect()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                time.sleep(0.5)
                self.playing = False
                self.main.quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == control_keys["RESET"]:
                    self.__init__(self.main, self.level_num)
                elif event.key == pygame.K_ESCAPE:
                    self.playing = False

        if self.checkpoint_time != None and pygame.time.get_ticks() - self.checkpoint_time >= 2000:
            if self.level_num < 2:
                self.__init__(self.main, self.level_num + 1)
            else:
                self.playing = False
