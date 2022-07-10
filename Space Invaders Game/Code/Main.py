#Note - Use alt+ctrl+l to format the program automatically
# import the pygame module
import pygame
import random
import math
from pygame import mixer #Mixer for sound effects
# You will need to initialize the pygame module so that it works
pygame.init()
# Create the screen
screen = pygame.display.set_mode((800,600))
#Set background
#bg = pygame.image.load("space.jpg")
bg = pygame.image.load("milky-way-1.jpg")

#background Sound
#mixer.music.load("background.wav")
#mixer.music.play(-1)

# Set Title of Window
pygame.display.set_caption("Space Invadors")
# Set Icon
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

#Player
playerimg = pygame.image.load("002-space-invaders.png")
playerX = 370
playerY = 480
playerX_change = 0

#Enemy
enemyimg=[]
enemyx=[]
enemyy=[]
enemyx_change=[]
enemyy_change=[]
no_of_enemies=7
for i in range(no_of_enemies):
    enemyimg.append(pygame.image.load("004-target.png"))
    enemyx.append(random.randint(0,735))
    enemyy.append(random.randint(50,150))
    enemyx_change.append(0.7)
    enemyy_change.append(40)

#Bullet
bulletimg = pygame.image.load("001-bullet.png")
bulletx=0
bullety=480
bulletx_change=0
bullety_change=2
# Ready - you can't see the bullet on the screen
# Fire - The bullet is currently moving
bullet_state="ready"

#score
score_value=0
font=pygame.font.Font('freesansbold.ttf',32)
textx=10
texty=10
#Game over font
over_font = pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    score=font.render("Score : "+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text=over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))

#Draw our player on screen
def player(x,y):
    screen.blit(playerimg,(x,y))

#Draw enemy on the screen
def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletimg,(x+16,y+10))

def isCollision(en_x,en_y,bul_x,bul_y):
    #Calculate the distance between enemy and the bullet
    distance=math.sqrt((math.pow(en_x-bul_x,2))+(math.pow(en_y-bul_y,2)))
    if distance<27:
        return True
    else:
        return False

# Loop is only to retain the game window until the window closing event
running = True
while running:
    # Set the bg Color
    screen.fill((0, 0, 0))
    # Set bg image
    screen.blit(bg,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #Check if the keystroke is pressed or not and weather it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change=-0.9
            if event.key == pygame.K_RIGHT:
                playerX_change=0.9
            if event.key == pygame.K_SPACE:
                if bullet_state=="ready":
                    bullet_sound=mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletx=playerX
                    fire_bullet(bulletx,bullety)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX+=playerX_change
    #Set boundaries for spaceship
    if playerX<=0:
        playerX=0
    #800-64 = 736 because the width is 800 and the img size is 64px
    elif playerX >= 736:
        playerX=736
    #enemy movement
    for i in range(no_of_enemies):
        #Game Over
        if enemyy[i]>440:
            for j in range(no_of_enemies):
                enemyy[j]=2000
            game_over_text()
            break
        enemyx[i]+=enemyx_change[i]
        if enemyx[i]<=0:
            #enemyx_change=0.3
            enemyx_change[i] = 0.7
            enemyy[i]+=enemyy_change[i]
        elif enemyx[i]>=736:
            #enemyx_change=-0.3
            enemyx_change[i] = -0.7
            enemyy[i]+=enemyy_change[i]

        # Collision
        collision = isCollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bullety = 480
            bullet_state = "ready"
            score_value += 1
            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(50, 150)

        enemy(enemyx[i], enemyy[i],i)

    #Bullet Movement
    if bullety<=0:
        bullety=480
        bullet_state="ready"

    if bullet_state=="fire":
        fire_bullet(bulletx,bullety)
        bullety-=bullety_change


    player(playerX,playerY)
    show_score(textx,texty)
    pygame.display.update()