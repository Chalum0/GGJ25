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

        self.load_texture('./src/textures/crab.png', (40, 20))
