import pygame
import pickle

class Map:

    INTERACTION_TILES_ID = {
        "red-bubble": 5,
        "green-bubble": 6,
        "blue-bubble": 7,
    }

    TEXTURES = {
        2: "wall",  # wall without collisions
        3: "urchin",  # damages
        4: "urchin",  # damages
        5: "bubble-red",  # red bubbles
        6: "bubble-green",  # green bubbles
        7: "bubble-blue",  # blue bubbles
        8: "checkpoint",  # checkpoint
        9: "wall-top",
        10: "wall-bottom",
        11: "wall-topbottom",
        12: "wall-left",
        13: "wall-topleft",
        14: "wall-bottomleft",
        15: "wall-topbottomleft",
        16: "wall-right",
        17: "wall-topright",
        18: "wall-bottomright",
        19: "wall-topbottomright",
        20: "wall-leftright",
        21: "wall-topleftright",
        22: "wall-bottomleftright",
        23: "wall-topbottomleftright",
    }
    TRANSPARENT_BLOCKS = [1, 2, 5, 6, 7, 8]
    HIDDEN_BLOCKS = [1]
    INTERACTION_BLOCKS = [5, 6, 7]

    def __init__(self, level_name, screen_size):
        self.tile_size = 40
        self.grid = None
        self.player_pos = (0, 0)
        self.load_map(level_name)

        self.min_offset_x = 0
        self.max_offset_x = - len(self.grid[0]) * self.tile_size + screen_size[0]
        self.min_offset_y = 0
        self.max_offset_y = - len(self.grid) * self.tile_size + screen_size[1]
        self.current_offset_x = self.min_offset_x
        self.current_offset_y = self.min_offset_y

        self.tiles_texture = [None]
        self.tiles_rect = []
        self.interaction_tiles_rect = []

        self.load_textures()

    def get_value(self, x, y):
        return self.grid[x][y]

    def set_value(self, x, y, value):
        self.grid[x][y] = value

    def load_map(self, level_name):
        self.grid: list = pickle.load(open(f"./levels/{level_name}.pickle", "rb"))
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == 1:
                    self.player_pos = (x, y)
                    self.grid[y][x] = 0

    def load_textures(self):
        for name in self.TEXTURES.values():
            texture = pygame.image.load(f'src/textures/{name}.png').convert_alpha()
            texture = pygame.transform.scale(texture, (self.tile_size, self.tile_size))
            self.tiles_texture.append(texture)
