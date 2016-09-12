#level4

import pygame
from PygameGame import PygameGame
from Gear import Gear
from Pipe import Pipe
from tile import Tile

def isin(pos):
	(mx,my)=pos
	mx -= 300
	my -= 150
	k = (mx//65)*4 + (my//65) + 1
	return k

class Game4move(PygameGame):

	def init(self):
		super().init()
		self.bgColor = (255,255,255)
		self.count = 50
		self.sec = 0 
		self.min = 0
		self.timetext = "TIME : 0:00"
		self.moveup = False
		self.mute = -1

		global curk,k
		curk,k = 16,16
		global pg,pp
		pg = [2,7,10,11,14]
		pp = [1,3,4,5,9,13]
		
		Gear.init()
		Tile.init()
		Pipe.init()

		self.win = False
		self.gears = pygame.sprite.Group()
		self.pipes = pygame.sprite.Group()

		self.gears.add(Gear(330-65,180+65,-1,0))
		self.gears.add(Gear(330+65*4,180,17,0))

		self.tiles = pygame.sprite.Group()

		for i in range(4):
			for j in range(4):
				x=330+65*j
				y=180+65*i
				num=j*4+i+1
				if num != curk: self.tiles.add(Tile(x,y,num))
				if num in pg: 
					self.gears.add(Gear(x,y,num,0))
				if num in pp:
					if num == 13:
						self.pipes.add(Pipe(x,y,num,4))
					elif num == 5:
						self.pipes.add(Pipe(x,y,num,5))
					else:
						self.pipes.add(Pipe(x,y,num,1))

		self.exit = 20
		self.exittype = 1
		self.timer = 15

	def mousePressed(self,x,y):
		if x>=720 and x<=770 and y>=520 and y<=570: self.mute *= (-1)
		if x>=30 and x<=90 and y>=520 and y<=560: 
			self.playing = False
		global curk
		pos=(x,y)
		k=isin(pos)
		if k in range(1,17) and not self.win and not self.moveup:
			if abs(curk-k)==1 or abs(curk-k)==4:
				self.count -= 1
				effect = pygame.mixer.Sound('sound/buttonPress.wav')
				effect.play()
				global pg,pp
				j=(curk-1)//4
				i=(curk-1)%4
				x=330+65*j
				y=180+65*i
				if k in pp:
					pp.remove(k)
					pp.append(curk)
					for pipe in self.pipes:
						if pipe.num == k:
							pstyle = pipe.style
							self.pipes.remove(pipe)
					self.pipes.add(Pipe(x,y,curk,pstyle))
				elif k in pg:
					pg.remove(k)
					pg.append(curk)
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
		self.timer -= 2
		if self.timer <= 0: self.timer = 15
		self.gears.update(self.width, self.height)
		for pipe in self.pipes:
			pipe.steam = False
		for gear in self.gears:
			gear.rotate = 0
			gear.angleSpeed = 0
		x,y,direction = 4,4,"right"
		self.checksteam(x,y,direction)
		cog = self.checkgear()
		gearsound = pygame.mixer.Sound('sound/gear2.wav')
		if cog: 
			gearsound.play()
			start = None
			for gear in self.gears:
				if gear.num == -1:
					gear.rotate = 1
					gear.angleSpeed = 5
					start = gear
			self.checkconnect(start,1)
		else:
			gearsound.stop()
		if not self.win: self.checkwin()

	def checkgear(self):
		for pipe in self.pipes:
			if pipe.num == 3:
				if pipe.style == 1 or pipe.style == 4:
					return pipe.steam
		return False
				

	def checksteam(self,x,y,direction):
		if x<=4 and y<=4 and x>0 and y>0:
			number = (y-1)*4+x
			for pipe in self.pipes:
				if pipe.num == number:
					connected = False
					if pipe.style == 1:
						if direction == "left":
							connected = True
							y += 1
						if direction == "right":
							connected = True
							y -= 1
					if pipe.style == 4:
						if direction == "left":
							connected = True
							x += 1
							direction = "up"
						if direction == "down":
							connected = True
							y -= 1
							direction = "right"
					if pipe.style == 5:
						if direction == "up":
							connected = True
							y += 1
							direction = "left"
						if direction == "right":
							connected = True
							x -= 1
							direction = "down"
					if connected:
						self.exit = number
						self.exittype = pipe.style
						pipe.steam = True
						self.checksteam(x,y,direction)

	def checkwin(self):
		for gear in self.gears:
			if gear.num==17 and gear.rotate != 0:
				self.win = True
				effect = pygame.mixer.Sound('sound/puzzleDone.wav')
				effect.play()

	def checkconnect(self,start,rotation):
		if start.num == -1:
			for gear in self.gears:
				if gear.num==2:
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

		image = pygame.image.load("image/steam3.png").convert_alpha()
		image = pygame.transform.scale(image, (33,66))
		screen.blit(image, (266+65*4+33,341))

		image = pygame.image.load("image/steam4-2.png").convert_alpha()
		image = pygame.transform.scale(image, (65,60))
		screen.blit(image, (266+33-65,341-65+5))

		image = pygame.image.load("image/steam2.png").convert_alpha()
		image = pygame.transform.scale(image, (22,55))
		screen.blit(image, (266+33-65+20,341-115))	

		self.tiles.draw(screen)
		self.gears.draw(screen)
		self.pipes.draw(screen)

		pygame.draw.rect(screen, (0,0,0), pygame.Rect(294,144,6,260))
		pygame.draw.rect(screen, (0,0,0), pygame.Rect(554,144,6,260))

		pygame.draw.rect(screen, (0,0,0), pygame.Rect(294,144,260,6))
		pygame.draw.rect(screen, (0,0,0), pygame.Rect(294,399,260,6))

		font = pygame.font.SysFont("arial", 35)
		counttext = "MOVES : " + str(self.count)
		text = font.render(counttext, True, (255,0,0))
		screen.blit(text,(15,200))

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

		font = pygame.font.SysFont("arial", 35)
		text = font.render(self.timetext, True, (255,255,255))
		screen.blit(text,(15,260))

		if self.exit!=3:
			j=(self.exit-1)//4
			i=(self.exit-1)%4
			x=330+65*j
			y=180+65*i
			if self.exittype == 1 or self.exittype == 4: 
				x -= 75
				y -= 6
				pygame.draw.ellipse(screen,(255,255,255),pygame.Rect(x+2.5*self.timer,y+0.5*self.timer,36-2*self.timer,18-self.timer))
			if self.exittype == 2 or self.exittype == 5: 
				x -= 4
				y -= 80
				pygame.draw.ellipse(screen,(255,255,255),pygame.Rect(x+0.5*self.timer,y+2.5*self.timer,18-self.timer,36-2*self.timer))

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
#Game4move(800,600).run()

