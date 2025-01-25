import pygame

class GameObj:

    def __init__(self):
        self.pos = [0, 0]
        self.texture = None
        self.rect = None

        self.max_x_momentum = 6
        self.max_y_momentum = 15
        self.x_acceleration = .5
        self.y_acceleration = .3
        self.x_momentum = 0
        self.y_momentum = 0


    def load_texture(self, path):
        self.texture = pygame.image.load('./src/textures/player.png')
        self.texture = pygame.transform.scale(self.texture, (20, 20))
        self.rect = self.texture.get_rect()

    def update_rect(self):
        self.rect.topleft = self.pos
