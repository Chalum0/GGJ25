from src.screens.mainmenu import MainMenu
import pygame


class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Bubble Passage")
        self.screen_size = (1080, 720)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_icon(pygame.image.load('src/textures/crab.png'))

        self.clock = pygame.time.Clock()
        self.max_fps = 120

        pygame.mixer.music.load('src/audio/menu_music.ogg')
        pygame.mixer.music.play(-1)

        self.quit = False
        MainMenu(self).loop()


if __name__ == "__main__":
    Main()
