from src.entities.gameobj import GameObj
import pygame

class Bubble(GameObj):

    RED = 0
    GREEN = 1
    BLUE = 2

    def __init__(self, type):
        super().__init__()
        self.type = type
        name = ['red', 'green', 'blue'][self.type]
        self.texture = pygame.image.load(f'./src/textures/bubble-{name}.png').convert_alpha()
