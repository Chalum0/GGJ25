from src.entities.gameobj import GameObj
import pygame

class Player(GameObj):

    def __init__(self):
        self.pos = [0, 0]
        self.texture = None

        self.jump_power = -7

        self.max_x_momentum = 5
        self.max_y_momentum = 15
        self.x_acceleration = .5
        self.y_acceleration = .3
        self.x_momentum = 0
        self.y_momentum = 0

        self.collide_top = False
        self.collide_bottom = False
        self.collide_left = False
        self.collide_right = False

        self.rect = None

        self.load_texture()
        GameObj.__init__(self)

    def load_texture(self):
        self.texture = pygame.image.load('./src/textures/player.png')
        self.texture = pygame.transform.scale(self.texture, (20, 20))
        self.rect = self.texture.get_rect()

    def update_rect(self):
        self.rect.topleft = self.pos
