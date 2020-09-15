import random
import math
import pygame
from pygame import mixer


#Add Init when making pygame it Initializes Pygame
#Always add pygame.init() and pygame.display.update() - put update into running loop
pygame.init()

#Creates the Window ((Width X, Hight Y)) (0,0) = Top left
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("C:/Users/lajbr/Documents/Programming/python/Invader/background.jpg")

#BG Music
mixer.music.load("C:/Users/lajbr/Documents/Programming/python/Invader/Stekalive.mp3")
mixer.music.play(-1)

#title and icon "Icons are 32pixels x 32ixels"
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("C:/Users/lajbr/Documents/Programming/python/Invader/ufo.png")
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load('C:/Users/lajbr/Documents/Programming/python/Invader/ship.png')
playerX = 370
playerY = 480
playerX_change = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemys = 6

for i in range(num_enemys):
    enemyImg.append(pygame.image.load('C:/Users/lajbr/Documents/Programming/python/Invader/enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(.5)
    enemyY_change.append(40)

#Bullet

#ready - can't see the bullet on the screen
#fire - bullet is moving

bulletImg = pygame.image.load('C:/Users/lajbr/Documents/Programming/python/Invader/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font ('freesansbold.ttf',32)

textX = 10
textY = 10

# GAME OVER TEXT
over_font = pygame.font.Font ('freesansbold.ttf',64)

def show_score(x,y):
    score = font.render("Score :" + str(score_value), True, (0,0,0))
    screen.blit(score, (x,y))

def game_over_text():
    over_text = over_font.render(("GAME OVER"), True, (0,0,0))
    screen.blit(over_text, (200,250))


def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet (x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16,y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


#Game Loop, Window Doesn't hang, what happends within the window

running = True
while running:

    #RGB VALUE (RED GREEN BLUE)
    screen.fill((255, 255, 255))
    
    #background image draw
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        #if keystroke is pressed check wether it is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1 
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound ('C:/Users/lajbr/Documents/Programming/python/Invader/Laser_Shoot.wav')
                    bullet_sound.play()
                    #Gets current X coord of spaceship
                bulletX = playerX 
                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    #keep player after screen.fill to keep player/anything on top

    #Checking for bounderies of spaceship
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #Enemy Movement
    #Checking for bounderies of Enemy as well as movement
    
    for i in range(num_enemys):

        #GAME OVER
        if enemyY[i] > 440:
            for j in range(num_enemys):
                enemyY[j] = 2000
            game_over_text ()
            break
            

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = .5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -.5
            enemyY[i] += enemyY_change[i]
        
        #Collision
        collsion = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collsion:
            dead_sound = mixer.Sound ('C:/Users/lajbr/Documents/Programming/python/Invader/dead.wav')
            dead_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)
        
        enemy(enemyX[i],enemyY[i], i)

    #Bullet Movement
    if bulletY <= 0 :
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet (bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX,playerY)
    show_score (textX,textY)
    pygame.display.update()