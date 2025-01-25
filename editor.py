#!/usr/bin/env python3

import pygame
import pickle


class Editor:

    PLAYER_TILE_INDEX = 0
    WALL_TILE_INDEX = 1

    def __init__(self, filename):
        self.filename = filename

        pygame.init()
        pygame.display.set_caption("Bubble Passage Editor")
        self.screen = pygame.display.set_mode((1080, 720))
        pygame.display.set_icon(pygame.image.load('src/textures/crab.png'))
        self.clock = pygame.time.Clock()
        self.max_fps = 60

        self.tile_width = 40
        self.tile_height = 40
        self.grid_width = self.screen.get_width() // self.tile_width
        self.grid_height = self.screen.get_height() // self.tile_height
        self.scroll_x = 0
        self.scroll_y = 0

        self.tiles = [[-1] * self.grid_width for _ in range(self.grid_height)]
        self.tiles[3][1] = 0
        self.current_tile = Editor.WALL_TILE_INDEX

        self.textures = None
        self.wall_textures = None
        self.load_textures()

        self.load()

        self.loop()


    def load_textures(self):
        filenames = ['crab', 'wall', 'urchin', 'urchin', 'bubble-red', 'bubble-green', 'bubble-blue', 'checkpoint']
        self.textures = [None] * len(filenames)
        for index, name in enumerate(filenames):
            texture = pygame.image.load(f'src/textures/{name}.png').convert_alpha()
            texture_height = self.tile_height // 2 if name == 'crab' else self.tile_height
            texture = pygame.transform.scale(texture, (self.tile_width, texture_height))
            self.textures[index] = texture
        directions = ['top', 'bottom', 'left', 'right']
        self.wall_textures = [None] * (2 ** len(directions))
        for index in range(2 ** len(directions)):
            texture_dir = ''
            for dir_index, direction in enumerate(directions):
                if index & 1 << dir_index != 0:
                    texture_dir += direction
            filename = 'wall' if texture_dir == '' else f'wall-{texture_dir}'
            filename = f'src/textures/{filename}.png'
            texture = pygame.image.load(filename).convert_alpha()
            texture = pygame.transform.scale(texture, (self.tile_width, self.tile_height))
            self.wall_textures[index] = texture


    def loop(self):
        self.playing = True
        while self.playing:
            self.render()
            pygame.display.flip()

            self.check_events()

            self.clock.tick(self.max_fps)


    def get_wall_index(self, x, y):
        index = 0
        for dir_index, (dx, dy) in enumerate(((0, -1), (0, 1), (-1, 0), (1, 0))):
            x2, y2 = x + dx, y + dy
            if 0 <= x2 < self.grid_width and 0 <= y2 < self.grid_height \
                    and self.tiles[y2][x2] != Editor.WALL_TILE_INDEX:
                index |= 1 << dir_index
        return index

    def texture_pos_px(self, x, y, texture):
        tile_x = self.tile_width * x + (self.tile_width - texture.get_width()) // 2 - self.scroll_x
        tile_y = self.tile_height * y + (self.tile_height - texture.get_height()) // 2 - self.scroll_y
        return tile_x, tile_y

    def render(self):
        screen = self.screen
        screen.fill((64, 64, 64))
        end_x = self.grid_width * self.tile_width - self.scroll_x
        end_y = self.grid_height * self.tile_height - self.scroll_y
        pygame.draw.rect(screen, (0, 0, 128), (0, 0, end_x, end_y))

        for y in range(self.grid_height):
            for x in range(self.grid_width):
                tile = self.tiles[y][x]
                texture = self.textures[tile]
                if tile >= 0:
                    if tile == Editor.WALL_TILE_INDEX:
                        texture = self.wall_textures[self.get_wall_index(x, y)]
                    tile_x, tile_y = self.texture_pos_px(x, y, texture)
                    screen.blit(texture, (tile_x, tile_y))

        current_texture = self.textures[self.current_tile].copy()
        current_texture.set_alpha(128)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        tile_x, tile_y = self.texture_pos_px(
            (mouse_x + self.scroll_x) // self.tile_width, (mouse_y + self.scroll_y) // self.tile_height,
            current_texture)
        screen.blit(current_texture, (tile_x, tile_y))


    def check_scroll(self, event):
        if event.type == pygame.KEYDOWN:
            if event.scancode == 26: # Z
                if event.mod & pygame.KMOD_SHIFT != 0 and self.grid_height > 1:
                    self.grid_height -= 1
                    self.tiles.pop()
                else:
                    self.scroll_y = max(0, self.scroll_y - self.tile_height)
            elif event.scancode == 4: # Q
                if event.mod & pygame.KMOD_SHIFT != 0 and self.grid_width > 1:
                    self.grid_width -= 1
                    for line in self.tiles:
                        line.pop()
                else:
                    self.scroll_x = max(0, self.scroll_x - self.tile_width)
            elif event.scancode == 22: # S
                if event.mod & pygame.KMOD_SHIFT != 0:
                    self.grid_height += 1
                    self.tiles.append([-1] * self.grid_width)
                else:
                    self.scroll_y += self.tile_height
            elif event.scancode == 7: # D
                if event.mod & pygame.KMOD_SHIFT != 0:
                    self.grid_width += 1
                    for line in self.tiles:
                        line.append(-1)
                else:
                    self.scroll_x += self.tile_width

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            elif event.type == pygame.MOUSEWHEEL:
                self.current_tile = (self.current_tile - event.y) % len(self.textures)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and event.mod & pygame.KMOD_CTRL != 0:
                    self.save()
                elif event.key == pygame.K_o and event.mod & pygame.KMOD_CTRL != 0:
                    self.load()
            self.check_scroll(event)

        mouse_buttons = pygame.mouse.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        tile_x = (mouse_x + self.scroll_x) // self.tile_width
        tile_y = (mouse_y + self.scroll_y) // self.tile_height
        if 0 <= tile_x < self.grid_width and 0 <= tile_y < self.grid_height:
            if mouse_buttons[2]:
                self.tiles[tile_y][tile_x] = -1
            elif mouse_buttons[0]:
                if self.current_tile == Editor.PLAYER_TILE_INDEX:
                    self.remove_player()
                self.tiles[tile_y][tile_x] = self.current_tile

    def remove_player(self):
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.tiles[y][x] == Editor.PLAYER_TILE_INDEX:
                    self.tiles[y][x] = -1


    def save(self):
        with open(self.filename, "wb") as file:
            tiles = [[-1] * self.grid_width for _ in range(self.grid_height)]
            for y in range(self.grid_height):
                for x in range(self.grid_width):
                    tile = self.tiles[y][x]
                    if tile == Editor.WALL_TILE_INDEX:
                        tile = 7 + self.get_wall_index(x, y)
                        tile = Editor.WALL_TILE_INDEX if tile == 7 else tile
                    tile += 1
                    tiles[y][x] = tile
            pickle.dump(tiles, file)

    def load(self):
        try:
            with open(self.filename, "rb") as file:
                self.tiles = pickle.load(file)
                self.grid_width = len(self.tiles[0])
                self.grid_height = len(self.tiles)
                for y in range(self.grid_height):
                    for x in range(self.grid_width):
                        tile = self.tiles[y][x] - 1
                        self.tiles[y][x] = Editor.WALL_TILE_INDEX if tile >= 8 else tile
        except:
            pass


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: ./editor.py <filename>")
    else:
        print("Use Ctrl-S to save.")
        Editor(sys.argv[1])
