from __future__ import print_function
import pygame, sys
from pygame.locals import *
from random import randint
from time import sleep

class Player:

	def __init__(self):
		self.size = 25
		self.x = screenwidth / 3 - 50 #center x
		self.y = screenheight / 2 #center y
		self.rectangle = Rect(0, 0, self.size, self.size)
		self.rectangle.center = (self.x, self.y)
		self.yvel = 0
		self.gravity = .4
		self.terminalvelocity = 13
		self.jumpvel = 6.3
		self.score = 0
		self.isalive = True
		self.time = 0

	def move(self):
		self.yvel -= self.gravity
		if abs(self.yvel) >= self.terminalvelocity:
			self.yvel = -self.terminalvelocity
		self.rectangle.y -= self.yvel
		if self.time != 0:
			self.time += 1
			if self.time >= 6:
				self.time = 0
		if self.rectangle.top > screenheight or self.rectangle.top < 0:
			self.isalive = False
			return
		for box in obstacles:
			if self.rectangle.colliderect(box.rectangle1) or self.rectangle.colliderect(box.rectangle2):
				self.isalive = False

	def startjump(self):
		if self.time == 0:
			self.yvel = self.jumpvel
			self.time += 1

	def getrect(self):
		return (self.rectangle.x, self.rectangle.y, self.rectangle.width, self.rectangle.height)

class Obstacles:

	def __init__(self):
		self.notpassed = True
		self.x = screenwidth
		self.width = 40
		self.heightgap = 100
		self.y = randint(screenheight * 2 // 7, screenheight * 5 // 7)
		self.rectangle1 = Rect(self.x, 0, self.width, self.y)
		self.rectangle2 = Rect(self.x, self.y + self.heightgap, self.width, screenheight - self.heightgap - self.y)

	def move(self):
		self.rectangle1.x -= 2
		self.rectangle2.x -= 2

	def getrect(self):
		return [(self.rectangle1.x, self.rectangle1.y, self.rectangle1.width, self.rectangle1.height), 
		        (self.rectangle2.x, self.rectangle2.y, self.rectangle2.width, self.rectangle2.height)]	

pygame.init()
fpsClock = pygame.time.Clock()

screenwidth = 600
screenheight = 400

windowSurfaceObj = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption('Flappy Box by Mitsuru Otsuka')

fontObj = pygame.font.Font('freesansbold.ttf', 24)

white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
black = pygame.Color(0, 0, 0)

while True:
	#Game variables
	obstacles = []
	started = False
	spawncount = 23
	player = Player()
	pygame.event.clear()

	while player.isalive:
		windowSurfaceObj.fill(white)
		if started:
			#Box spawn counter
			if spawncount >= 80:
				spawncount = 0
				obstacles.append(Obstacles())
			spawncount += 1
			#Move stuff and draw
			player.move()
			pygame.draw.rect(windowSurfaceObj, green, player.getrect())
			for box in obstacles:
				box.move()
				if box.rectangle1.right < 0:
					if box in obstacles:
						obstacles.remove(box)
					continue
				if box.notpassed and box.rectangle1.centerx <= player.rectangle.x:
					box.notpassed = False
					player.score += 1
				pygame.draw.rect(windowSurfaceObj, red, box.getrect()[0])
				pygame.draw.rect(windowSurfaceObj, red, box.getrect()[1])
			msgSurfaceObj = fontObj.render('Score: ' + str(player.score), False, black)
			msgRectobj = msgSurfaceObj.get_rect()
			msgRectobj.center = (screenwidth / 2, 15)
			windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
		else:
			pygame.draw.rect(windowSurfaceObj, green, player.getrect())
			msgSurfaceObj = fontObj.render('Press Space to Start', False, black)
			msgRectobj = msgSurfaceObj.get_rect()
			msgRectobj.center = (screenwidth / 2, screenheight / 2)
			windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
		#User input
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_SPACE:
					started = True
					player.startjump()
				elif event.key == K_q:
					pygame.quit()
					sys.exit()
                        elif event.type == MOUSEBUTTONDOWN:
				started = True
				player.startjump()
		#Update screen and FPS delay
		pygame.display.update()
		fpsClock.tick(60)
	sleep(2)
