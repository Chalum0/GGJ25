#!/usr/bin/env python3

import pygame
import pickle


class Editor:

    PLAYER_TILE_INDEX = 0
    WALL_TILE_INDEX = 1
    PLANT_TILE_INDEX = 8
    CONVERTED_PLANT_TILE_INDEX = 23

    def __init__(self, filename):
        self.filename = filename

        pygame.init()
        pygame.display.set_caption("Bubble Passage Editor")
        self.screen = pygame.display.set_mode((1080, 720), flags=pygame.RESIZABLE)
        pygame.display.set_icon(pygame.image.load('src/textures/crab.png'))
        self.clock = pygame.time.Clock()
        self.max_fps = 60

        self.tile_width = 40
        self.tile_height = 40
        self.grid_width = self.screen.get_width() // self.tile_width
        self.grid_height = self.screen.get_height() // self.tile_height
        self.scroll_x = 0
        self.scroll_y = 0

        self.tiles = [[-1] * self.grid_width for _ in range(self.grid_height)]
        self.tiles[3][1] = 0
        self.current_tile = Editor.WALL_TILE_INDEX
        self.selection = None

        self.textures = None
        self.wall_textures = None
        self.load_textures()

        self.load()

        self.loop()


    def load_textures(self):
        filenames = ['crab', 'wall', 'urchin1', 'urchin2', 'bubble-red1', 'bubble-green1', 'bubble-blue1', 'crabette1',
            'plant1', 'plant2', 'plant3', 'plant4', 'bigplant1', 'bigplant2']
        self.textures = [None] * len(filenames)
        for index, name in enumerate(filenames):
            texture = pygame.image.load(f'src/textures/{name}.png').convert_alpha()
            texture_height = self.tile_height // 2 if name == 'crab' else self.tile_height
            texture = pygame.transform.scale(texture, (self.tile_width, texture_height))
            self.textures[index] = texture
        directions = ['top', 'bottom', 'left', 'right']
        self.wall_textures = [None] * (2 ** len(directions))
        for index in range(2 ** len(directions)):
            texture_dir = ''
            for dir_index, direction in enumerate(directions):
                if index & 1 << dir_index != 0:
                    texture_dir += direction
            filename = 'wall' if texture_dir == '' else f'wall-{texture_dir}'
            filename = f'src/textures/{filename}.png'
            texture = pygame.image.load(filename).convert_alpha()
            texture = pygame.transform.scale(texture, (self.tile_width, self.tile_height))
            self.wall_textures[index] = texture


    def loop(self):
        self.playing = True
        while self.playing:
            self.render()
            pygame.display.flip()

            self.check_events()

            self.clock.tick(self.max_fps)


    def get_wall_index(self, x, y):
        index = 0
        for dir_index, (dx, dy) in enumerate(((0, -1), (0, 1), (-1, 0), (1, 0))):
            x2, y2 = x + dx, y + dy
            if 0 <= x2 < self.grid_width and 0 <= y2 < self.grid_height \
                    and self.tiles[y2][x2] != Editor.WALL_TILE_INDEX:
                index |= 1 << dir_index
        return index

    def pixel_pos_to_tile_pos(self, x, y):
        return ((x + self.scroll_x) // self.tile_width, (y + self.scroll_y) // self.tile_height)
    def tile_pos_to_pixel_pos(self, x, y):
        return (x * self.tile_width - self.scroll_x, y * self.tile_height - self.scroll_y)

    def texture_pos_px(self, x, y, texture):
        tile_x = self.tile_width * x + (self.tile_width - texture.get_width()) // 2 - self.scroll_x
        tile_y = self.tile_height * y + (self.tile_height - texture.get_height()) // 2 - self.scroll_y
        return tile_x, tile_y


    def render(self):
        screen = self.screen
        screen.fill((64, 64, 64))
        end_x = self.grid_width * self.tile_width - self.scroll_x
        end_y = self.grid_height * self.tile_height - self.scroll_y
        pygame.draw.rect(screen, (0, 0, 128), (0, 0, end_x, end_y))

        for y in range(self.grid_height):
            for x in range(self.grid_width):
                tile = self.tiles[y][x]
                texture = self.textures[tile]
                if tile >= 0:
                    if tile == Editor.WALL_TILE_INDEX:
                        texture = self.wall_textures[self.get_wall_index(x, y)]
                    tile_x, tile_y = self.texture_pos_px(x, y, texture)
                    screen.blit(texture, (tile_x, tile_y))

        if self.selection != None:
            x1, y1 = self.tile_pos_to_pixel_pos(
                min(self.selection[0], self.selection[2]),
                min(self.selection[1], self.selection[3]))
            x2, y2 = self.tile_pos_to_pixel_pos(
                max(self.selection[0], self.selection[2]) + 1,
                max(self.selection[1], self.selection[3]) + 1)
            width, height = x2 - x1, y2 - y1
            pygame.draw.rect(screen, (0, 0, 0), (x1, y1, width, height), 3)
        elif isinstance(self.current_tile, int):
            current_texture = self.textures[self.current_tile].copy()
            current_texture.set_alpha(160)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            tile_x, tile_y = self.texture_pos_px(
                (mouse_x + self.scroll_x) // self.tile_width, (mouse_y + self.scroll_y) // self.tile_height,
                current_texture)
            screen.blit(current_texture, (tile_x, tile_y))


    def check_scroll(self, event):
        if event.type == pygame.KEYDOWN:
            if event.scancode == 26: # Z
                if event.mod & pygame.KMOD_SHIFT != 0 and self.grid_height > 1:
                    self.grid_height -= 1
                    self.tiles.pop()
                else:
                    self.scroll_y = max(0, self.scroll_y - self.tile_height)
            elif event.scancode == 4: # Q
                if event.mod & pygame.KMOD_SHIFT != 0 and self.grid_width > 1:
                    self.grid_width -= 1
                    for line in self.tiles:
                        line.pop()
                else:
                    self.scroll_x = max(0, self.scroll_x - self.tile_width)
            elif event.scancode == 22: # S
                if event.mod & pygame.KMOD_SHIFT != 0:
                    self.grid_height += 1
                    self.tiles.append([-1] * self.grid_width)
                else:
                    self.scroll_y += self.tile_height
            elif event.scancode == 7: # D
                if event.mod & pygame.KMOD_SHIFT != 0:
                    self.grid_width += 1
                    for line in self.tiles:
                        line.append(-1)
                else:
                    self.scroll_x += self.tile_width

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            elif event.type == pygame.MOUSEWHEEL:
                if isinstance(self.current_tile, int):
                    self.current_tile = (self.current_tile - event.y) % len(self.textures)
                else:
                    self.current_tile = Editor.WALL_TILE_INDEX
            elif event.type == pygame.MOUSEMOTION:
                if self.selection != None:
                    self.selection[2], self.selection[3] = self.pixel_pos_to_tile_pos(*event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and event.mod & pygame.KMOD_CTRL != 0:
                    self.save()
                elif event.key == pygame.K_o and event.mod & pygame.KMOD_CTRL != 0:
                    self.load()
                elif event.key == pygame.K_SPACE:
                    if self.selection == None:
                        selection_x, selection_y = self.pixel_pos_to_tile_pos(*pygame.mouse.get_pos())
                        self.selection = [selection_x, selection_y, selection_x, selection_y]
                    else:
                        x1 = min(self.selection[0], self.selection[2])
                        y1 = min(self.selection[1], self.selection[3])
                        x2 = max(self.selection[0], self.selection[2]) + 1
                        y2 = max(self.selection[1], self.selection[3]) + 1
                        self.current_tile = []
                        for y in range(y1, y2):
                            self.current_tile.append(self.tiles[y][x1:x2])
                        self.selection = None
            self.check_scroll(event)

        mouse_buttons = pygame.mouse.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        tile_x = (mouse_x + self.scroll_x) // self.tile_width
        tile_y = (mouse_y + self.scroll_y) // self.tile_height
        if 0 <= tile_x < self.grid_width and 0 <= tile_y < self.grid_height:
            if mouse_buttons[1]: # Middle button
                if self.tiles[tile_y][tile_x] >= 0:
                    self.current_tile = self.tiles[tile_y][tile_x]
            elif mouse_buttons[2]: # Right button
                self.tiles[tile_y][tile_x] = -1
            elif mouse_buttons[0]: # Left button
                if isinstance(self.current_tile, list):
                    y = 0
                    while y < len(self.current_tile) and tile_y + y < self.grid_height:
                        x = 0
                        while x < len(self.current_tile[y]) and tile_x + x < self.grid_width:
                            self.tiles[tile_y + y][tile_x + x] = self.current_tile[y][x]
                            x += 1
                        y += 1
                            
                else:
                    if self.current_tile == Editor.PLAYER_TILE_INDEX:
                        self.remove_player()
                    self.tiles[tile_y][tile_x] = self.current_tile

    def remove_player(self):
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.tiles[y][x] == Editor.PLAYER_TILE_INDEX:
                    self.tiles[y][x] = -1


    def save(self):
        with open(self.filename, "wb") as file:
            tiles = [[-1] * self.grid_width for _ in range(self.grid_height)]
            for y in range(self.grid_height):
                for x in range(self.grid_width):
                    tile = self.tiles[y][x]
                    if tile == Editor.WALL_TILE_INDEX:
                        tile = Editor.PLANT_TILE_INDEX - 1 + self.get_wall_index(x, y)
                        if tile == Editor.PLANT_TILE_INDEX - 1:
                            tile = Editor.WALL_TILE_INDEX
                    elif tile >= Editor.PLANT_TILE_INDEX:
                        tile += Editor.CONVERTED_PLANT_TILE_INDEX - Editor.PLANT_TILE_INDEX
                    tile += 1
                    tiles[y][x] = tile
            pickle.dump(tiles, file)

    def load(self):
        try:
            with open(self.filename, "rb") as file:
                self.tiles = pickle.load(file)
                self.grid_width = len(self.tiles[0])
                self.grid_height = len(self.tiles)
                for y in range(self.grid_height):
                    for x in range(self.grid_width):
                        tile = self.tiles[y][x] - 1
                        if tile >= Editor.CONVERTED_PLANT_TILE_INDEX:
                            self.tiles[y][x] = tile - Editor.CONVERTED_PLANT_TILE_INDEX + Editor.PLANT_TILE_INDEX
                        elif tile >= Editor.PLANT_TILE_INDEX:
                            self.tiles[y][x] = Editor.WALL_TILE_INDEX
                        else:
                            self.tiles[y][x] = tile
        except:
            pass


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: ./editor.py <filename>")
    else:
        print("Use Ctrl-S to save.")
        Editor(sys.argv[1])
