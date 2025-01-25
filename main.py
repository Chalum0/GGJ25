#!/usr/bin/env python3

from src.screens.game import Game
import pygame


class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Bubble Passage")
        self.screen_size = (1080, 720)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        self.max_fps = 120

        self.quit = False
        Game(self).loop()


if __name__ == "__main__":
    Main()
