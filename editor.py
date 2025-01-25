#!/usr/bin/env python3

import pygame
from queue import Queue


class Editor:

    PLAYER_TILE_INDEX = 0

    def __init__(self, filename):
        self.filename = filename

        pygame.init()
        pygame.display.set_caption("Bubble Passage Editor")
        self.screen = pygame.display.set_mode((1080, 720))
        self.clock = pygame.time.Clock()
        self.max_fps = 60

        self.load_textures()

        self.tile_width = self.textures[1].get_width()
        self.tile_height = self.textures[1].get_height()
        self.grid_width = self.screen.get_width() // self.tile_width
        self.grid_height = self.screen.get_height() // self.tile_height
        self.tiles = [[-1] * self.grid_width for _ in range(self.grid_height)]
        self.tiles[1][1] = 0
        self.current_tile = 1

        self.load()

        self.loop()


    def load_textures(self):
        filenames = ['player', 'wall', 'hurt-down']
        self.textures = [
            pygame.image.load('src/textures/{}.png'.format(name)).convert_alpha()
            for name in filenames
        ]


    def loop(self):
        self.playing = True
        while self.playing:
            self.render()
            pygame.display.flip()

            self.check_events()

            self.clock.tick(self.max_fps)


    def centered_tile(self, x, y, texture):
        tile_x = self.tile_width * x + (self.tile_width - texture.get_width()) // 2
        tile_y = self.tile_height * y + (self.tile_height - texture.get_height()) // 2
        return tile_x, tile_y

    def render(self):
        screen = self.screen
        screen.fill((128, 128, 255))

        for y in range(self.grid_height):
            for x in range(self.grid_width):
                tile = self.tiles[y][x]
                if tile >= 0:
                    tile_x, tile_y = self.centered_tile(x, y, self.textures[tile])
                    screen.blit(self.textures[tile], (tile_x, tile_y))

        current_texture = self.textures[self.current_tile].copy()
        current_texture.set_alpha(128)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        tile_x, tile_y = self.centered_tile(
            mouse_x // self.tile_width, mouse_y // self.tile_height, current_texture)
        screen.blit(current_texture, (tile_x, tile_y))


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            elif event.type == pygame.MOUSEWHEEL:
                self.current_tile = (self.current_tile - event.y) % len(self.textures)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.save()

        mouse_buttons = pygame.mouse.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        tile_x = min(max(0, mouse_x // self.tile_width), self.grid_width - 1)
        tile_y = min(max(0, mouse_y // self.tile_height), self.grid_height - 1)
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


    tile_codes = ['-', ' ', 'P', 'W', '^']

    def mark_reachable(self):
        reachable = [[False] * self.grid_width for _ in range(self.grid_height)]
        queue = Queue()
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.tiles[y][x] == Editor.PLAYER_TILE_INDEX:
                    reachable[y][x] = True
                    queue.put((x, y))
        while not queue.empty():
            x, y = queue.get()
            for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                x2 = x + dx
                y2 = y + dy
                if 0 <= x2 < self.grid_width and 0 <= y2 < self.grid_height \
                        and not reachable[y2][x2]:
                    reachable[y2][x2] = True
                    if self.tiles[y2][x2] < 0:
                        queue.put((x2, y2))
        return reachable

    def save(self):
        reachable = self.mark_reachable()
        with open(self.filename, "w") as file:
            for y in range(self.grid_height):
                for x in range(self.grid_width):
                    tile = self.tiles[y][x]
                    if tile == 1 and not reachable[y][x]:
                        tile = -2
                    file.write(Editor.tile_codes[tile + 2])
                file.write('\n')

    def load(self):
        try:
            with open(self.filename, "r") as file:
                lines = file.readlines()
                self.grid_width = len(lines[0]) - 1
                self.grid_height = len(lines)
                self.tiles = [[-1] * self.grid_width for _ in range(self.grid_height)]
                for y in range(self.grid_height):
                    for x in range(self.grid_width):
                        tile = Editor.tile_codes.index(lines[y][x]) - 2
                        self.tiles[y][x] = 1 if tile == -2 else tile
        except:
            pass


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: ./editor.py <filename>")
    else:
        print("Press S to save.")
        Editor(sys.argv[1])
