import random
import pygame
import pickle

class Map:

    TEXTURES = {
        1: "1",
        2: "full-wall",
        3: "urchin",
        4: "urchin",
        5: "bubble-red",
        6: "bubble-green",
        7: "bubble-blue",
        8: "checkpoint",
        9: "1"
    }

    def __init__(self, screen_size):
        self.tile_size = 40
        self.grid = None
        self.load_map(1)
        print(len(self.grid))
        self.min_offset_x = 0
        self.max_offset_x = - len(self.grid[0]) * self.tile_size + screen_size[0]
        self.min_offset_y = 0
        self.max_offset_y = - len(self.grid) * self.tile_size + screen_size[1]
        self.current_offset_x = self.min_offset_x
        self.current_offset_y = self.min_offset_y
        self.tiles_texture = []
        self.tiles_amount = len(self.TEXTURES)

        self.tiles_rect = []

        self.load_textures()

    def get_value(self, x, y):
        return self.grid[x][y]

    def set_value(self, x, y, value):
        self.grid[x][y] = value

    def load_map(self, lvl):
        self.grid: list = pickle.load(open(f"./levels/{lvl}.pickle", "rb"))

    def load_textures(self):
        for i in range(self.tiles_amount):
            self.tiles_texture.append(pygame.transform.scale(pygame.image.load(f'src/textures/{self.TEXTURES[i+1]}.png').convert_alpha(), (self.tile_size, self.tile_size)))

