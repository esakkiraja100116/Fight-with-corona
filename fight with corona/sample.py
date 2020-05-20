import pygame
import sys
import random
import math
from pygame import mixer
#initilazation of pygame
pygame.init()

width = 800
height = 600
bg= (0,0,0)

#background image 
background = pygame.image.load('backgroundimg1.png') 

#background sound
mixer.music.load('background.wav')
mixer.music.play(-1)


#settong of display
screen = pygame.display.set_mode((width,height))
caption = pygame.display.set_caption("FIGHT WITH CORONA")
icon = pygame.image.load('add (3).png')
pygame.display.set_icon(icon)

#player image
player_image = pygame.image.load('gaming3.png')
playerX = 400
playerY = 480
playerX_change = 0

#enemy
enemy_image = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 6

#score 
score_value = 0


for i in range (num_of_enemies):
	enemy_image.append(pygame.image.load('icon1.png'))
	enemyX.append(random.randint(0,750))
	enemyY.append(random.randint(50,150))
	enemyX_change.append(4 )
	enemyY_change.append(40)

#bullot
bullot_img = pygame.image.load('bullet2.png')
bullotX = 0
bullotY = 480
bullotX_change = 0 
bullotY_change = 10
bullot_state = "ready"

score_value = 0
font = pygame.font.Font('Tale of Hawks.ttf',32)

textX = 10
textY = 10

#game over text
over_font = pygame.font.Font('Avocado Creamy.ttf',100)

def show_score(x,y):
	score = font.render("score :" + str(score_value),True , (255,255,255))
	screen.blit(score , (x,y))

def game_over_text():
	over_text = over_font.render("GAME OVER",True , (255,255,255))
	screen.blit(over_text , (200,250))

def player():
	screen.blit(player_image,(playerX,playerY))

def enemy(x,y,i):
	screen.blit(enemy_image[i],(x,y))

def fire_bullot(x,y):
	global bullot_state
	bullot_state = "fire"
	screen.blit(bullot_img,(x + 45,y + 14))

def iscollition(enemyX,enemyY,bullotX,bullotY):
	distance = math.sqrt(math.pow(enemyX-bullotX,2)) + (math.pow(enemyY-bullotY,2))
	
	if distance<40:
		return True
	else:
		return False

#game loop
while True:

	#rgb
	screen.fill(bg)
	#bg clr
	screen.blit(background,(0,0))
	
	for event in pygame.event.get():     
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit("END")

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				playerX_change = 7
			if event.key == pygame.K_LEFT:
				playerX_change = -7

			if event.key == pygame.K_UP:
				if bullot_state is "ready":
					bullot_sound = mixer.Sound('laser.wav')
					bullot_sound.play()

				bullotX = playerX
				fire_bullot(bullotX,bullotY)


		if event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
				playerX_change = 0			
			 
	#boundry of the player image
	playerX +=playerX_change

	if playerX <= 0:
		playerX = 0
	elif playerX >= 710:
		playerX = 710
	#enemy
	for i in range(num_of_enemies):

		#game over
		if enemyY[i] > 440:
			for j in range(num_of_enemies):
				enemyY[j] = 2000
			game_over_text ()

		enemyX[i] += enemyX_change[i]
		if enemyX[i] <=0:
			enemyX_change[i] = 4
			enemyY[i] += enemyY_change[i]
		elif enemyX[i] >= 710:
			enemyX_change[i] = -4
			enemyY[i] += enemyY_change[i]
	
	    #collison
		collison = iscollition(enemyX[i],enemyY[i],bullotX,bullotY)
		
		if collison:
			exploation_sound = mixer.Sound('exploation.wav')
			exploation_sound.play()

			bullotY = 480
			bullot_state ="ready"

			score_value += 1
			enemyX[i] = random.randint(0,400)
			enemyY[i] = random.randint(50,180)

		enemy(enemyX[i],enemyY[i],i)	

	
	#bullot move
	if bullotY <= 0:
		bullotY = 480
		bullot_state = "ready"

	if bullot_state is "fire":
		fire_bullot(bullotX,bullotY)
		bullotY -= (bullotY_change)

	player()
	show_score(textX,textY)
	pygame.display.update()
