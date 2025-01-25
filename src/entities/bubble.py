from src.entities.gameobj import GameObj
import pygame

class Bubble(GameObj):

    BLUE = 0
    RED = 1
    GREEN = 2

    def __init__(self, type):
        super().__init__()
        self.type = type

    def load_texture(self, **kwargs):
        name = ['blue', 'red', 'green'][self.type]
        self.texture = pygame.image.load(f'./src/textures/bubble-{name}.png')