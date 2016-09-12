#level1 gears

import pygame
import random
from PygameGame import PygameGame
from Gear import Gear
from tile import Tile


def isin(pos):
	(mx,my)=pos
	mx -= 300
	my -= 150
	k = (mx//65)*4 + (my//65) + 1
	return k

class Game1move(PygameGame):

	def init(self):
		super().init()
		self.bgColor = (255,255,255)
		self.count = 15
		self.sec = 0 
		self.min = 0
		self.timetext = "TIME : 0:00"
		self.moveup = False
		self.mute = -1

		global curk,k
		curk,k = 3,3
		global p
		p = [1,4,6,7,10,11,13,16]
		
		Gear.init()
		Tile.init()
		self.win = False
		self.gears = pygame.sprite.Group()
		self.gears.add(Gear(330,180+65*4,-1,1))
		self.gears.add(Gear(330+65*4,180,17,0))
		self.tiles = pygame.sprite.Group()

		for i in range(4):
			for j in range(4):
				x=330+65*j
				y=180+65*i
				num=j*4+i+1
				if num != curk: self.tiles.add(Tile(x,y,num))
				if num in p: 
					if num==4: 
						self.gears.add(Gear(x,y,num,1))	
					else:
						self.gears.add(Gear(x,y,num,0))

	def mousePressed(self,x,y):
		if x>=720 and x<=770 and y>=520 and y<=570: self.mute *= (-1)
		if x>=30 and x<=90 and y>=520 and y<=560: 
			self.playing = False
		global curk,k
		pos=(x,y)
		k=isin(pos)
		if k in range(1,17) and (self.win == False) and not self.moveup:
			if abs(curk-k)==1 or abs(curk-k)==4:
				self.count -= 1
				effect = pygame.mixer.Sound('sound/slide01.wav')
				effect.play()
				global p
				j=(curk-1)//4
				i=(curk-1)%4
				x=330+65*j
				y=180+65*i
				if k in p:
					p.remove(k)
					p.append(curk)
					for gear in self.gears:
						if gear.num == k:
							self.gears.remove(gear)
					self.gears.add(Gear(x,y,curk,0))
				for tile in self.tiles:
					if tile.num == k:
						self.tiles.remove(tile)
				self.tiles.add(Tile(x,y,curk))
				curk=k

	def keypressed(self,mode,mod):
		pass

	def timerFired(self,dt):
		self.gears.update(self.width, self.height)
		for gear in self.gears:
			if gear.num == -1: 
				start=gear
				gear.rotate=1
			else: 
				gear.rotate=0
				gear.angleSpeed = 0
		self.checkconnect(start,1)
		if not self.win: self.checkwin()

	def checkwin(self):
		for gear in self.gears:
			if gear.num==17 and gear.rotate != 0:
				self.win = True
				effect = pygame.mixer.Sound('sound/puzzleDone.wav')
				effect.play()

	def checkconnect(self,start,rotation):
		if start.num == -1:
			for gear in self.gears:
				if gear.num==4:
					gear.rotate = -1
					gear.angleSpeed = -5
					self.checkconnect(gear,-1)
		else:
			length=len(self.gears)
			b=False
			for gear in self.gears:
				if gear.num>0:
					n1,n2=start.num,gear.num
					row1,row2 = (n1-1)//4, (n2-1)//4
					if (abs(n1-n2)==1) and (row1==row2) or abs(n1-n2)==4:
						if gear.rotate==0:
							rotation *= (-1)
							gear.rotate = rotation
							gear.angleSpeed = gear.rotate * 5
							self.checkconnect(gear,rotation)

	def redrawAll(self,screen):
		
		color=(150,80,0)
		x,y=300,150

		global curk
		pygame.draw.rect(screen, (0,0,0), pygame.Rect(250,100,400,400))

		image = pygame.image.load("image/board1.png").convert_alpha()
		image = pygame.transform.scale(image, (800,600))
		screen.blit(image, (0,0))

		self.tiles.draw(screen)
		self.gears.draw(screen)

		pygame.draw.rect(screen, (0,0,0), pygame.Rect(294,144,6,260))
		pygame.draw.rect(screen, (0,0,0), pygame.Rect(554,144,6,260))

		pygame.draw.rect(screen, (0,0,0), pygame.Rect(294,144,260,6))
		pygame.draw.rect(screen, (0,0,0), pygame.Rect(294,399,260,6))

		font = pygame.font.SysFont("arial", 40)
		counttext = "MOVES : " + str(self.count)
		text = font.render(counttext, True, (255,0,0))
		screen.blit(text,(30,200))

		if self.count <= 0:
			if not self.moveup:
				effect = pygame.mixer.Sound('sound/Failure.wav')
				effect.play()
			self.moveup = True
			font = pygame.font.SysFont("arial", 80)
			text = font.render("Fail !!!", True, (255,0,0))
			screen.blit(text,(275,480))

		if not self.win and not self.moveup: self.sec += 6

		if self.sec >= 6000:
			self.sec = 0
			self.min += 1

		if (self.sec//100) < 10:
			self.timetext = "TIME : " + str(self.min) + ":0" + str(self.sec//100)	
		else:
			self.timetext = "TIME : " + str(self.min) + ":" + str(self.sec//100)

		font = pygame.font.SysFont("arial", 40)
		text = font.render(self.timetext, True, (255,255,255))
		screen.blit(text,(30,260))

		font = pygame.font.SysFont("arial", 40)
		text = font.render("Back", True, (255,255,255))
		screen.blit(text,(30,520))

		if self.mute == 1: 
			image = pygame.image.load("image/mute.png").convert_alpha()
			image = pygame.transform.scale(image, (50,50))
			screen.blit(image, (720,520))
		else:
			image = pygame.image.load("image/audio.png").convert_alpha()
			image = pygame.transform.scale(image, (50,50))
			screen.blit(image, (720,520))	

		if self.win:
			font = pygame.font.SysFont("chalkduster", 70)
			text = font.render("Level Passed!", True, (255,255,255))
			screen.blit(text,(175,472))

#Game1move(800,600).run()

