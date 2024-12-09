import pygame
import sys
import math
from random import randint
from pygame import mixer

from pygame.constants import K_LEFT

pygame.init()

my_screen = pygame.display.set_mode((800, 600))

font = pygame.font.Font("font/GameOfSquids.ttf", 24)
fontX = 10
fontY = 10

pygame.display.set_caption("Space Shooter Game")

icon = pygame.image.load("images/logo.jpg")

pygame.display.set_icon(icon)

bullet_state = None


def high_score_display():
    fileo = open("highscore.txt")
    hiscore_value = fileo.readline()
    hiscore = font.render("High-Score : " + str(hiscore_value), True, (255, 255, 255))
    my_screen.blit(hiscore, (500, 10))


def show_score(x, y, score_value):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    my_screen.blit(score, (x, y))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    dist = math.sqrt(math.pow((enemyX - bulletX), 2) + math.pow((bulletY - enemyY), 2))
    if dist < 35:
        return True
    else:
        return False


def player(x, y, playerImg):
    my_screen.blit(playerImg, (x, y))


def bullet():
    global bullet_state
    bullet_state = "fire"


def enemy(x, y, enemyImg):
    my_screen.blit(enemyImg, (x, y))


def main():
    global bullet_state

    mixer.music.load("music/background.wav")
    mixer.music.play(1000)

    over = False
    score_value = 0
    fileo = open("highscore.txt")
    hiscore_value = fileo.readline()

    backgroundImg = pygame.image.load("images/background.png")

    playerImg = pygame.image.load("images/player.png")
    playerX = 369
    playerY = 500
    playerXchange = 0

    k = 0
    j = 0

    bulletImg = pygame.image.load("images/bullet.png")
    bulletX = 0
    bulletY = 500
    bulletY_change = 10
    bullet_state = "ready"

    enemyImg = []
    enemyImg.append(pygame.image.load("enemy/1.png"))
    enemyImg.append(pygame.image.load("enemy/1.png"))
    enemyImg.append(pygame.image.load("enemy/3.png"))
    enemyImg.append(pygame.image.load("enemy/4.png"))
    enemyImg.append(pygame.image.load("enemy/2.png"))
    enemyImg.append(pygame.image.load("enemy/3.png"))
    enemyImg.append(pygame.image.load("enemy/2.png"))
    enemyImg.append(pygame.image.load("enemy/4.png"))

    enemyX = []
    enemyY = []
    enemyXchange = []
    enemyYchange = []
    enemies_count = 8
    for i in range(enemies_count):
        enemyX.append(randint(0, 720))
        enemyY.append(randint(10, 150))
        enemyXchange.append(2)
        enemyYchange.append(0)

    blast_img = pygame.image.load("images/blast.png")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerXchange = -4
                if event.key == pygame.K_RIGHT:
                    playerXchange = 4
                if event.key == pygame.K_SPACE:
                    if bullet_state is "ready":
                        bullet_sound = mixer.Sound("music/laser.wav")
                        bullet_sound.play()
                        bulletX = playerX - 5
                        bullet()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if (pos[0] > 330 and pos[0] < 422) and (pos[1] > 340 and pos[1] < 372):
                    return

            if event.type == pygame.KEYUP:
                if event.key == K_LEFT or event.key == pygame.K_RIGHT:
                    playerXchange = 0

        my_screen.blit(backgroundImg, (0, 0))

        if bullet_state is "fire":
            my_screen.blit(bulletImg, (bulletX, bulletY))
            bulletY -= bulletY_change
            if bulletY == 0:
                bullet_state = "ready"
                bulletY = 500
                i = 0

        if playerX < 0:
            playerX = 0
        elif playerX > 743:
            playerX = 743
        else:
            playerX += playerXchange
        player(playerX, playerY, playerImg)

        for i in range(enemies_count):
            if enemyY[i] > 450:
                for j in range(enemies_count):
                    enemyY[j] = 2000
                game_font = pygame.font.Font("font/GameOfSquids.ttf", 65)
                gameover = game_font.render("GAME OVER ", True, (255, 255, 255))
                my_screen.blit(gameover, (200, 250))
                mixer.music.stop()
                if not over:
                    game_over = mixer.Sound("music/gameover.mp3")
                    game_over.play()
                    over = True
                game_over = font.render("RESTART", True, (200, 200, 200))
                my_screen.blit(game_over, (330, 340))
                break

            if k == 0 and j == 0:
                enemyYchange[i] = .3
            if score_value > 50 and score_value <= 150 and k == 0:
                enemyYchange = [x + .1 for x in enemyYchange]
                k = 1

            if score_value > 150 and j == 0:
                enemyYchange = [c + .3 for c in enemyYchange]
                j = 1

            enemyY[i] += enemyYchange[i]
            enemy(enemyX[i], enemyY[i], enemyImg[i])

            collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                collision_sound = mixer.Sound("music/explosion.wav")
                collision_sound.play()
                my_screen.blit(blast_img, (enemyX[i], enemyY[i]))
                bullet_state = "ready"
                bulletY = 500
                score_value += 1
                if score_value > int(hiscore_value):
                    file = open("highscore.txt", "w")
                    file.write(str(score_value))
                    file.close()
                enemyX[i] = randint(0, 720)
                enemyY[i] = randint(10, 150)

        show_score(fontX, fontY, score_value)
        high_score_display()

        pygame.display.update()


while True:
    main()
