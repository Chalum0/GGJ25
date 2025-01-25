from src.entities.gameobj import GameObj
import pygame

class Player(GameObj):

    def __init__(self):
        GameObj.__init__(self)

    def load_texture(self):
        self.texture = pygame.image.load('./src/textures/player.png')
