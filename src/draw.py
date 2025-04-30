import pygame


def draw_vertical_gradient(main):
    top_color = (10, 125, 180)
    bottom_color = (0, 25, 60)
    delta_r = bottom_color[0] - top_color[0]
    delta_g = bottom_color[1] - top_color[1]
    delta_b = bottom_color[2] - top_color[2]
    for y in range(main.screen_size[1]):
        t = y / main.screen_size[1]
        r = int(top_color[0] + (delta_r * t))
        g = int(top_color[1] + (delta_g * t))
        b = int(top_color[2] + (delta_b * t))
        pygame.draw.line(main.screen, (r, g, b), (0, y), (main.screen_size[0], y))


def draw_centered_text(main, font, text, relative_y, color):
    surface = font.render(text, True, color)
    x = (main.screen_size[0] - surface.get_width()) // 2
    y = main.screen_size[1] * relative_y - surface.get_height() // 2
    main.screen.blit(surface, (x, y))
