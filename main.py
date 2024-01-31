import os
import sys

import pygame
import random

skier_images = ["data/skier_down.png", "data/skier_right.png", "data/skier_right1.png",
                "data/skier_left1.png", "data/skier_left.png"]

boost = 1


class SkierClass(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("data/skier_down.png")
        self.rect = self.image.get_rect()
        self.rect.center = [800, 100]
        self.angle = 0

    def turn(self, direction):
        self.angle = self.angle + direction
        if self.angle < -2:
            self.angle = -2
        if self.angle > 2:
            self.angle = 2
        center = self.rect.center
        self.image = pygame.image.load(skier_images[self.angle])
        self.rect = self.image.get_rect()
        self.rect.center = center
        speed = [self.angle, 6 + boost - abs(self.angle) * 2]
        return speed

    def move(self, speed):
        self.rect.centerx = self.rect.centerx + speed[0]
        if self.rect.centerx < 50:
            self.rect.centerx = 50
        if self.rect.centerx > 1550:
            self.rect.centerx = 1550


class ObstacleClass(pygame.sprite.Sprite):
    def __init__(self, image_file, location, type):
        pygame.sprite.Sprite.__init__(self)
        self.image_file = image_file
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.type = type
        self.passed = False

    def update(self):
        global speed
        self.rect.centery -= speed[1]
        if self.rect.centery < -32:
            self.kill()


def create_map():
    global obstacles
    locations = []
    for i in range(11):
        row = random.randint(0, 10)
        col = random.randint(0, 10)
        location = [col * 150 + 60, row * 150 + 60 + 1700]
        if not (location in locations):
            locations.append(location)
            type = random.choice(["tree", "flag"])
            if type == "tree":
                img = "data/tree.png"
            elif type == "flag":
                img = "data/flag.png"
            obstacle = ObstacleClass(img, location, type)
            obstacles.add(obstacle)


def animate():
    screen.fill([255, 255, 255])
    obstacles.draw(screen)
    screen.blit(skier.image, skier.rect)
    screen.blit(score_text, [10, 10])
    pygame.display.flip()


pygame.init()
screen = pygame.display.set_mode([1600, 900])
clock = pygame.time.Clock()
speed = [0, 7]
obstacles = pygame.sprite.Group()
skier = SkierClass()
map_position = 0
points = 0
create_map()
font = pygame.font.Font(None, 50)

FPS = 50


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.png'), (1600, 900))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                run = False
        pygame.display.flip()
        clock.tick(FPS)


start_screen()

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                speed = skier.turn(-1)
            elif event.key == pygame.K_RIGHT:
                speed = skier.turn(1)
    skier.move(speed)
    map_position += speed[1]

    if map_position >= 1600:
        create_map()
        map_position = 1

    hit = pygame.sprite.spritecollide(skier, obstacles, False)
    if hit:
        if hit[0].type == "tree" and not hit[0].passed:
            points = points - 30
            skier.image = pygame.image.load("data/skier_crash.png")
            animate()
            pygame.time.delay(1000)
            skier.image = pygame.image.load("data/skier_down.png")
            skier.angle = 0
            hit[0].passed = True
        elif hit[0].type == "flag" and not hit[0].passed:
            points += 10
            speed[1] += boost
            hit[0].kill()

    obstacles.update()
    score_text = font.render("Score: " + str(points), 1, (0, 0, 0))
    animate()

pygame.quit()
