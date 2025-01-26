from src.entities.gameobj import GameObj
import pygame

class Player(GameObj):

    DYING_TIME = 1.

    def __init__(self, pos):
        super().__init__()
        self.pos = list(pos)
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

        self.in_bubble = False
        self.bubble_pos = None
        self.before_bubble_offset_x = None
        self.before_bubble_offset_y = None
        self.bubble_element = None
        self.on_falling_bubble = False
        self.max_placed_bubbles = 3

        self.bubble_mod = False
        self.before_bubble_pos = None
        self.bubble_color = 1  # 1: blue, 2: red, 3: green

        self.death_time = None
        self.jumping = False

        crab_size = (40, 20)
        self.load_texture('./src/textures/crab-idle.png', crab_size)
        self.death_textures = [pygame.image.load(f'./src/textures/crab-dies{i}.png').convert_alpha() for i in range(1, 4)]
        self.death_textures = [pygame.transform.scale(img, crab_size) for img in self.death_textures]
        self.jump_textures = [
            pygame.image.load(f'./src/textures/crab-{action}.png').convert_alpha()
            for action in ('jumping', 'gliding', 'falling')
        ]
        self.jump_textures = [pygame.transform.scale(img, crab_size) for img in self.jump_textures]

    def toggle_bubble_mod(self, mp):
        if not self.bubble_mod:
            self.before_bubble_offset_x = mp.current_offset_x
            self.before_bubble_offset_y = mp.current_offset_y
            self.before_bubble_pos = [self.pos[0], self.pos[1]]
            self.pos[1] -= 12
            self.change_bubble_color(self.bubble_color)
        else:
            mp.current_offset_x = self.before_bubble_offset_x
            mp.current_offset_y = self.before_bubble_offset_y
            self.pos[0] = self.before_bubble_pos[0]
            self.pos[1] = self.before_bubble_pos[1]
            self.rect.x = self.pos[0]
            self.rect.y = self.pos[1]
            self.load_texture('./src/textures/crab-idle.png', (40, 20))

        self.bubble_mod = not self.bubble_mod

    def change_bubble_color(self, color):
        self.bubble_color = color
        if self.bubble_mod:
            match self.bubble_color:
                case 1:
                    self.load_texture('./src/textures/bubble-white-blue.png', (32, 32))
                case 2:
                    self.load_texture('./src/textures/bubble-white-red.png', (32, 32))
                case 3:
                    self.load_texture('./src/textures/bubble-white-green.png', (32, 32))

    def draw(self, screen):
        texture = self.texture
        if not self.bubble_mod:
            if self.death_time != None:
                texture = self.death_textures[int(self.death_time / (self.DYING_TIME / len(self.death_textures)))]
            elif self.jumping:
                if self.y_momentum < -2:
                    texture = self.jump_textures[0]
                elif self.y_momentum > 2:
                    texture = self.jump_textures[2]
                else:
                    texture = self.jump_textures[1]
        screen.blit(texture, self.rect)
