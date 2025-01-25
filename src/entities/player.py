import pygame

class Player:

    def __init__(self):
        self.pos = [0, 0]
        self.texture = None
        self.load_texture()

    def load_texture(self):
        self.texture = pygame.image.load('./src/textures/player.png')
