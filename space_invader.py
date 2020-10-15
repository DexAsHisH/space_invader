import pygame
import random
import math
import time
from pygame import mixer


pygame.init()

clock = pygame.time.Clock()
FPS = 30
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)


#background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

#Game over text
game_over_font = pygame.font.Font('freesansbold.ttf',64)


def show_score(x, y):
    score = font.render("score: " +str(score_value), True, white)

    screen.blit(score, (x, y))

def Game_over_text():
    game_over = game_over_font.render("GAME OVER",True,white)
    screen.blit(game_over, (200,250))


#Title and icons
pygame.display.set_caption("Space invaders")
icon = pygame.image.load('ufo.png')
bg = pygame.image.load('bg.jpg')
pygame.display.set_icon(icon)

# Creating a spaceship
playerimg = pygame.image.load('spaceship.png')
spaceship_x = 370
spaceship_y = 480
spaceship_change_x = 0


def spaceship(x, y):
    screen.blit(playerimg, (x, y))


# Creating an Enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_change_x = []
enemy_change_y = []

number_of_enemies = 6

for i in range(number_of_enemies):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemy_change_x.append(5)
    enemy_change_y.append(40)

# Creating a bullet
bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_change_x = 0
bullet_change_y = 20
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))


def iscollision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x-bullet_x, 2) +
                         math.pow(enemy_y-bullet_y, 2))
    if distance < 27:
        return True
    else:
        return False


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


gameExit = True
while gameExit:

    screen.fill(black)
    screen.blit(bg, [0, 0])

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = False
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                spaceship_change_x = -10

            if event.key == pygame.K_RIGHT:
                spaceship_change_x = 10

            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bullet_x = spaceship_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                spaceship_change_x = 0

    spaceship_x += spaceship_change_x

    if spaceship_x <= 0:
        spaceship_x = 0

    elif spaceship_x >= 736:
        spaceship_x = 736

    #enemy movement
    
    for i in range(number_of_enemies):

        #Game over
        if enemy_y[i] > 440:
            for j in range(number_of_enemies):
                    enemy_y[j] = 2000
            Game_over_text()
            break


        enemy_x[i] += enemy_change_x[i]
        if enemy_x[i] <= 0:
            enemy_change_x[i] = 5
            enemy_y[i] += enemy_change_y[i]

        elif enemy_x[i] >= 736:
            enemy_change_x[i] = -5
            enemy_y[i] += enemy_change_y[i]


        #Collision

        collision = iscollision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i], i)

    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_change_y

    spaceship(spaceship_x, spaceship_y)

    show_score(textX, textY)
    pygame.display.update()
