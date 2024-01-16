import pygame


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1600, 900
    screen = pygame.display.set_mode(size)

    while pygame.event.wait().type != pygame.QUIT:
        pass
