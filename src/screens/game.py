from src.entities.bubble import Bubble
from src.entities.player import Player
from src.settings.settings import *
from src.map import Map
from src.screens.win import Win
from src.draw import *
import pygame
import json
import math
from typing import Any


class Game:
    def __init__(self, main, level_num=1):
        self.main = main
        self.level_num = level_num
        self.playing = True
        self.dt = 0
        self.keys = [False] * 500

        self.font = pygame.font.SysFont("Liberation Sans", 30)
        self.jump_sound = pygame.mixer.Sound('src/audio/jump.wav')
        self.death_sound = pygame.mixer.Sound('src/audio/death.wav')
        self.bubble_spawn_sound = pygame.mixer.Sound('src/audio/bubble-spawn.wav')
        self.bubble_burst_sound = pygame.mixer.Sound('src/audio/bubble-burst.wav')

        json.dump(self.level_num, open('src/settings/save.json', 'w'))

        try:
            self.map = Map(str(level_num), self.main.screen_size)
            player_pos = [coord * self.map.tile_size for coord in self.map.player_pos]
            self.player = Player(player_pos)
            self.checkpoint_time = None

        except: # Map loading failed
            Win(self.main)
            self.playing = False


    def reset(self):
        self.__init__(self.main, self.level_num)

    def die(self):
        if self.player.death_time == None:
            self.death_sound.play()
            self.player.death_time = 0
            level_bottom = len(self.map.grid) * self.map.tile_size
            self.player.pos[1] = min(self.player.pos[1], level_bottom - 20)
            self.player.update_rect()

    def jump(self):
        self.player.jumping = True
        self.jump_sound.play()


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

        screen.fill((64, 64, 64))
        draw_vertical_gradient(self.main)

        for y in range(len(grid)):
            for x in range(len(grid[y])):
                block = grid[y][x]
                if block not in self.map.HIDDEN_TILES:
                    block_x = x * self.map.tile_size - self.map.scroll_x
                    block_y = y * self.map.tile_size - self.map.scroll_y
                    texture = self.map.tiles_texture[block - 1]
                    if isinstance(texture, list):
                        index = pygame.time.get_ticks() * len(texture) // 1000 % len(texture)
                        screen.blit(texture[index], (block_x, block_y))
                    else:
                        screen.blit(texture, (block_x, block_y))

        for bubble in self.map.placed_bubbles:
            bubble_x = bubble.pos[0] - self.map.scroll_x
            bubble_y = bubble.pos[1] - self.map.scroll_y
            screen.blit(bubble.texture, (bubble_x, bubble_y))

        self.player.draw(screen, self.map)

        if self.checkpoint_time != None:
            black = pygame.Surface(self.main.screen_size)
            black.fill((0, 0, 0))
            black.set_alpha((pygame.time.get_ticks() - self.checkpoint_time) * 255 // 2000)
            screen.blit(black, (0, 0))


    def calculations(self):
        self.select_map_tiles()
        if self.player.death_time == None:
            self.alive_calculations()
        else:
            self.player.death_time += self.dt
            if self.player.death_time > Player.DYING_TIME:
                self.reset()

    def select_map_tiles(self):
        grid = self.map.grid
        self.map.tiles_rect = []
        self.map.interaction_tiles_rect = []
        self.map.deadly_tiles_rect = []
        for y, row in enumerate(grid):
            for x, block in enumerate(row):
                if block not in self.map.HIDDEN_TILES:
                    rect_x = x * self.map.tile_size
                    rect_y = y * self.map.tile_size
                    rect = pygame.rect.Rect(rect_x, rect_y, self.map.tile_size, self.map.tile_size)
                    if block not in self.map.TRANSPARENT_TILES:
                        self.map.tiles_rect.append(rect)
                    if block in self.map.INTERACTION_TILES:
                        self.map.interaction_tiles_rect.append({"type": block, "rect": rect, "pos": (x, y)})
                    if block in self.map.DEADLY_TILES:
                        self.map.deadly_tiles_rect.append(rect)

    def alive_calculations(self):
        player = self.player
        previous_player_pos = list(player.rect.topleft)
        if not player.in_bubble:
            self.player_calculations()
        else:
            player.pos = previous_player_pos
        player.update_rect()

        self.bubble_falling()

    def player_calculations(self):
        player = self.player
        previous_player_pos = list(player.rect.topleft)
        dt = self.dt * 60

        def player_fall():
            if player.rect.bottom >= len(self.map.grid) * self.map.tile_size:
                self.die()
                return True
            elif not player.bubble_mode:
                if not player.collide_bottom:
                    if player.y_momentum < player.max_y_momentum:
                        player.y_momentum = min(
                            player.y_momentum + player.y_acceleration * dt,
                            player.max_y_momentum
                        )
                    else:
                        player.y_momentum = 0
            player.collide_bottom = False
            return False
        if player_fall():
            return

        self.move_obj(player, dt)

        def scrolling():
            map = self.map
            screen_size = self.main.screen_size
            sight_x = screen_size[0] * .4
            sight_y = screen_size[1] * .4
            map.scroll_x = max(player.pos[0] - screen_size[0] + sight_x, min(map.scroll_x, player.pos[0] - sight_x))
            map.scroll_x = max(map.min_scroll_x, min(map.scroll_x, map.max_scroll_x))
            map.scroll_y = max(player.pos[1] - screen_size[1] + sight_y, min(map.scroll_y, player.pos[1] - sight_y))
            map.scroll_y = max(map.min_scroll_y, min(map.scroll_y, map.max_scroll_y))
        scrolling()

        def tile_interaction(tile):
            trect = tile["rect"]
            ttyp = tile["type"]
            tpos = tile["pos"]
            if player.rect.colliderect(trect):
                if ttyp == self.map.INTERACTION_TILES_ID["red-bubble"]:
                    player.pos = [trect.x, trect.y + player.rect.height/2]
                    player.in_bubble = True
                    player.x_momentum = 0
                    player.y_momentum = 0
                    player.bubble_pos = tpos
                elif ttyp == self.map.INTERACTION_TILES_ID["green-bubble"]:
                    player.bubble_pos = tpos
                    player.x_momentum = -player.x_momentum * 2
                    player.y_momentum = -min(player.y_momentum * 1.3, player.max_y_momentum/1.2)
                    x, y = self.player.bubble_pos
                    self.map.grid[y][x] = 0
                elif ttyp == self.map.INTERACTION_TILES_ID["blue-bubble"]:
                    player.x_momentum = 0
                    player.y_momentum = 0
                    player.bubble_pos = tpos
                    x, y = self.player.bubble_pos
                    self.map.grid[y][x] = 0
                    self.map.placed_bubbles.append(Bubble(1, [x * self.map.tile_size, y * self.map.tile_size], False))
                elif ttyp == self.map.INTERACTION_TILES_ID["checkpoint"] and self.checkpoint_time == None:
                    self.checkpoint_time = pygame.time.get_ticks()

        def bubble_interaction(bubble):
            if player.rect.colliderect(bubble.rect):
                if bubble.color == Bubble.BLUE:
                    player.x_momentum = 0
                    player.y_momentum = 0
                    bubble.falling = True
                    player.on_falling_bubble = True
                elif bubble.color == Bubble.RED:
                    player.pos = [bubble.rect.x, bubble.rect.y + player.rect.height / 2]
                    player.in_bubble = True
                    player.x_momentum = 0
                    player.y_momentum = 0
                    player.bubble_pos = bubble.pos
                    self.player.bubble_element = bubble
                elif bubble.color == Bubble.GREEN:
                    player.bubble_pos = bubble.pos
                    player.x_momentum = -player.x_momentum * 2
                    player.y_momentum = -min(player.y_momentum * 1.3, player.max_y_momentum / 1.2)
                    self.map.placed_bubbles.remove(bubble)

        if not player.bubble_mode:
            for tile in self.map.interaction_tiles_rect:
                tile_interaction(tile)
            for tile in self.map.deadly_tiles_rect:
                if player.rect.colliderect(tile):
                    self.die()
            for bubble in self.map.placed_bubbles:
                bubble_interaction(bubble)

        else:
            for bubble in self.map.placed_bubbles:
                if self.player.bubble_color == bubble.color and player.rect.colliderect(bubble.rect):
                    self.map.placed_bubbles.remove(bubble)

    def bubble_falling(self):
        for bubble in self.map.placed_bubbles:
            if bubble.falling:
                bubble.pos[1] += self.dt * 30
            bubble.update_rect()
            bubble.update_texture()

            """
            ???
            for tile in self.map.tiles_rect:
                if tile.collidepoint(bubble.rect.center):
                    self.map.placed_bubbles.remove(bubble)
                    break
            """
            if bubble.rect.bottom >= len(self.map.grid) * self.map.tile_size:
                self.map.placed_bubbles.remove(bubble)


    def controls_any_state(self):
        if self.keys[control_keys["SWITCH_BLUE"]]:
            self.player.change_bubble_color(Bubble.BLUE)
        if self.keys[control_keys["SWITCH_RED"]]:
            self.player.change_bubble_color(Bubble.RED)
        if self.keys[control_keys["SWITCH_GREEN"]]:
            self.player.change_bubble_color(Bubble.GREEN)

    def controls(self):
        dt = self.dt * 60
        if self.keys[control_keys["LEFT"]] and self.player.x_momentum > -self.player.max_x_momentum:
            self.player.x_momentum -= self.player.x_acceleration * dt
        if self.keys[control_keys["RIGHT"]] and self.player.x_momentum < self.player.max_x_momentum:
            self.player.x_momentum += self.player.x_acceleration * dt

        if not self.keys[control_keys["LEFT"]] and not self.keys[control_keys["RIGHT"]]:
            if self.player.x_momentum > 0:
                self.player.x_momentum -= self.player.x_acceleration * dt
            elif self.player.x_momentum < 0:
                self.player.x_momentum += self.player.x_acceleration * dt

            if -0.5 < self.player.x_momentum < 0.5:
                self.player.x_momentum = 0

        if self.player.bubble_mode:
            if self.keys[control_keys["UP"]] and self.player.y_momentum > -self.player.max_x_momentum:
                self.player.y_momentum -= self.player.x_acceleration * dt
            if self.keys[control_keys["DOWN"]] and self.player.y_momentum < self.player.max_x_momentum:
                self.player.y_momentum += self.player.x_acceleration * dt

            if not self.keys[control_keys["UP"]] and not self.keys[control_keys["DOWN"]]:
                if self.player.y_momentum > 0:
                    self.player.y_momentum -= self.player.x_acceleration * dt
                elif self.player.y_momentum < 0:
                    self.player.y_momentum += self.player.x_acceleration * dt

                if -0.5 < self.player.y_momentum < 0.5:
                    self.player.y_momentum = 0

        # if player goes over the speed limit (example: dashes)
        if self.player.x_momentum > self.player.max_x_momentum + 2:
            self.player.x_momentum -= self.player.x_acceleration * dt * 2
        if self.player.x_momentum < -self.player.max_x_momentum - 2:
            self.player.x_momentum += self.player.x_acceleration * dt * 2
        if self.player.y_momentum > self.player.max_y_momentum + 2:
            self.player.y_momentum -= self.player.y_acceleration * dt
        if self.player.y_momentum < -self.player.max_y_momentum - 2:
            self.player.y_momentum += self.player.y_acceleration * dt

        if self.keys[control_keys["JUMP"]] and (self.player.collide_bottom or self.player.on_falling_bubble):
            self.player.on_falling_bubble = False
            self.player.collide_bottom = False
            self.player.y_momentum = self.player.jump_power
            self.jump()

    def controls_in_bubble(self):
        if self.keys[control_keys["JUMP"]]:
            horizontal_speed = 20
            if self.keys[control_keys["LEFT"]] and self.keys[control_keys["JUMP"]]:
                self.player.x_momentum = -horizontal_speed
            if self.keys[control_keys["RIGHT"]] and self.keys[control_keys["JUMP"]]:
                self.player.x_momentum = horizontal_speed
            if self.keys[control_keys["UP"]] and self.keys[control_keys["JUMP"]]:
                self.player.y_momentum = self.player.jump_power
            if self.keys[control_keys["DOWN"]] and self.keys[control_keys["JUMP"]]:
                self.player.y_momentum = 10
            if self.keys[control_keys["RIGHT"]] or self.keys[control_keys["LEFT"]] or self.keys[control_keys["UP"]] or self.keys[control_keys["DOWN"]]:
                self.player.in_bubble = False
                self.jump()
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
                if obj == self.player:
                    self.player.jumping = False
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
        bound_on_right(len(self.map.grid[0]) * self.map.tile_size)
        for tile in tls:
            if not obj.rect.colliderect(tile):
                continue
            bound_on_left(tile.right)
            bound_on_right(tile.left)
        obj.update_rect()

    def place_bubble(self, dx, dy):
        x = self.player.rect.centerx + dx
        y = self.player.rect.centery + dy
        self.map.placed_bubbles.append(Bubble(self.player.bubble_color, [x, y]))

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.main.quit = True

            elif event.type == pygame.KEYDOWN:
                self.keys[event.scancode] = True

                if event.scancode == control_keys["RESET"]:
                    self.reset()
                elif event.key == pygame.K_ESCAPE:
                    self.playing = False
                    
                if event.scancode == control_keys["BUBBLE"]:
                    if self.player.in_bubble:
                        self.player.toggle_bubble_mode(self.map)
                    elif self.player.x_momentum == 0 and -0.5 < self.player.y_momentum < 0.5:
                        self.player.toggle_bubble_mode(self.map)

                if len(self.map.placed_bubbles) < 3 and self.player.bubble_mode:
                    distance = 50
                    if event.scancode == control_keys["SPAWN_BUBBLE_UP"]:
                        self.place_bubble(0, -distance)
                    if event.scancode == control_keys["SPAWN_BUBBLE_DOWN"]:
                        self.place_bubble(0, distance)
                    if event.scancode == control_keys["SPAWN_BUBBLE_LEFT"]:
                        self.place_bubble(-distance, 0)
                    if event.scancode == control_keys["SPAWN_BUBBLE_RIGHT"]:
                        self.place_bubble(distance, 0)

            elif event.type == pygame.KEYUP:
                self.keys[event.scancode] = False

        if not self.player.in_bubble:
            self.controls()
        else:
            self.controls_in_bubble()
        self.controls_any_state()

        if self.checkpoint_time != None and pygame.time.get_ticks() - self.checkpoint_time >= 2000:
            self.__init__(self.main, self.level_num + 1)
