from typing import Any
from src.entities.bubble import Bubble
from src.entities.player import Player
from src.settings.settings import *
from src.terrain.map import Map
from src.screens.win import Win

import pygame
import json
import time
import math


class Game:
    def __init__(self, main, level_num=1):
        self.main = main
        self.level_num = level_num
        self.playing = True
        self.dt = 0
        self.font = pygame.font.SysFont("Liberation Sans", 30)

        try:
            self.map = Map(str(level_num), self.main.screen_size)
            player_pos = (coord * self.map.tile_size for coord in self.map.player_pos)
            self.player = Player(player_pos)
            self.checkpoint_time = None

        except: # Game loading failed
            Win(self.main)
            self.playing = False


    def loop(self):
        while self.playing:
            self.calculations()

            self.render()
            pygame.display.flip()

            self.check_events()

            self.dt = self.main.clock.tick(self.main.max_fps) / 1000

        json.dump(self.level_num, open('src/settings/save.json', 'w'))

    def draw_vertical_gradient(self):
        top_color = (10, 125, 180)  # LightSkyBlue
        bottom_color = (0, 25, 60)  # MidnightBlue
        """Draws a vertical gradient on the given surface."""
        # Pre-calculate color differences
        delta_r = bottom_color[0] - top_color[0]
        delta_g = bottom_color[1] - top_color[1]
        delta_b = bottom_color[2] - top_color[2]

        for y in range(self.main.screen_size[1]):
            # Compute interpolation factor from 0.0 (top) to 1.0 (bottom)
            t = y / self.main.screen_size[1]

            # Interpolate color channel by channel
            r = int(top_color[0] + (delta_r * t))
            g = int(top_color[1] + (delta_g * t))
            b = int(top_color[2] + (delta_b * t))

            # Draw a horizontal line for this row
            pygame.draw.line(self.main.screen, (r, g, b), (0, y), (self.main.screen_size[0], y))

    def render(self):
        screen = self.main.screen
        grid = self.map.grid

        screen.fill((64, 64, 64))
        self.draw_vertical_gradient()
        end_x = len(grid[0]) * self.map.tile_size - self.map.current_offset_x
        end_y = len(grid) * self.map.tile_size - self.map.current_offset_y
        # pygame.draw.rect(screen, (0, 0, 128), (0, 0, end_x, end_y))

        self.map.tiles_rect = []
        self.map.interaction_tiles_rect = []
        self.map.deadly_tiles_rect = []
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                block = grid[y][x]
                if block != 0:
                    # display
                    
                    if block not in self.map.HIDDEN_TILES:
                        block_x = self.map.current_offset_x + x * self.map.tile_size
                        block_y = self.map.current_offset_y + y * self.map.tile_size
                        texture = self.map.tiles_texture[block - 1]
                        if isinstance(texture, list):
                            index = pygame.time.get_ticks() // (1000 // len(texture)) % len(texture)
                            screen.blit(texture[index], (block_x, block_y))
                        else:
                            screen.blit(texture, (block_x, block_y))

                    # add collision
                    rect = pygame.rect.Rect(0, 0, self.map.tile_size, self.map.tile_size)
                    rect.topleft = (self.map.current_offset_x + x * self.map.tile_size, self.map.current_offset_y + y * self.map.tile_size)
                    if block not in self.map.TRANSPARENT_TILES:
                        self.map.tiles_rect.append(rect)
                    if block in self.map.INTERACTION_TILES:
                        self.map.interaction_tiles_rect.append({"type": block, "rect": rect, "pos": (x, y)})

                    if block in self.map.DEADLY_TILES:
                        self.map.deadly_tiles_rect.append(rect)

        for bubble in self.map.placed_bubbles:
            screen.blit(bubble.texture, bubble.rect)
            
        screen.blit(self.player.texture, self.player.rect)

        if self.checkpoint_time != None:
            black = pygame.Surface(self.main.screen_size)
            black.fill((0, 0, 0))
            black.set_alpha((pygame.time.get_ticks() - self.checkpoint_time) * 255 // 2000)
            screen.blit(black, (0, 0))


    def calculations(self):
        player = self.player
        previous_player_pos = list(player.rect.topleft)
        dt = self.dt * 60
        keys = pygame.key.get_pressed()
        screen_size = self.main.screen_size

        if not player.in_bubble:
            if player.rect.top >= self.map.current_offset_y + screen_size[1]:
                self.__init__(self.main, self.level_num)
                return

            if not player.collide_bottom and not player.bubble_mod:
                if player.y_momentum < player.max_y_momentum:
                    player.y_momentum = min(
                        player.y_momentum + player.y_acceleration * dt,
                        player.max_y_momentum
                    )

            elif not player.bubble_mod:
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
                if player.rect.colliderect(rect) and not player.bubble_mod:
                    if t == self.map.INTERACTION_TILES_ID["red-bubble"]:
                        player.pos = [rect.x, rect.y + player.rect.height/2]
                        player.in_bubble = True
                        player.x_momentum = 0
                        player.y_momentum = 0
                        player.bubble_pos = p
                    if t == self.map.INTERACTION_TILES_ID["green-bubble"]:
                        player.bubble_pos = p
                        player.x_momentum = -player.x_momentum * 2
                        player.y_momentum = -min(player.y_momentum * 1.3, player.max_y_momentum/1.2)
                        x, y = self.player.bubble_pos
                        self.map.grid[y][x] = 0
                    if t == self.map.INTERACTION_TILES_ID["checkpoint"] and self.checkpoint_time == None:
                        self.checkpoint_time = pygame.time.get_ticks()

                    if t == self.map.INTERACTION_TILES_ID["blue-bubble"]:
                        player.x_momentum = 0
                        player.y_momentum = 0
                        player.bubble_pos = p
                        x, y = self.player.bubble_pos
                        self.map.grid[y][x] = 0
                        self.map.placed_bubbles.append(Bubble(1, [x * self.map.tile_size, y * self.map.tile_size]))
                        # self.map.placed_bubbles.append(Bubble(1, ((self.map.current_offset_x + x * self.map.tile_size)+self.map.tile_size/2, (self.map.current_offset_y + y * self.map.tile_size)+self.map.tile_size/2), self.map.current_offset_x, self.map.current_offset_y, x * self.map.tile_size, y * self.map.tile_size))

            for tile in self.map.deadly_tiles_rect:
                if player.rect.colliderect(tile) and not player.bubble_mod:
                    self.__init__(self.main, self.level_num)

            for bubble in self.map.placed_bubbles:
                if player.rect.colliderect(bubble.rect):
                    if player.bubble_mod and self.player.bubble_color == bubble.color:
                        self.map.placed_bubbles.remove(bubble)

                    elif not player.bubble_mod:
                        if bubble.color == 2:
                            player.pos = [bubble.rect.x, bubble.rect.y + player.rect.height / 2]
                            player.in_bubble = True
                            player.x_momentum = 0
                            player.y_momentum = 0
                            player.bubble_pos = bubble.pos
                            self.player.bubble_element = bubble

                        if bubble.color == 3:
                            player.bubble_pos = bubble.pos
                            player.x_momentum = -player.x_momentum * 2
                            player.y_momentum = -min(player.y_momentum * 1.3, player.max_y_momentum / 1.2)
                            self.map.placed_bubbles.remove(bubble)

                        if bubble.color == 1:
                            # player.rect.center = bubble.rect.center
                            player.x_momentum = 0
                            player.y_momentum = 0
                            bubble.falling = True
                            player.on_falling_bubble = True

                if bubble.falling:
                    bubble.default_y += 0.5
                bubble.pos = [self.map.current_offset_x + bubble.default_x, self.map.current_offset_y + bubble.default_y]
                bubble.update_rect()

                b = False
                for tile in self.map.tiles_rect:
                    if tile.collidepoint(bubble.rect.center):
                        self.map.placed_bubbles.remove(bubble)
                        break
                else:
                    b = True

                if b:
                    if bubble.rect.y >= screen_size[1] - self.map.max_offset_y:
                        self.map.placed_bubbles.remove(bubble)



        else:
            player.pos = previous_player_pos
            self.controls_in_bubble(keys)

        self.control_any(keys)
        player.update_rect()

    def control_any(self, keys):
        pass

        if keys[control_keys["SWITCH_BLUE"]]:
            self.player.change_buble_color(1)
        if keys[control_keys["SWITCH_RED"]]:
            self.player.change_buble_color(2)
        if keys[control_keys["SWITCH_GREEN"]]:
            self.player.change_buble_color(3)

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


        # Bubble Mode
        if self.player.bubble_mod:
            if keys[control_keys["UP"]] and self.player.y_momentum > -self.player.max_x_momentum:
                self.player.y_momentum -= self.player.x_acceleration * dt
            if keys[control_keys["DOWN"]] and self.player.y_momentum < self.player.max_x_momentum:
                self.player.y_momentum += self.player.x_acceleration * dt

            if not keys[control_keys["UP"]] and not keys[control_keys["DOWN"]]:
                if self.player.y_momentum > 0:
                    self.player.y_momentum -= self.player.x_acceleration * dt
                elif self.player.y_momentum < 0:
                    self.player.y_momentum += self.player.x_acceleration * dt

                if -0.5 < self.player.y_momentum < 0.5:
                    self.player.y_momentum = 0






        # if player goes over the speed limit (exemple: dashes)
        if self.player.x_momentum > self.player.max_x_momentum + 2:
            self.player.x_momentum -= self.player.x_acceleration * dt * 2
        if self.player.x_momentum < -self.player.max_x_momentum - 2:
            self.player.x_momentum += self.player.x_acceleration * dt * 2
        if self.player.y_momentum > self.player.max_y_momentum + 2:
            self.player.y_momentum -= self.player.y_acceleration * dt
        if self.player.y_momentum < -self.player.max_y_momentum - 2:
            self.player.y_momentum += self.player.y_acceleration * dt

        if keys[control_keys["JUMP"]] and (self.player.collide_bottom or self.player.on_falling_bubble):
            self.player.on_falling_bubble = False
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
            try:
                x, y = self.player.bubble_pos
                self.map.grid[y][x] = 0
            except IndexError:
                pass
            try:
                self.map.placed_bubbles.remove(self.player.bubble_element)
            except ValueError:
                pass

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
                    
                if (event.key == control_keys["BUBBLE"] and self.player.x_momentum == 0 and -0.5 < self.player.y_momentum < 0.5 and not self.player.in_bubble) or (event.key == control_keys["BUBBLE"] and self.player.bubble_mod):
                    self.player.toggle_bubble_mod(self.map)

                if not len(self.map.placed_bubbles) >= 3:
                    if event.key == control_keys["SPAWN_BUBBLE_UP"] and self.player.bubble_mod:
                        self.map.placed_bubbles.append(Bubble(self.player.bubble_color, [self.player.rect.left - self.map.current_offset_x, self.player.rect.top - self.map.current_offset_y - 60]))
                    if event.key == control_keys["SPAWN_BUBBLE_DOWN"] and self.player.bubble_mod:
                        self.map.placed_bubbles.append(Bubble(self.player.bubble_color, [self.player.rect.left - self.map.current_offset_x, self.player.rect.top - self.map.current_offset_y + 60]))
                    if event.key == control_keys["SPAWN_BUBBLE_LEFT"] and self.player.bubble_mod:
                        self.map.placed_bubbles.append(Bubble(self.player.bubble_color, [self.player.rect.left - self.map.current_offset_x - 60, self.player.rect.top - self.map.current_offset_y]))
                    if event.key == control_keys["SPAWN_BUBBLE_RIGHT"] and self.player.bubble_mod:
                        self.map.placed_bubbles.append(Bubble(self.player.bubble_color, [self.player.rect.left - self.map.current_offset_x + 60, self.player.rect.top - self.map.current_offset_y]))

        if self.checkpoint_time != None and pygame.time.get_ticks() - self.checkpoint_time >= 2000:
            self.__init__(self.main, self.level_num + 1)
