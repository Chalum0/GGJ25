import random
import pygame

class Map:
    def __init__(self):
        self.tile_size = 40
        self.grid = [[random.choice([0, 0, 0, 0, 1]) for i in range(self.tile_size)] for j in range(self.tile_size)]
        self.tiles_texture = []
        self.tiles_amount = 1

        self.tiles_rect = []

        self.load_textures()

    def get_value(self, x, y):
        return self.grid[x][y]

    def set_value(self, x, y, value):
        self.grid[x][y] = value

    def load_map(self):
        pass

    def load_textures(self):
        for i in range(self.tiles_amount):
            self.tiles_texture.append(pygame.image.load(f'src/textures/{i+1}.png'))

