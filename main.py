import pygame
import random
import sys
import os


images_skier = ["data/skier_down.png", "data/skier_right.png", "data/skier_left.png"]


class Skier(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.player = pygame.image.load("data/skier_down.png")
        self.rect = self.player.get_rect()
        self.rect.center = [300, 200]
        self.corner = 0

    def moving(self, speed):
        self.rect.centerx = self.rect.centerx + speed[0]
        if self.rect.centerx < 20:
            self.rect.centerx = 20
        if self.rect.centerx > 620:
            self.rect.centerx = 620

    def turn(self, direction):
        self.corner = self.corner + direction
        if self.corner < -1:
            self.corner = -1
        if self.corner > 1:
            self.corner = 1
        center = self.rect.center
        self.player = pygame.image.load(images_skier[self.corner])
        self.rect = self.player.get_rect()
        self.rect.center = center
        speed_skier = [self.corner, 6 - abs(self.corner) * 2]
        return speed_skier


pygame.init()
size = width, height = 1600, 900
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
pygame.display.set_caption("Горнолыжник")
pygame.display.flip()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        sys.exit()
    uploaded_image = pygame.image.load(fullname)
    if colorkey is not None:
        uploaded_image = uploaded_image.convert()
        if colorkey == -1:
            colorkey = uploaded_image.get_at((0, 0))
        uploaded_image.set_colorkey(colorkey)
    else:
        uploaded_image = uploaded_image.convert_alpha()
    return uploaded_image


image = load_image("skier_down.png")
all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = load_image("skier_down.png")
sprite.rect = sprite.image.get_rect()
all_sprites.add(sprite)
sprite.rect.x, sprite.rect.y = 600, 30

speed = [0, 6]
skier = Skier()
clock = pygame.time.Clock()
run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.K_LEFT:
                speed = skier.turn(-1)
            elif event.type == pygame.K_RIGHT:
                speed = skier.turn(1)
    all_sprites.draw(screen)
    skier.moving(speed)
    pygame.display.update()
pygame.quit()
