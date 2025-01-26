from src.screens.game import Game
from src.screens.credits import Credits
import pygame
import json


class MainMenu:
    def __init__(self, main):
        self.main = main

        self.title_font = pygame.font.SysFont("Liberation Sans", 60, bold=True)
        self.button_font = pygame.font.SysFont("Liberation Sans", 40)

        self.crab = pygame.image.load('src/textures/crab.png')
        self.crab = pygame.transform.scale_by(self.crab, 2)
        self.bubbles = [
            [pygame.image.load(f'src/textures/bubble-{name}{i}.png') for i in range(1, 5)]
            for name in ('red', 'green')
        ]
        self.bubbles = [[pygame.transform.scale(img, (50, 50)) for img in l] for l in self.bubbles]

        self.buttons = [(.35, "Play"), (.51, "Resume"), (.67, "Credits"), (.83, "Quit")]
        self.button_height = self.main.screen_size[1] * .15
        self.cursor = 0

        self.game_ambiance = pygame.mixer.Sound('src/audio/game_ambiance.ogg')
        pygame.mixer.music.load('src/audio/menu_music.ogg')
        pygame.mixer.music.play(-1)

        self.can_resume = False
        try:
            json.load(open('src/settings/save.json', 'r'))
            self.can_resume = True
        except:
            pass


    def loop(self):
        while not self.main.quit:
            self.render()
            pygame.display.flip()

            self.check_events()

            self.main.clock.tick(self.main.max_fps)


    def draw_centered_text(self, font, text, relative_y, color):
        surface = font.render(text, True, color)
        x = (self.main.screen_size[0] - surface.get_width()) // 2
        y = self.main.screen_size[1] * relative_y - surface.get_height() // 2
        self.main.screen.blit(surface, (x, y))

    def render(self):
        screen = self.main.screen
        screen.fill((0, 0, 255))

        for bubble_imgs, bubble_x in zip(self.bubbles, (.15, .85)):
            img_index = pygame.time.get_ticks() // (1000 // len(bubble_imgs)) % len(bubble_imgs)
            bubble_x = self.main.screen_size[0] * bubble_x - bubble_imgs[img_index].get_width() / 2
            bubble_y = self.main.screen_size[1] * .15 - bubble_imgs[img_index].get_height() / 2
            screen.blit(bubble_imgs[img_index], (bubble_x, bubble_y))
        self.draw_centered_text(self.title_font, "Bubble Passage", .15, (255, 255, 255))

        for index, (button_y, label) in enumerate(self.buttons):
            if index == self.cursor:
                y = self.main.screen_size[1] * button_y
                rect = (0, y - self.button_height / 2, self.main.screen_size[0], self.button_height)
                pygame.draw.rect(screen, (0, 128, 0), rect)
                crab_x = self.main.screen_size[0] * .25 - self.crab.get_width() / 2
                crab_y = y - self.crab.get_height() / 2
                screen.blit(self.crab, (crab_x, crab_y))
                crab_x = self.main.screen_size[0] * .75 - self.crab.get_width() / 2
                screen.blit(self.crab, (crab_x, crab_y))
            color = (192, 192, 192) if index == 1 and not self.can_resume else (255, 255, 255)
            self.draw_centered_text(self.button_font, label, button_y, color)


    def launch_game(self, level_num):
        pygame.mixer.music.load('src/audio/game_music.ogg')
        pygame.mixer.music.play(-1)
        self.game_ambiance.play(-1)
        Game(self.main, level_num).loop()
        self.game_ambiance.stop()
        pygame.mixer.music.load('src/audio/menu_music.ogg')
        pygame.mixer.music.play(-1)

    def press_button(self):
        match self.cursor:
            case 0:
                self.launch_game(1)
                self.can_resume = True
            case 1:
                try:
                    level_num = json.load(open('src/settings/save.json', 'r'))
                    self.launch_game(level_num)
                except:
                    pass
            case 2:
                Credits(self.main).loop()
            case 3:
                self.main.quit = True

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.cursor = (self.cursor - 1) % len(self.buttons)
                elif event.key == pygame.K_DOWN:
                    self.cursor = (self.cursor + 1) % len(self.buttons)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self.press_button()
            elif event.type == pygame.MOUSEMOTION:
                self.cursor = -1
                for index, (button_y, _) in enumerate(self.buttons):
                    _, mouse_y = event.pos
                    button_y *= self.main.screen_size[1]
                    if button_y - self.button_height / 2 <= mouse_y < button_y + self.button_height / 2:
                        self.cursor = index
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.press_button()
