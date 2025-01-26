from src.entities.gameobj import GameObj
import pygame
from src.entities.bubblesTextureLoader import *


class Bubble(GameObj):

    BLUE = 1
    RED = 2
    GREEN = 3

    def __init__(self, color: int, pos: list):
        super().__init__()
        self.size = 40
        self.color = color
        self.pos = pos
        self.texture = bubbles_textures[color]
        self.rect = self.texture.get_rect()
        self.rect.center = pos
        self.pos = self.rect.topleft
        self.falling = False
        self.default_x = pos[0]
        self.default_y = pos[1]
