from src.entities.gameobj import GameObj
import pygame

class Bubble(GameObj):

    BLUE = 0
    RED = 1
    GREEN = 2

    def __init__(self, type):
        GameObj.__init__(self)
        self.type = type

    def load_texture(self):
        name = ['blue', 'red', 'green'][self.type]
        self.texture = pygame.image.load('./src/textures/bubble-{}.png'.format(name))
