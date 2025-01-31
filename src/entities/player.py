from src.entities.gameobj import GameObj
import pygame

class Player(GameObj):

    DYING_TIME = 1.

    def __init__(self, pos):
        super().__init__()
        self.pos = list(pos)
        self.texture = None

        self.jump_power = -7.5

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

        self.in_bubble = False
        self.bubble_pos = None
        self.before_bubble_offset_x = None
        self.before_bubble_offset_y = None
        self.bubble_element = None
        self.on_falling_bubble = False
        self.max_placed_bubbles = 3

        self.bubble_mode = False
        self.before_bubble_pos = None
        self.bubble_color = 1  # 1: blue, 2: red, 3: green

        self.death_time = None
        self.jumping = False

        self.crab_size = (40, 20)
        self.load_texture('./src/textures/crab.png', self.crab_size)
        self.walk_textures = [pygame.image.load(f'./src/textures/crab-walk{i}.png').convert_alpha() for i in range(1, 4)]
        self.walk_textures = [pygame.transform.scale(img, self.crab_size) for img in self.walk_textures]
        self.jump_textures = [
            pygame.image.load(f'./src/textures/crab-{action}.png').convert_alpha()
            for action in ('jumping', 'gliding', 'falling')
        ]
        self.jump_textures = [pygame.transform.scale(img, self.crab_size) for img in self.jump_textures]
        self.death_textures = [pygame.image.load(f'./src/textures/crab-dies{i}.png').convert_alpha() for i in range(1, 4)]
        self.death_textures = [pygame.transform.scale(img, self.crab_size) for img in self.death_textures]

        self.bubble_size = (32, 32)
        self.bubble_textures = [
            [pygame.image.load(f'./src/textures/bubble-white-{color}{i}.png').convert_alpha() for i in range(1, 5)]
            for color in ['blue', 'red', 'green']
        ]
        self.bubble_textures = [[pygame.transform.scale(img, self.bubble_size) for img in l] for l in self.bubble_textures]

    def toggle_bubble_mode(self, mp):
        if not self.bubble_mode:
            self.before_bubble_offset_x = mp.scroll_x
            self.before_bubble_offset_y = mp.scroll_y
            self.before_bubble_pos = [self.pos[0], self.pos[1]]
            self.pos[1] -= self.bubble_size[1] - self.crab_size[1]
            self.load_texture('./src/textures/bubble-white1.png', (32, 32))
        else:
            mp.scroll_x = self.before_bubble_offset_x
            mp.scroll_y = self.before_bubble_offset_y
            self.pos[0] = self.before_bubble_pos[0]
            self.pos[1] = self.before_bubble_pos[1]
            self.rect.x = self.pos[0]
            self.rect.y = self.pos[1]
            self.load_texture('./src/textures/crab.png', self.crab_size)

        self.bubble_mode = not self.bubble_mode

    def change_bubble_color(self, color):
        self.bubble_color = color

    def draw(self, screen, map):
        texture = self.texture
        if not self.bubble_mode:
            if self.death_time != None:
                texture = self.death_textures[int(self.death_time / (self.DYING_TIME / len(self.death_textures)))]
            elif self.jumping:
                if self.y_momentum < -2:
                    texture = self.jump_textures[0]
                elif self.y_momentum > 2:
                    texture = self.jump_textures[2]
                else:
                    texture = self.jump_textures[1]
            elif self.x_momentum != 0:
                img_index = pygame.time.get_ticks() * len(self.walk_textures) // 1000 % len(self.walk_textures)
                texture = self.walk_textures[img_index]
        else:
            textures = self.bubble_textures[self.bubble_color - 1]
            img_index = pygame.time.get_ticks() * len(textures) // 1000 % len(textures)
            texture = textures[img_index]
        screen.blit(texture, (self.rect.left - map.scroll_x, self.rect.top - map.scroll_y, self.rect.width, self.rect.height))
