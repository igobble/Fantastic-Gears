'''
Level2.py
'''

import pygame
import random
from PygameGame import PygameGame
from Pipe import Pipe
from tile import Tile
from Gear import Gear

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

def isin(pos):
	(mx,my)=pos
	mx -= 300
	my -= 150
	k = (mx//65)*4 + (my//65) + 1
	return k

class Game2(PygameGame):

	def init(self,voice=1):
		if voice==1: super().init()
		self.bgColor = (255,255,255)
		self.count = 0
		self.sec = 0 
		self.min = 0
		self.timetext = "TIME: 0:00"
		self.timechange = False
		self.movechange = False
		self.mute = -1
		self.mode = "play"
		#self.mode = "solve"
		self.solvelist = [11,12,8,7,6,10,11,12,8,4,3,7,6,5,9,10,14,13]
		self.solvelist += [9,5,6,10,9,5,1,2,6,10,14,15,16,12,11,10,14]
		self.solvelist += [15,11,10,9,13,14,15,11,7]
		self.solveindex = len(self.solvelist)-1

		datastring = "1000\n"
		datastring += "1000\n"
		writeFile("game2data.txt",datastring)

		global curk,k
		curk,k = 3,3
		global p1,p2,p3
		p1 = [5,8,9,12]
		p2 = [2,14,15]
		p3 = [13]
		
		Pipe.init()
		Tile.init()
		Gear.init()

		self.win = False
		self.pipes = pygame.sprite.Group()
		self.tiles = pygame.sprite.Group()
		self.gears = pygame.sprite.Group()

		self.gears.add(Gear(330+65*3+5,180-55,-1,0,1))

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
				elif num!= curk:
					self.tiles.add(Tile(x,y,num))
		self.exit = 0
		self.exittype = 0
		self.timer = 15

	def mousePressed(self,x,y):
		if x>=720 and x<=770 and y>=520 and y<=570: self.mute *= (-1)
		elif x>=30 and x<=90 and y>=520 and y<=560: 
			self.playing = False
		elif x>=30 and x<=150 and y>=320 and y<=360: 
			self.mode = "solve"
		elif x>=30 and x<=150 and y>=380 and y<=420:
			self.init(-1)
		else:
			pos=(x,y)
			k=isin(pos)
			self.movetiles(k)

	def movetiles(self,k):
		global curk
		if not self.win and k in range(1,17):
			if abs(curk-k)==1 or abs(curk-k)==4:
				self.solvelist += [curk]
				self.solveindex += 1
				if self.mode == "play": self.count += 1
				effect = pygame.mixer.Sound('sound/slide01.wav')
				effect.play()
				global p1,p2,p3
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
				else:
					for tile in self.tiles:
						if tile.num == k:
							self.tiles.remove(tile)
					self.tiles.add(Tile(x,y,curk))
				curk=k

	def keypressed(self,mode,mod):
		pass

	def timerFired(self,dt):
		if self.mode == "solve" and self.solveindex>=0:
			k = self.solvelist[self.solveindex]
			self.movetiles(k)
			self.solveindex -= 1
		self.exit,self.exittype = 0,0
		self.timer -= 2
		if self.timer <= 0: self.timer = 15
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
							direction = "right"
						elif direction == "left":
							connected = True
							x -= 1
							direction = "down"
					if connected: 
						self.exit = number
						self.exittype = pipe.style
						pipe.steam = True
						self.checkconnect(x,y,direction)

	def checkwin(self):
		for pipe in self.pipes:
			if (pipe.num==13) and (pipe.steam):
				if (self.exit == 13):
					for gear in self.gears:
						gear.angleSpeed = 5
						self.win = True
						s = readFile("gamepass.txt")
						count = 0 
						new = ""
						for line in s.splitlines():
							if count == 2:
								new += "1\n"
							else:
								new += line + "\n"
							count += 1
						writeFile("gamepass.txt",new)
						if self.mode == "play":
							datastring = readFile("game2data.txt")
							mincount = int(datastring.splitlines()[0])
							mintime = int(datastring.splitlines()[1])
							if self.count < mincount: 
								mincount = self.count
								self.movechange = True
							curtime = self.min*60+self.sec//100
							if curtime < mintime: 
								mintime = curtime
								self.timechange = True

							datastring = ""
							datastring = str(mincount)+"\n"
							datastring += str(mintime)+"\n"
							print(datastring)
							writeFile("game2data.txt",datastring)

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
		counttext = "MOVE: " + str(self.count)
		text = font.render(counttext, True, (255,255,255))
		screen.blit(text,(30,200))

		if not self.win and self.mode == "play": self.sec += 6

		if self.sec >= 6000:
			self.sec = 0
			self.min += 1

		if (self.sec//100) < 10:
			self.timetext = "TIME: " + str(self.min) + ":0" + str(self.sec//100)	
		else:
			self.timetext = "TIME: " + str(self.min) + ":" + str(self.sec//100)

		font = pygame.font.SysFont("arial", 40)
		text = font.render(self.timetext, True, (255,255,255))
		screen.blit(text,(30,260))

		datastring = readFile("game2data.txt")
		mincount = int(datastring.splitlines()[0])
		mintime = int(datastring.splitlines()[1])
		minmin = mintime // 60
		minsec = mintime % 60

		if self.movechange: 
			color = (255,0,0)
		else:
			color = (255,255,255)

		font = pygame.font.SysFont("comicsansms", 25)
		counttext = "Best Move: " + str(mincount)
		text = font.render(counttext, True, color)
		screen.blit(text,(580,40))

		if self.timechange: 
			color = (255,0,0)
		else:
			color = (255,255,255)

		font = pygame.font.SysFont("comicsansms", 25)
		if minsec < 10:
			timetext = "Best Time: " + str(minmin) + ":0" + str(minsec)	
		else:
			timetext = "Best Time: " + str(minmin) + ":" + str(minsec)
		text = font.render(timetext, True, color)
		screen.blit(text,(580,80))
		
		font = pygame.font.SysFont("arial", 40)
		text = font.render("SOLVE", True, (0,0,0))
		screen.blit(text,(30,320))

		font = pygame.font.SysFont("arial", 40)
		text = font.render("RETRY", True, (0,0,0))
		screen.blit(text,(30,380))

		if self.mute == 1: 
			image = pygame.image.load("image/mute.png").convert_alpha()
			image = pygame.transform.scale(image, (50,50))
			screen.blit(image, (720,520))
		else:
			image = pygame.image.load("image/audio.png").convert_alpha()
			image = pygame.transform.scale(image, (50,50))
			screen.blit(image, (720,520))	

		font = pygame.font.SysFont("arial", 40)
		text = font.render("Back", True, (255,255,255))
		screen.blit(text,(30,520))
		
		if self.exit!=13:
			j=(self.exit-1)//4
			i=(self.exit-1)%4
			x=330+65*j
			y=180+65*i
			if self.exittype == 1 or self.exittype == 0: 
				x += 48
				y -= 12
				pygame.draw.ellipse(screen,(255,255,255),pygame.Rect(x-self.timer,y+self.timer,36-2*self.timer,18-self.timer))
			if self.exittype == 2 or self.exittype == 3: 
				x -= 6
				y -= 80
				pygame.draw.ellipse(screen,(255,255,255),pygame.Rect(x+0.5*self.timer,y+2.5*self.timer,18-self.timer,36-2*self.timer))

		if self.win:
			font = pygame.font.SysFont("comicsansms", 80)
			text = font.render("Level Passed!", True, (255,255,255))
			screen.blit(text,(180,400))

#Game2(800,600).run()


