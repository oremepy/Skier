import pygame
import random
import sys
import os


pygame.init()
size = width, height = 1600, 900
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
pygame.display.set_caption("Горнолыжник")
pygame.display.flip()


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        sys.exit()
    image = pygame.image.load(fullname)
    return image


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
pygame.quit()
