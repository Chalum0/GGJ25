import pygame

bubbles_textures = {
    1: pygame.transform.scale(pygame.image.load(f'./src/textures/bubble-blue.png'), (40, 40)),
    2: pygame.transform.scale(pygame.image.load(f'./src/textures/bubble-red.png'), (40, 40)),
    3: pygame.transform.scale(pygame.image.load(f'./src/textures/bubble-green.png'), (40, 40))
}
