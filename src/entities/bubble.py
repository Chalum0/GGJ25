from src.entities.gameobj import GameObj
import pygame
from src.entities.bubblesTextureLoader import *


class Bubble(GameObj):

    BLUE = 1
    RED = 2
    GREEN = 3

    def __init__(self, color: int, pos: list, x_offset: int, y_offset: int, default_x: int, default_y: int):
        super().__init__()
        self.size = 40
        self.color = color
        self.pos = pos
        self.texture = bubbles_textures[color]
        self.rect = self.texture.get_rect()
        self.rect.center = pos
        self.pos = self.rect.topleft
        self.falling = False
        self.default_x = default_x
        self.default_y = default_y
        self.current_x_offset = x_offset
        self.current_y_offset = y_offset
