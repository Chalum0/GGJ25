import random
import pygame
import pickle

class Map:

    INTERACTION_TILES_ID = {
        "green-bubble": 6,
        "red-bubble": 5,
        "blue-bubble": 7,
    }

    TEXTURES = {
        1: "bubble-green",  # stating_point
        2: "full-wall",  # wall with collisions
        3: "urchin",  # damages
        4: "urchin",  # damages
        5: "bubble-red",  # red bubbles
        6: "bubble-green",  # green bubbles
        7: "bubble-blue",  # blue bubbles
        8: "checkpoint",  # checkpoint
        9: "1"  # wall without collisions
    }
    TRANSPARENT_BLOCKS = [1, 5, 6, 7, 8, 9]
    HIDDEN_BLOCKS = [1]
    INTERACTION_BLOCKS = [5, 6, 7]

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
        self.interaction_tiles_rect = []

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

