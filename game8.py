#level8

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

class Game8(PygameGame):

	def init(self,voice=1):
		if voice==1: super().init()
		self.bgColor = (255,255,255)
		self.count = 0
		self.sec = 0 
		self.flysec = 0
		self.min = 0
		self.timetext = "TIME: 0:00"
		self.timechange = False
		self.movechange = False
		self.mute = -1
		self.mode = "play"
		#self.mode = "solve"
		self.solvelist = [7,8,4,3,7,11,15,14,10,11,7,6,5]
		self.solvelist += [9,13,14,10,9,5,6,10,9,5,1]
		self.solvelist += [2,6,10,11,15,14,10,6]
		self.solvelist += [7,11,15,16,12,11,10,14,15,16,12,11]
		self.solveindex = len(self.solvelist)-1

		datastring = "1000\n"
		datastring += "1000\n"
		writeFile("game8data.txt",datastring)

		global curk1,curk2
		curk1,curk2 = 7,11
		global p1,p2
		p1 = [2,3,5,8,9,12,14,15]
		p2 = [2,4,7,14]
		self.flip = 1
		
		Pipe.init()
		Tile.init()
		Gear.init()

		self.win = False
		self.pipes = pygame.sprite.Group()
		self.backpipes = pygame.sprite.Group()
		self.tiles = pygame.sprite.Group()
		self.backtiles = pygame.sprite.Group()
		self.gears = pygame.sprite.Group()

		self.gears.add(Gear(265,118,-1,0,1))

		for i in range(4):
			for j in range(4):
				x=332+65*j
				y=180+65*i
				num = j*4+i+1
				if num in p1: 
					self.pipes.add(Pipe(x,y,num,1))	
				elif num!= curk1:
					self.tiles.add(Tile(x,y,num))

		for i in range(4):
			for j in range(4):
				x=332+65*j
				y=180+65*i
				num = j*4+i+1
				if num in p2: 
					self.backpipes.add(Pipe(x,y,num,2))	
				elif num!= curk2:
					self.backtiles.add(Tile(x,y,num))

		self.exit1 = 0
		self.exittype1 = "left"
		self.exit2 = 0
		self.exittype2 = "none"
		self.timer = 15
		self.gassound = pygame.mixer.Sound('sound/gas01.wav')
		self.gassound.play()
		self.gassound.set_volume(0.2)

	def mousePressed(self,x,y):
		if x>=720 and x<=770 and y>=520 and y<=570: 
			self.mute *= (-1)
		elif x>=30 and x<=90 and y>=520 and y<=560: 
			self.playing = False
		elif x>=600 and x<=760 and y>=240 and y<=320: 
			self.flip *= (-1)     #flip side
		elif x>=30 and x<=150 and y>=320 and y<=360: 
			self.mode = "solve"
		elif x>=30 and x<=150 and y>=380 and y<=420:
			self.init(-1)
		elif self.flip == 1:
			pos=(x,y)
			k=isin(pos)
			self.movetiles1(k)
		else:
			pos=(x,y)
			k=isin(pos)
			self.movetiles2(k)

	def movetiles1(self,k):
		global curk1,curk2
		curk = curk1
		if not self.win and k in range(1,17):
			if abs(curk-k)==1 or abs(curk-k)==4:
				self.solvelist += [curk]
				self.solveindex += 1
				if self.mode == "play": self.count += 1
				effect = pygame.mixer.Sound('sound/slide01.wav')
				effect.play()
				global p1,p2
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
				else:
					for tile in self.tiles:
						if tile.num == k:
							self.tiles.remove(tile)
					self.tiles.add(Tile(x,y,curk))
				k1 = k
				j=(curk2-1)//4
				i=(curk2-1)%4
				x=330+65*j
				y=180+65*i
				j=3-(k-1)//4
				i=(k-1)%4
				k2 = j*4+i+1
				curk = curk2
				k = k2
				if k in p2:
					p2.remove(k)
					p2.append(curk)
					for pipe in self.backpipes:
						if pipe.num == k:
							self.backpipes.remove(pipe)
					self.backpipes.add(Pipe(x,y,curk,2))
				else:
					for tile in self.backtiles:
						if tile.num == k:
							self.backtiles.remove(tile)
					self.backtiles.add(Tile(x,y,curk))
				curk1 = k1
				curk2 = k2

	def movetiles2(self,k):
		global curk1,curk2
		curk= curk2
		if not self.win and k in range(1,17):
			if abs(curk-k)==1 or abs(curk-k)==4:
				self.solvelist += [curk1]
				self.solveindex += 1
				if self.mode == "play": self.count += 1
				effect = pygame.mixer.Sound('sound/slide01.wav')
				effect.play()
				j=(curk-1)//4
				i=(curk-1)%4
				x=330+65*j
				y=180+65*i
				if k in p2:
					p2.remove(k)
					p2.append(curk)
					for pipe in self.backpipes:
						if pipe.num == k:
							self.backpipes.remove(pipe)
					self.backpipes.add(Pipe(x,y,curk,2))
				else:
					for tile in self.backtiles:
						if tile.num == k:
							self.backtiles.remove(tile)
					self.backtiles.add(Tile(x,y,curk))
				k2 = k
				j=(curk1-1)//4
				i=(curk1-1)%4
				x=330+65*j
				y=180+65*i
				j=3-(k-1)//4
				i=(k-1)%4
				k1 = j*4+i+1
				curk = curk1
				k = k1
				if k in p1:
					p1.remove(k)
					p1.append(curk)
					for pipe in self.pipes:
						if pipe.num == k:
							self.pipes.remove(pipe)
					self.pipes.add(Pipe(x,y,curk,1))
				else:
					for tile in self.tiles:
						if tile.num == k:
							self.tiles.remove(tile)
					self.tiles.add(Tile(x,y,curk))
				curk1 = k1
				curk2 = k2

	def keypressed(self,mode,mod):
		pass

	def timerFired(self,dt):
		if self.mode == "solve" and self.solveindex>=0:
			#self.flip = 1
			k = self.solvelist[self.solveindex]
			self.movetiles1(k)
			self.solveindex -= 1
		if self.flysec>0:
			if self.flysec % 8 == 0 : self.flip *= -1
		self.gears.update(self.width, self.height)
		self.timer -= 4
		if self.timer <= 0: self.timer = 15
		for pipe in self.pipes:
			pipe.steam = False
		for pipe in self.backpipes:
			pipe.steam = False
		self.exit1 = 0
		self.exittype1 = "left"
		self.checkconnect1(4,1,"left")
		self.exit2 = 0
		self.exittype2 = "none"
		for pipe in self.pipes:
			if pipe.num == 16 and pipe.steam: 
				self.exit2 = 4
				self.exittype2 = "init"
				self.checkconnect2(4,1,"down")
		for pipe in self.backpipes:
			if pipe.num == 1 and pipe.steam: 
				self.exit1 = 13
				self.exittype1 = "right"
				self.checkconnect1(1,4,"right")
		if not self.win: self.checkwin()
		if self.win: 
			pygame.mixer.music.load('sound/gear1.wav')
			pygame.mixer.music.play()

	def checkconnect1(self,x,y,direction):
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
					if connected: 
						self.exit1 = number
						self.exittype1 = direction
						pipe.steam = True
						self.checkconnect1(x,y,direction)

	def checkconnect2(self,x,y,direction):
		if x<=4 and y<=4 and x>0 and y>0:
			number = (y-1)*4+x
			for pipe in self.backpipes:
				if pipe.num == number:
					connected = False
					if pipe.style == 2:
						if direction=="down": 
							connected = True
							x -= 1
						elif direction=="up": 
							connected = True
							x += 1
					if connected: 
						self.exit2 = number
						self.exittype2 = direction
						pipe.steam = True
						self.checkconnect2(x,y,direction)

	def checkwin(self):
		for pipe in self.pipes:
			if (pipe.num==1) and (pipe.steam):
				for gear in self.gears:
					gear.angleSpeed = 10
					self.win = True

					if self.mode == "play":
						datastring = readFile("game8data.txt")
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
						writeFile("game8data.txt",datastring)

					self.gassound.stop()
					effect = pygame.mixer.Sound('sound/puzzleDone.wav')
					effect.play()

	def redrawAll(self,screen):
		
		color=(150,80,0)
		x,y=300,150

		pygame.draw.rect(screen, (0,0,0), pygame.Rect(220,70,400,400))

		image = pygame.image.load("image/board1.png").convert_alpha()
		image = pygame.transform.scale(image, (800,600))
		screen.blit(image, (0,0))

		image = pygame.image.load("image/bg2.png").convert_alpha()
		image = pygame.transform.scale(image, (160,80))
		screen.blit(image, (600,240))
		font = pygame.font.SysFont("arial", 40)
		text = font.render("Flip Side", True, (255,255,255))
		screen.blit(text,(605,252))

		if self.flip == 1:
			image = pygame.image.load("image/steam1.png").convert_alpha()
			image = pygame.transform.scale(image, (33,66))
			screen.blit(image, (266,341))		

			image = pygame.image.load("image/ds4.png").convert_alpha()
			image = pygame.transform.scale(image, (65,40))
			screen.blit(image, (495,90))	

			image = pygame.image.load("image/ds3.png").convert_alpha()
			image = pygame.transform.scale(image, (65,100))
			screen.blit(image, (495+65,95))	

			image = pygame.image.load("image/ds6.png").convert_alpha()
			image = pygame.transform.scale(image, (65,40))
			screen.blit(image, (495,90+65*5+14))	

			image = pygame.image.load("image/ds5.png").convert_alpha()
			image = pygame.transform.scale(image, (65,100))
			screen.blit(image, (495+65,95+65*4+8))	

			image = pygame.image.load("image/steam4-2.png").convert_alpha()
			image = pygame.transform.scale(image, (65,60))
			screen.blit(image, (266+33-65,211-65+5))

			image = pygame.image.load("image/steam2.png").convert_alpha()
			image = pygame.transform.scale(image, (22,55))
			screen.blit(image, (266+33-65+20,211-115))	

			self.tiles.draw(screen)
			self.pipes.draw(screen)
			self.gears.draw(screen)

			if self.exit1!=16 and not self.win:
				j=(self.exit1-1)//4
				i=(self.exit1-1)%4
				x=330+65*j
				y=180+65*i
				if self.exittype1 == "right": 
					x -= 75
					y -= 6
					pygame.draw.ellipse(screen,(255,255,255),pygame.Rect(x+2.5*self.timer,y+0.5*self.timer,36-2*self.timer,18-self.timer))
				if self.exittype1 == "left": 
					x += 48
					y -= 12
					pygame.draw.ellipse(screen,(255,255,255),pygame.Rect(x-self.timer,y+self.timer,36-2*self.timer,18-self.timer))
			j=(curk1-1)//4
			i=(curk1-1)%4
			x=330+65*j
			y=180+65*i
			if self.exittype2 == "down" and self.exit2-1==curk2: 
				x -= 4
				y -= 15
				pygame.draw.ellipse(screen,(255,255,255),pygame.Rect(x+0.5*self.timer,y+2.5*self.timer,18-self.timer,36-2*self.timer))

		else:
			self.backtiles.draw(screen)
			self.backpipes.draw(screen)
			image = pygame.image.load("image/steam5.png").convert_alpha()
			image = pygame.transform.scale(image, (65,35))
			screen.blit(image, (298,405))		

			image = pygame.image.load("image/steam6.png").convert_alpha()
			image = pygame.transform.scale(image, (65,35))
			screen.blit(image, (518-4*65+45,115))	

			if self.exit2!=1 and not self.win:
				j=(self.exit2-1)//4
				i=(self.exit2-1)%4
				x=330+65*j
				y=180+65*i
				if self.exittype2 == "down" or self.exittype2 == "init": 
					x -= 4
					y -= 80
					if self.exittype2 == "init": y += 65
					pygame.draw.ellipse(screen,(255,255,255),pygame.Rect(x+0.5*self.timer,y+2.5*self.timer,18-self.timer,36-2*self.timer))
				if self.exittype2 == "up":
					x -= 5
					y += 32
					pygame.draw.ellipse(screen,(255,255,255),pygame.Rect(x+0.5*self.timer,y,18-self.timer,36-2*self.timer))
			j=(curk2-1)//4
			i=(curk2-1)%4
			x=330+65*j
			y=180+65*i
			if self.exittype1 == "left" and self.exit1+4==curk1: 
				x -= 10
				y -= 6
				pygame.draw.ellipse(screen,(255,255,255),pygame.Rect(x+2.5*self.timer,y+0.5*self.timer,36-2*self.timer,18-self.timer))
			if self.exittype1 == "right" and self.exit1-4==curk1: 
				x += 48
				y -= 12
				pygame.draw.ellipse(screen,(255,255,255),pygame.Rect(x-self.timer,y+self.timer,36-2*self.timer,18-self.timer))

				
		pygame.draw.rect(screen, (0,0,0), pygame.Rect(294,144,6,260))
		pygame.draw.rect(screen, (0,0,0), pygame.Rect(554,144,6,260))

		pygame.draw.rect(screen, (0,0,0), pygame.Rect(294,144,260,6))
		pygame.draw.rect(screen, (0,0,0), pygame.Rect(294,399,260,6))

		font = pygame.font.SysFont("arial", 40)
		counttext = "MOVE: " + str(self.count)
		text = font.render(counttext, True, (255,255,255))
		screen.blit(text,(30,200))

		if not self.win and self.mode == "play": self.sec += 15
		if self.mode == "solve": self.flysec += 1

		if self.sec >= 6000:
			self.sec = 0
			self.min += 1

		if self.sec%100 == 0 or 1==1:
			if (self.sec//100) < 10:
				self.timetext = "TIME: " + str(self.min) + ":0" + str(self.sec//100)	
			else:
				self.timetext = "TIME: " + str(self.min) + ":" + str(self.sec//100)

		font = pygame.font.SysFont("arial", 40)
		text = font.render(self.timetext, True, (255,255,255))
		screen.blit(text,(30,260))

		datastring = readFile("game8data.txt")
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
		screen.blit(text,(580,15))

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
		screen.blit(text,(580,55))

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

		font = pygame.font.SysFont("arial", 40)
		text = font.render("SOLVE", True, (0,0,0))
		screen.blit(text,(30,320))

		font = pygame.font.SysFont("arial", 40)
		text = font.render("RETRY", True, (0,0,0))
		screen.blit(text,(30,380))

		if self.win:
			font = pygame.font.SysFont("chalkduster", 70)
			text = font.render("Level Passed!", True, (255,255,255))
			screen.blit(text,(175,472))

		 
#Game8(800,600).run()


