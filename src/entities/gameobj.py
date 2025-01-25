class GameObj:

    def __init__(self):
        self.pos = [0, 0]

        self.max_x_momentum = 6
        self.max_y_momentum = 15
        self.x_acceleration = .5
        self.y_acceleration = .3
        self.x_momentum = 0
        self.y_momentum = 0

        self.rect = None

        self.load_texture()

    def load_texture(self):
        self.texture = None
