from src.entities.gameobj import GameObj
import pygame


bubbles_textures = {
    1: pygame.transform.scale(pygame.image.load(f'./src/textures/bubble-blue1.png'), (40, 40)),
    2: pygame.transform.scale(pygame.image.load(f'./src/textures/bubble-red1.png'), (40, 40)),
    3: pygame.transform.scale(pygame.image.load(f'./src/textures/bubble-green1.png'), (40, 40))
}


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
