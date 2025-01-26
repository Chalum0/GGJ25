from src.entities.gameobj import GameObj

class Player(GameObj):

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

        self.load_texture('./src/textures/crab-idle.png', (40, 20))

    def toggle_bubble_mod(self, mp):
        if not self.bubble_mod:
            self.before_bubble_offset_x = mp.current_offset_x
            self.before_bubble_offset_y = mp.current_offset_y
            self.before_bubble_pos = [self.pos[0], self.pos[1]]
            self.pos[1] -= 12
            match self.bubble_color:
                case 1:
                    self.load_texture('./src/textures/white_bubble_blue_idle1.png', (32, 32))
                case 2:
                    self.load_texture('./src/textures/white_bubble_red_idle1.png', (32, 32))
                case 3:
                    self.load_texture('./src/textures/white_bubble_green_idle1.png', (32, 32))
        else:
            mp.current_offset_x = self.before_bubble_offset_x
            mp.current_offset_y = self.before_bubble_offset_y
            self.pos[0] = self.before_bubble_pos[0]
            self.pos[1] = self.before_bubble_pos[1]
            self.rect.x = self.pos[0]
            self.rect.y = self.pos[1]
            self.load_texture('./src/textures/crab-idle.png', (40, 20))

        self.bubble_mod = not self.bubble_mod

    def change_buble_color(self, color):
        self.bubble_color = color
        if self.bubble_mod:
            match self.bubble_color:
                case 1:
                    self.load_texture('./src/textures/white_bubble_blue_idle1.png', (32, 32))
                case 2:
                    self.load_texture('./src/textures/white_bubble_red_idle1.png', (32, 32))
                case 3:
                    self.load_texture('./src/textures/white_bubble_green_idle1.png', (32, 32))
