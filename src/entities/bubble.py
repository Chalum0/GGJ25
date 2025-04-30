from src.entities.gameobj import GameObj
import pygame


bubble_color_names = ['blue', 'red', 'green']
bubble_textures = [
    [pygame.image.load(f'src/textures/bubble-{color}{i}.png') for i in range(1, 5)]
    for color in bubble_color_names
]
bubble_textures = [[pygame.transform.scale(img, (40, 40)) for img in l] for l in bubble_textures]
bubble_textures.insert(0, None)


class Bubble(GameObj):

    BLUE = 1
    RED = 2
    GREEN = 3

    def __init__(self, color: int, pos: list, centered: bool = True):
        super().__init__()
        self.size = 40
        self.color = color
        self.update_texture()
        self.rect = self.texture.get_rect()
        if centered:
            self.rect.center = pos
        else:
            self.rect.topleft = pos
        self.pos = list(self.rect.topleft)
        self.falling = False

    def update_texture(self):
        all_sprites = bubble_textures[self.color]
        index = pygame.time.get_ticks() * len(all_sprites) // 1000 % len(all_sprites)
        self.texture = all_sprites[index]
