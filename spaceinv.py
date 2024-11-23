import pygame
import sys
import math
from random import randint
from pygame import mixer

from pygame.constants import K_LEFT, KEYDOWN
pygame.init()

screen = pygame.display.set_mode((800,600))



font = pygame.font.Font("font/GameOfSquids.ttf" , 25)
fontX = 10
fontY = 10
git 
bullet_state = None


def showHiScore():  
      fileo = open("highscore.txt" )
      hiscore_value = fileo.readline()
      hiscore = font.render("High-Score : " + str(hiscore_value) , True , (255,255,255))
      screen.blit(hiscore , (500,10))
 
def showScore(x,y,score_value):
     score = font.render("Score : " + str(score_value), True , (255,255,255))
     screen.blit(score , (x,y))
 
 
def isCollision(enemyX , enemyY , bulletX , bulletY):
     dist = math.sqrt(math.pow((enemyX - bulletX),2) + math.pow((bulletY - enemyY),2))
     if dist<35:
         return True
     else:
         return False
 
def player(x,y,playerImg):
     screen.blit(playerImg , (x, y))
 
def bullet():
      global bullet_state
      bullet_state = "fire"
     #  screen.blit(bulletImg , (x, y))
  
def enemy(x,y,enemyImg):
     screen.blit(enemyImg , (x, y))
 



pygame.display.set_caption("Space Shooter Game")
    
icon = pygame.image.load("images/logo.jpg")

pygame.display.set_icon(icon)