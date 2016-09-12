'''
Level7.py
'''

import pygame
import random
from PygameGame import PygameGame
from Pipe import Pipe
from tile import Tile
from Gear import Gear

def isin(pos):
	(mx,my)=pos
	mx -= 300
	my -= 150
	k = (mx//65)*4 + (my//65) + 1
	return k

class Game7move(PygameGame):

	def init(self):
		super().init()
		self.bgColor = (255,255,255)
		self.count = 60
		self.sec = 0 
		self.min = 0
		self.timetext = "TIME : 0:00"
		self.moveup = False
		self.mute = -1

		global curk,k
		curk,k = 4,4
		global p1,p2,p3,p4,p5,p6,p7
		p1 = [5,7,10,12,15]
		p2 = [8,9]
		p3 = [14]
		p4 = []
		p5 = [3]
		p6 = [2]
		p7 = [6,11]
		
		Pipe.init()
		Tile.init()
		Gear.init()

		self.win = False
		self.pipes = pygame.sprite.Group()
		self.tiles = pygame.sprite.Group()
		self.gears = pygame.sprite.Group()

		self.gears.add(Gear(330+65*3+5,180-55,-1,0))

		for i in range(4):
			for j in range(4):
				x=332+65*j
				y=180+65*i
				num = j*4+i+1
				if num in p1: 
					self.pipes.add(Pipe(x,y,num,1))	
				elif num in p2:
					self.pipes.add(Pipe(x,y,num,2))
				elif num in p3:
					self.pipes.add(Pipe(x,y,num,3))
				elif num in p4:
					self.pipes.add(Pipe(x,y,num,4))
				elif num in p5:
					self.pipes.add(Pipe(x,y,num,5))
				elif num in p6:
					self.pipes.add(Pipe(x,y,num,6))
				elif num in p7:
					self.pipes.add(Pipe(x,y,num,7))
				elif num!= curk:
					self.tiles.add(Tile(x,y,num))
		self.timer = 15

	def mousePressed(self,x,y):
		if x>=720 and x<=770 and y>=520 and y<=570: self.mute *= (-1)
		if x>=30 and x<=90 and y>=520 and y<=560: 
			self.playing = False
		global curk,k
		pos=(x,y)
		k=isin(pos)
		if not self.win and k in range(1,17) and not self.moveup:
			if abs(curk-k)==1 or abs(curk-k)==4:
				self.count -= 1
				effect = pygame.mixer.Sound('sound/slide01.wav')
				effect.play()
				global p1,p2,p3,p5,p6,p7
				j=(curk-1)//4
				i=(curk-1)%4
				x=330+65*j
				y=180+65*i
				if k in p1:
					p1.remove(k)
					p1.append(curk)
					for pipe in self.pipes:
						if pipe.num == k:
							self.pipes.remove(pipe)
					self.pipes.add(Pipe(x,y,curk,1))
				elif k in p2:
					p2.remove(k)
					p2.append(curk)
					for pipe in self.pipes:
						if pipe.num == k:
							self.pipes.remove(pipe)
					self.pipes.add(Pipe(x,y,curk,2))
				elif k in p3:
					p3.remove(k)
					p3.append(curk)
					for pipe in self.pipes:
						if pipe.num == k:
							self.pipes.remove(pipe)
					self.pipes.add(Pipe(x,y,curk,3))
				elif k in p5:
					p5.remove(k)
					p5.append(curk)
					for pipe in self.pipes:
						if pipe.num == k:
							self.pipes.remove(pipe)
					self.pipes.add(Pipe(x,y,curk,5))
				elif k in p6:
					p6.remove(k)
					p6.append(curk)
					for pipe in self.pipes:
						if pipe.num == k:
							self.pipes.remove(pipe)
					self.pipes.add(Pipe(x,y,curk,6))
				elif k in p7:
					p7.remove(k)
					p7.append(curk)
					for pipe in self.pipes:
						if pipe.num == k:
							self.pipes.remove(pipe)
					self.pipes.add(Pipe(x,y,curk,7))
				else:
					for tile in self.tiles:
						if tile.num == k:
							self.tiles.remove(tile)
					self.tiles.add(Tile(x,y,curk))
				curk=k

	def keypressed(self,mode,mod):
		pass

	def timerFired(self,dt):
		self.exit = dict()
		for num in range(0,17):
			self.exit[num] = []
		self.exit[0] = ["left"]
		self.timer -= 2
		if self.timer<=0: self.timer = 15
		x,y,direction=4,1,"left"
		self.checkconnect(x,y,direction)
		if not self.win: self.checkwin()
		if self.win: 
			pygame.mixer.music.load('sound/gear1.wav')
			pygame.mixer.music.play()

	def checkconnect(self,x,y,direction):
		if x<=4 and y<=4 and x>0 and y>0:
			number = (y-1)*4+x
			for pipe in self.pipes:
				if pipe.num == number:
					connected = False
					newdirection = direction
					if pipe.style == 1:
						if direction=="left": 
							connected = True
							y += 1
						elif direction=="right": 
							connected = True
							y -= 1
					if pipe.style == 2:
						if direction == "up":
							connected = True
							x += 1
						elif direction == "down":
							connected = True
							x -= 1
					if pipe.style == 3:
						if direction == "up":
							connected = True
							y -= 1
							newdirection = "right"
						elif direction == "left":
							connected = True
							x -= 1
							newdirection = "down"
					if pipe.style == 5:
						if direction == "up":
							connected = True
							y += 1
							newdirection = "left"
						if direction == "right":
							connected = True
							x -= 1
							newdirection = "down"
					if pipe.style == 6:
						if direction == "down":
							connected = True
							y += 1
							newdirection = "left"
						if direction == "right":
							connected = True
							x += 1
							newdirection = "up"
					if pipe.style == 7:
						if direction!="right": 
							sum=pipe.entrance1+pipe.entrance2+pipe.entrance3
							if not pipe.steam or sum<2:
								pipe.steam = True
								if direction == "up":
									pipe.entrance1 = 1
									self.exit[pipe.num-1].remove("up")
									self.exit[pipe.num] += ["right"] + ["up"]
									self.checkconnect(x,y-1,"right")
									self.checkconnect(x+1,y,"up")
								if direction == "left":
									pipe.entrance2 = 1
									self.exit[pipe.num-4].remove("left")
									self.exit[pipe.num] += ["up"] + ["down"]
									self.checkconnect(x+1,y,"up")
									self.checkconnect(x-1,y,"down")
								if direction == "down":
									pipe.entrance3 = 1
									self.exit[pipe.num+1].remove("down")
									self.exit[pipe.num] += ["right"] + ["down"]
									self.checkconnect(x,y-1,"right")
									self.checkconnect(x-1,y,"down")

					if connected: 
						if direction == "up": self.exit[pipe.num-1].remove("up")
						if direction == "down": self.exit[pipe.num+1].remove("down")
						if direction == "left": self.exit[pipe.num-4].remove("left")
						if direction == "right": self.exit[pipe.num+4].remove("right")
						self.exit[pipe.num] += [newdirection]
						pipe.steam = True
						self.checkconnect(x,y,newdirection)

	def checkwin(self):
		for pipe in self.pipes:
			if (pipe.num==13) and (pipe.steam):
				m = pipe.style
				if (m == 2) or (m == 3) or (m==5) or (m == 7):
					b = True
					for pipe in self.pipes:
						if pipe.style == 7:
							sum=pipe.entrance1+pipe.entrance2+pipe.entrance3
							if sum!=2: b = False
					if b:
						for gear in self.gears:
							gear.angleSpeed = 5
							self.win = True
							effect = pygame.mixer.Sound('sound/puzzleDone.wav')
							effect.play()

	def redrawAll(self,screen):
		
		color=(150,80,0)
		x,y=300,150

		global curk

		pygame.draw.rect(screen, (0,0,0), pygame.Rect(220,70,400,400))

		image = pygame.image.load("image/board1.png").convert_alpha()
		image = pygame.transform.scale(image, (800,600))
		screen.blit(image, (0,0))

		image = pygame.image.load("image/steam1.png").convert_alpha()
		image = pygame.transform.scale(image, (33,66))
		screen.blit(image, (266,341))		

		image = pygame.image.load("image/steam2.png").convert_alpha()
		image = pygame.transform.scale(image, (22,42))
		screen.blit(image, (518,110))	

		self.tiles.draw(screen)
		self.pipes.draw(screen)

		self.gears.update(self.width, self.height)
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


		if not self.win and not self.moveup: self.sec += 7

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

		for pipe in self.pipes:
			font = pygame.font.SysFont("arial", 10)
			if pipe.style == 7:
				pipetext = str(pipe.entrance1+pipe.entrance2+pipe.entrance3)
			else:
				pipetext = str(pipe.steam)
			text = font.render(pipetext, True, (255,255,255))
			#screen.blit(text,(pipe.x,pipe.y))

		for exits in self.exit:
			if not self.win:
				j=(exits-1)//4
				i=(exits-1)%4
				xx=330+65*j
				yy=180+65*i
				exitstype = self.exit[exits]
				if "right" in exitstype: 
					x = xx-75
					y = yy-6
					pygame.draw.ellipse(screen,(255,255,255),pygame.Rect(x+2.5*self.timer,y+0.5*self.timer,36-2*self.timer,18-self.timer))
				if "down" in exitstype and not exits == 13: 
					x = xx-4
					y = yy-80
					pygame.draw.ellipse(screen,(255,255,255),pygame.Rect(x+0.5*self.timer,y+2.5*self.timer,18-self.timer,36-2*self.timer))
				if "left" in exitstype: 
					x = xx+48
					y = yy-12
					pygame.draw.ellipse(screen,(255,255,255),pygame.Rect(x-self.timer,y+self.timer,36-2*self.timer,18-self.timer))
				if "up" in exitstype:
					x = xx-5
					y = yy+32
					pygame.draw.ellipse(screen,(255,255,255),pygame.Rect(x+0.5*self.timer,y,18-self.timer,36-2*self.timer))

		
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
			font = pygame.font.SysFont("comicsansms", 80)
			text = font.render("Level Passed!", True, (255,255,255))
			screen.blit(text,(180,400))

#Game7move(800,600).run()


