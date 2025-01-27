import pygame
import pickle

class Map:

    INTERACTION_TILES_ID = {
        "red-bubble": 5,
        "green-bubble": 6,
        "blue-bubble": 7,
        "checkpoint": 8,
    }

    TEXTURES = {
        2: "wall",  # wall without collisions
        3: ["urchin1", "urchin2"],  # damages
        4: ["urchin2", "urchin1"],  # damages
        5: [f"bubble-red{i}" for i in range(1, 5)],  # red bubbles
        6: [f"bubble-green{i}" for i in range(1, 5)],  # green bubbles
        7: [f"bubble-blue{i}" for i in range(1, 5)],  # blue bubbles
        8: ["crabette1", "crabette2"],  # checkpoint
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
        24: "plant1",
        25: "plant2",
        26: "plant3",
        27: "plant4",
        28: "bigplant1",
        29: "bigplant2",
    }
    TRANSPARENT_TILES = [1, 2, 3, 4, 5, 6, 7, 8, 24, 25, 26, 27, 28, 29]
    HIDDEN_TILES = [0, 1]
    INTERACTION_TILES = [5, 6, 7, 8]
    DEADLY_TILES = [3, 4]

    def __init__(self, level_name, screen_size):
        self.tile_size = 40
        self.grid = None
        self.player_pos = (0, 0)
        self.load_map(level_name)
        self.min_scroll_x = 0
        self.max_scroll_x = max(0, len(self.grid[0]) * self.tile_size - screen_size[0])
        self.min_scroll_y = 0
        self.max_scroll_y = max(0, len(self.grid) * self.tile_size - screen_size[1])
        self.scroll_x = self.min_scroll_x
        self.scroll_y = self.min_scroll_y

        self.tiles_texture = [None]
        self.tiles_rect = []
        self.interaction_tiles_rect = []
        self.deadly_tiles_rect = []

        self.placed_bubbles = []

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
        for names in self.TEXTURES.values():
            if isinstance(names, list):
                textures = [pygame.image.load(f'src/textures/{name}.png').convert_alpha() for name in names]
                textures = [pygame.transform.scale(texture, (self.tile_size, self.tile_size)) for texture in textures]
                self.tiles_texture.append(textures)
            else:
                texture = pygame.image.load(f'src/textures/{names}.png').convert_alpha()
                texture = pygame.transform.scale(texture, (self.tile_size, self.tile_size))
                self.tiles_texture.append(texture)
