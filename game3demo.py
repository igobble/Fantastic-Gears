#level4 Dimensions

import pygame
from PygameGame import PygameGame
from gear3d import Gear
from tile3d import Tile

x1,y1=155,80
x2,y2=480,80
x3,y3=480,380
x4,y4=155,380

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

def isin1(pos):
	(mx,my)=pos
	global x1,y1
	mx += 30
	my += 30
	if mx>x1 and mx<x1+3*65 and my>y1 and my<y1+3*65:
		mx = mx-x1
		my = my-y1
		k = (mx//65)*3 + (my//65) + 1
		return k
	else:
		return None

def isin2(pos):
	(mx,my)=pos
	global x2,y2
	mx += 30
	my += 30
	if mx>x2 and mx<x2+3*65 and my>y2 and my<y2+3*65:
		mx -= x2
		my -= y2
		k = (mx//65)*3 + (my//65) + 1
		return k+9
	else:
		return None

def isin3(pos):
	(mx,my)=pos
	global x3,y3
	mx += 30
	my += 30
	if mx>x3 and mx<x3+3*65 and my>y3 and my<y3+3*65:
		mx -= x3
		my -= y3
		k = (mx//65)*3 + (my//65) + 1
		return k+18
	else:
		return None

def isin4(pos):
	(mx,my)=pos
	global x4,y4
	mx += 30
	my += 30
	if mx>x4 and mx<x4+3*65 and my>y4 and my<y4+3*65:
		mx -= x4
		my -= y4
		k = (mx//65)*3 + (my//65) + 1
		return k+27
	else:
		return None

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Texture():
# simple texture class
# designed for 32 bit png images (with alpha channel)
    def __init__(self,fileName):
        self.texID=0
        self.LoadTexture(fileName)
    def LoadTexture(self,fileName): 
        try:
            textureSurface = pygame.image.load(fileName)
            textureData = pygame.image.tostring(textureSurface, "RGBA", 1)

            self.texID=glGenTextures(1)

            glBindTexture(GL_TEXTURE_2D, self.texID)
            glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA,
                        textureSurface.get_width(), textureSurface.get_height(),
                        0, GL_RGBA, GL_UNSIGNED_BYTE, textureData )
            glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        except:
            print ("can't open the texture: %s"%(fileName))
    def __del__(self):
        glDeleteTextures(self.texID)

class Game3demo(PygameGame):
	def init(self,width=800,height=600,voice=1):
		if voice==1:
			pass
		self.bgColor = (255,255,255)
		self.count = 0
		self.sec = 0 
		self.min = 0
		self.timetext = "TIME: 0:00"
		self.flysec = 0
		self.mute = -1

		global curk1,k1,x1,y1
		global curk2,k2,x2,y2
		global curk3,k3,x3,y3
		global curk4,k4,x3,y3
		curk1,k1 = 6,6
		curk2,k2 = 17,17
		curk3,k3 = 20,20
		curk4,k4 = 35,35

		global p1,p2,p2_3,p3,p3_3,p4,p4_3
		p1 = [3,5,7]
		p2 = [10,14,18]
		p2_3 = [12,16]
		p3 = [21,23,25]
		p3_3 = [19,27]
		p4 = [29]
		p4_3 = [32]
	
		Gear.init()
		Tile.init()
		self.win = False
		self.gears = list()

		self.gears.append(Gear(x1+65,y1+65*3,-1,1))
		self.gears.append(Gear(x1+65*3,y1+65,-2,0))
		self.gears.append(Gear(x2-65,y2+65,-3,0))
		self.gears.append(Gear(x2+65*3,y2+65,-4,0))
		self.gears.append(Gear(x3+65*3,y3+65,-5,0))
		self.gears.append(Gear(x3-65,y3+65,-6,0))
		self.gears.append(Gear(x4+65*3,y4+65,-7,0))
		self.gears.append(Gear(x4+65,y4+65,32,0))

		self.tiles = list()

		for i in range(3):
			for j in range(3):
				x=x1+65*j
				y=y1+65*i
				num=j*3+i+1
				if num != curk1: self.tiles.append(Tile(x,y,num))
				if num in p1: 
					self.gears.append(Gear(x,y,num,0))

		for i in range(3):
			for j in range(3):
				x=x2+65*j
				y=y2+65*i
				num=j*3+i+1+9
				if num != curk2: 
					if num in p2_3:
						self.tiles.append(Tile(x,y,num,3))
					else:
						self.tiles.append(Tile(x,y,num))
				if num in p2: 
					self.gears.append(Gear(x,y,num,0))

		for i in range(3):
			for j in range(3):
				x=x3+65*j
				y=y3+65*i
				num=j*3+i+1+18
				if num != curk3: 
					if num in p3_3:
						self.tiles.append(Tile(x,y,num,3))
					else:
						self.tiles.append(Tile(x,y,num))
				if num in p3: 
					self.gears.append(Gear(x,y,num,0))

		for i in range(3):
			for j in range(3):
				x=x4+65*j
				y=y4+65*i
				num=j*3+i+1+27
				if num != curk4: 
					if num in p4_3:
						self.tiles.append(Tile(x,y,num,3))
					else:
						self.tiles.append(Tile(x,y,num))
				if num in p4: 
					self.gears.append(Gear(x,y,num,0))

		#writeFile
		s = ""
		for tile in self.tiles:
			if tile.style != 3: s += str(tile.num)+","
		s += "\n"
		for tile in self.tiles:
			if tile.style == 3: s += str(tile.num)+","
		s += "\n"
		for gear in self.gears:
			if gear.num>0: s += str(gear.num) + ","
		s += "\n"
		s += str(curk1)+","+str(curk2)+","
		s += str(curk3)+","+str(curk4)+"\n"

		for gear in self.gears:
			if gear.rotate!=0: s += str(gear.num) + ","
		s += "\n"

		if self.win: 
			s += "True"
		else:
			s += "False"
		writeFile("foo.txt",s)

		self.vertices = (
		    #0~7
		    (1,-1,-1),(1,1,-1),(-1,1,-1),  (-1,-1,-1), 
		    (1,-1,1),(1,1,1),(-1,-1,1),(-1,1,1),   
		    #8~15
		    (-1/3,1,1),(-1/3,-1,1),(1/3,1,1),(1/3,-1,1),
		    (-1,-1/3,1),(1,-1/3,1),(-1,1/3,1), (1,1/3,1),  
			#16~23
		    (-1/3,1,-1),(-1/3,-1,-1),(1/3,1,-1),(1/3,-1,-1),
		    (-1,-1/3,-1),(1,-1/3,-1),(-1,1/3,-1),(1,1/3,-1), 
		    #24~31
		    (1,1,-1/3),(-1,1,-1/3),(1,1,1/3),(-1,1,1/3),
		    (-1,-1,-1/3),(1,-1,-1/3),(-1,-1,1/3),(1,-1,1/3), 
		    #32~35
		    (-1/3,1/3,1),(1/3,1/3,1),(-1/3,-1/3,1),(1/3,-1/3,1),
		    #36~39
		    (1,1/3,1/3),(1,1/3,-1/3),(1,-1/3,1/3),(1,-1/3,-1/3),
		    #40~43
		    (-1/3,1/3,-1),(1/3,1/3,-1),(-1/3,-1/3,-1),(1/3,-1/3,-1),
		    #44~47
		    (-1,1/3,1/3),(-1,1/3,-1/3),(-1,-1/3,1/3),(-1,-1/3,-1/3),
		    #48~51
		    (0.8,1/3,-1.2),(0.8,-1/3,-1.2),(1.2,1/3,-0.8),(1.2,-1/3,-0.8),
		    #52~55
		    (1.2,-1/3,0.8),(0.8,-1/3,1.2),(0.8,1/3,1.2),(1.2,1/3,0.8),
			#56~59
			(-0.8,1/3,1.2),(-1.2,1/3,0.8),(-1.2,-1/3,0.8),(-0.8,-1/3,1.2),
			#60~63
			(-1/3,-0.8,-1.2),(-1/3,-1.2,-0.8),(1/3,-1.2,-0.8),(1/3,-0.8,-1.2),

			#64~67
			(1,1.2,-1),(-1,1.2,-1),(1,1.2,1),(-1,1.2,1)
		)

		self.allsurfaces = (
			#1,2,3,4,5,6,7,8,9
			[2,16,40,22],[22,40,42,20],[20,42,17,3],
			[16,18,41,40],[40,41,43,42],[42,43,19,17],
			[18,1,23,41],[41,23,21,43],[43,21,0,19],

			#10,11,12,13,14,15,16,17,18
			[24,1,23,37],[37,23,21,39],[39,21,0,29],
			[26,24,37,36],[36,37,39,38],[38,39,29,31],
			[5,26,36,15],[15,36,38,13],[13,38,31,4],

			#19,20,21,22,23,24,25,26,27
			[12,34,9,6],[14,32,34,12],[7,8,32,14],
			[34,35,11,9],[32,33,35,34],[8,10,33,32],
			[35,13,4,11],[33,15,13,35],[10,5,15,33],

			#28,29,30,31,32,33,34,35,36
			[47,20,3,28],[45,22,20,47],[25,2,22,45],
			[46,47,28,30],[44,45,47,46],[27,25,45,44],
			[12,46,30,6],[14,44,46,12],[7,27,44,14],

			#37,38
			[2,1,5,7],[3,0,4,6],
			#39,40,41,42,43
			[48,50,51,49],[52,53,54,55],[56,57,58,59],[60,61,62,63],[64,65,67,66]
		)
		self.fly = False

	def Cube(self):
		glEnable(GL_TEXTURE_2D)

		tile_texture=Texture("image/tile2.png")
		tile3_texture=Texture("image/tile3.png")
		black_texture=Texture("image/black.png")
		gear_texture=Texture("image/gear2.png")
		gear1_texture=Texture("image/gear1.png")
		screw1_texture=Texture("image/airscrew1.png")
		screw2_texture=Texture("image/airscrew2.png")
		screw3_texture=Texture("image/airscrew3.png")
		screw4_texture=Texture("image/airscrew4.png")

		glEnable(GL_DEPTH_TEST)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glDisable(GL_LIGHTING)
		glDepthFunc(GL_LEQUAL)
		glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
		glEnable(GL_BLEND)	
		glEnable(GL_TEXTURE_2D)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

		glPushMatrix()

		glBindTexture(GL_TEXTURE_2D,tile_texture.texID)

		glBegin(GL_QUADS)
		x=0 
		for surface in self.allsurfaces:
			x += 1
			if x in self.surfaces:
				a,b,c,d = surface[0],surface[1],surface[2],surface[3]

				a1,a2,a3 = self.vertices[a]
				b1,b2,b3 = self.vertices[b]
				c1,c2,c3 = self.vertices[c]
				d1,d2,d3 = self.vertices[d]

				glTexCoord2f(0,0)
				glVertex3f(a1/3,a2/3,(a3-1)/3)
				glTexCoord2f(0,1)
				glVertex3f(b1/3,b2/3,(b3-1)/3)
				glTexCoord2f(1,1)
				glVertex3f(c1/3,c2/3,(c3-1)/3)
				glTexCoord2f(1,0)
				glVertex3f(d1/3,d2/3,(d3-1)/3)

		glEnd()

		glBindTexture(GL_TEXTURE_2D,tile3_texture.texID)

		glBegin(GL_QUADS)
		x=0 
		for surface in self.allsurfaces:
			x += 1
			if x in self.surfacegrey:
				a,b,c,d = surface[0],surface[1],surface[2],surface[3]
				a1,a2,a3 = self.vertices[a]
				b1,b2,b3 = self.vertices[b]
				c1,c2,c3 = self.vertices[c]
				d1,d2,d3 = self.vertices[d]

				glTexCoord2f(0,0)
				glVertex3f(a1/3,a2/3,(a3-1)/3)
				glTexCoord2f(0,1)
				glVertex3f(b1/3,b2/3,(b3-1)/3)
				glTexCoord2f(1,1)
				glVertex3f(c1/3,c2/3,(c3-1)/3)
				glTexCoord2f(1,0)
				glVertex3f(d1/3,d2/3,(d3-1)/3)

		glEnd()

		if self.fly:
			surface=self.allsurfaces[42]
			a,b,c,d = surface[0],surface[1],surface[2],surface[3]
			a1,a2,a3 = self.vertices[a]
			b1,b2,b3 = self.vertices[b]
			c1,c2,c3 = self.vertices[c]
			d1,d2,d3 = self.vertices[d]
			a1,a2,a3=a1/3,a2/3,(a3-1)/3
			b1,b2,b3=b1/3,b2/3,(b3-1)/3
			c1,c2,c3=c1/3,c2/3,(c3-1)/3
			d1,d2,d3=d1/3,d2/3,(d3-1)/3
			if self.flysec%4==0: 
				glBindTexture(GL_TEXTURE_2D,screw1_texture.texID)
				a1,b1,c1,d1=a1+0.1,b1+0.1,c1+0.1,d1+0.1
				a3,b3,c3,d3=a3-0.1,b3-0.1,c3-0.1,d3-0.1
			elif self.flysec%4==1:
				glBindTexture(GL_TEXTURE_2D,screw2_texture.texID)
			elif self.flysec%4==2:
				glBindTexture(GL_TEXTURE_2D,screw3_texture.texID)
				a1,b1,c1,d1=a1-0.1,b1-0.1,c1-0.1,d1-0.1
			elif self.flysec%4==3:
				glBindTexture(GL_TEXTURE_2D,screw4_texture.texID)
				a3,b3,c3,d3=a3-0.1,b3-0.1,c3-0.1,d3-0.1
		else:
			glBindTexture(GL_TEXTURE_2D,screw2_texture.texID)
			surface=self.allsurfaces[42]
			a,b,c,d = surface[0],surface[1],surface[2],surface[3]
			a1,a2,a3 = self.vertices[a]
			b1,b2,b3 = self.vertices[b]
			c1,c2,c3 = self.vertices[c]
			d1,d2,d3 = self.vertices[d]
			a1,a2,a3=a1/3,a2/3,(a3-1)/3
			b1,b2,b3=b1/3,b2/3,(b3-1)/3
			c1,c2,c3=c1/3,c2/3,(c3-1)/3
			d1,d2,d3=d1/3,d2/3,(d3-1)/3
		

		glBegin(GL_QUADS)
		glTexCoord2f(0,0)
		glVertex3f(a1,a2,a3)
		glTexCoord2f(0,1)
		glVertex3f(b1,b2,b3)
		glTexCoord2f(1,1)
		glVertex3f(c1,c2,c3)
		glTexCoord2f(1,0)
		glVertex3f(d1,d2,d3)
		glEnd()

		glBindTexture(GL_TEXTURE_2D,black_texture.texID)

		glBegin(GL_QUADS)
		x=0 
		for surface in self.allsurfaces:
			x += 1
			if x in self.surfaceblack:

				a,b,c,d = surface
				a1,a2,a3 = self.vertices[a]
				b1,b2,b3 = self.vertices[b]
				c1,c2,c3 = self.vertices[c]
				d1,d2,d3 = self.vertices[d]

				glTexCoord2f(0,0)
				glVertex3f(a1/3,a2/3,(a3-1)/3)
				glTexCoord2f(0,1)
				glVertex3f(b1/3,b2/3,(b3-1)/3)
				glTexCoord2f(1,1)
				glVertex3f(c1/3,c2/3,(c3-1)/3)
				glTexCoord2f(1,0)
				glVertex3f(d1/3,d2/3,(d3-1)/3)

		glEnd()
		
		glPopMatrix()

		x=0 
		for surface in self.allsurfaces:
			x += 1
			if x in self.surfacegear and not x in self.surfacerotategear:
				if x!=31:
					glPushMatrix()
					
					glBindTexture(GL_TEXTURE_2D,gear_texture.texID)
					glEnable(GL_DEPTH_TEST)
					glBegin(GL_QUADS)

					a,b,c,d = surface
					a1,a2,a3 = self.vertices[a]
					b1,b2,b3 = self.vertices[b]
					c1,c2,c3 = self.vertices[c]
					d1,d2,d3 = self.vertices[d]

					if x in range(1,10):
						a1,b1,c1,d1 = a1-0.1,b1+0.1,c1+0.1,d1-0.1
						a2,b2,c2,d2 = a2+0.1,b2+0.1,c2-0.1,d2-0.1
					if x==39:
						a1,b1,c1,d1 = a1-0.1,b1+0.1,c1+0.1,d1-0.1
						a2,b2,c2,d2 = a2+0.1,b2+0.1,c2-0.1,d2-0.1
						a3,b3,c3,d3 = a3-0.1,b3-0.1,c3-0.1,d3-0.1
					if x in range(10,19):
						a2,b2,c2,d2 = a2+0.1,b2+0.1,c2-0.1,d2-0.1
						a3,b3,c3,d3 = a3+0.1,b3-0.1,c3-0.1,d3+0.1
					if x == 40:
						a1,b1,c1,d1 = a1+0.1,b1-0.1,c1-0.1,d1+0.1
						a2,b2,c2,d2 = a2-0.1,b2-0.1,c2+0.1,d2+0.1
						a3,b3,c3,d3 = a3+0.1,b3+0.1,c3+0.1,d3+0.1
					if x in range(19,28):
						a1,b1,c1,d1 = a1-0.1,b1+0.1,c1+0.1,d1-0.1
						a2,b2,c2,d2 = a2+0.1,b2+0.1,c2-0.1,d2-0.1
					if x == 41:
						a1,b1,c1,d1 = a1-0.1,b1-0.1,c1-0.1,d1-0.1
						a2,b2,c2,d2 = a2+0.1,b2+0.1,c2-0.1,d2-0.1
						a3,b3,c3,d3 = a3+0.1,b3-0.1,c3-0.1,d3+0.1
					if x in range(28,37):
						a2,b2,c2,d2 = a2+0.1,b2+0.1,c2-0.1,d2-0.1
						a3,b3,c3,d3 = a3+0.1,b3-0.1,c3-0.1,d3+0.1

					glTexCoord2f(0,0)
					glVertex3f(a1/3,a2/3,(a3-1)/3)
					glTexCoord2f(0,1)
					glVertex3f(b1/3,b2/3,(b3-1)/3)
					glTexCoord2f(1,1)
					glVertex3f(c1/3,c2/3,(c3-1)/3)
					glTexCoord2f(1,0)
					glVertex3f(d1/3,d2/3,(d3-1)/3)

					glEnd()
					
					glPopMatrix()
		
		glPushMatrix()
		
		glBindTexture(GL_TEXTURE_2D,gear1_texture.texID)
		glEnable(GL_DEPTH_TEST)
		glBegin(GL_QUADS)

		a,b,c,d = self.allsurfaces[31]
		a1,a2,a3 = self.vertices[a]
		b1,b2,b3 = self.vertices[b]
		c1,c2,c3 = self.vertices[c]
		d1,d2,d3 = self.vertices[d]
		a2,b2,c2,d2 = a2+0.1,b2+0.1,c2-0.1,d2-0.1
		a3,b3,c3,d3 = a3+0.1,b3-0.1,c3-0.1,d3+0.1

		glTexCoord2f(0,0)
		glVertex3f(a1/3,a2/3,(a3-1)/3)
		glTexCoord2f(0,1)
		glVertex3f(b1/3,b2/3,(b3-1)/3)
		glTexCoord2f(1,1)
		glVertex3f(c1/3,c2/3,(c3-1)/3)
		glTexCoord2f(1,0)
		glVertex3f(d1/3,d2/3,(d3-1)/3)

		glEnd()
		
		glPopMatrix()

		if self.rotatetimer % 2 == 0:
			gear_texture=Texture("image/gear2.png")
		else:
			gear_texture=Texture("image/gear3.png")

		x=0 
		for surface in self.allsurfaces:
			x += 1
			if x in self.surfacerotategear and x!=31:
				glPushMatrix()
				
				glBindTexture(GL_TEXTURE_2D,gear_texture.texID)
				glBegin(GL_QUADS)

				a,b,c,d = surface
				a1,a2,a3 = self.vertices[a]
				b1,b2,b3 = self.vertices[b]
				c1,c2,c3 = self.vertices[c]
				d1,d2,d3 = self.vertices[d]

				if x in range(1,10):
					a1,b1,c1,d1 = a1-0.1,b1+0.1,c1+0.1,d1-0.1
					a2,b2,c2,d2 = a2+0.1,b2+0.1,c2-0.1,d2-0.1
				if x==39:
					a1,b1,c1,d1 = a1-0.1,b1+0.1,c1+0.1,d1-0.1
					a2,b2,c2,d2 = a2+0.1,b2+0.1,c2-0.1,d2-0.1
					a3,b3,c3,d3 = a3-0.1,b3-0.1,c3-0.1,d3-0.1
				if x in range(10,19):
					a2,b2,c2,d2 = a2+0.1,b2+0.1,c2-0.1,d2-0.1
					a3,b3,c3,d3 = a3+0.1,b3-0.1,c3-0.1,d3+0.1
				if x == 40:
					a1,b1,c1,d1 = a1+0.1,b1-0.1,c1-0.1,d1+0.1
					a2,b2,c2,d2 = a2-0.1,b2-0.1,c2+0.1,d2+0.1
					a3,b3,c3,d3 = a3+0.1,b3+0.1,c3+0.1,d3+0.1
				if x in range(19,28):
					a1,b1,c1,d1 = a1-0.1,b1+0.1,c1+0.1,d1-0.1
					a2,b2,c2,d2 = a2+0.1,b2+0.1,c2-0.1,d2-0.1
				if x == 41:
					a1,b1,c1,d1 = a1-0.1,b1-0.1,c1-0.1,d1-0.1
					a2,b2,c2,d2 = a2+0.1,b2+0.1,c2-0.1,d2-0.1
					a3,b3,c3,d3 = a3+0.1,b3-0.1,c3-0.1,d3+0.1
				if x in range(28,37):
					a2,b2,c2,d2 = a2+0.1,b2+0.1,c2-0.1,d2-0.1
					a3,b3,c3,d3 = a3+0.1,b3-0.1,c3-0.1,d3+0.1
				if x == 42:
					a2,b2,c2,d2 = a2-0.1,b2-0.1,c2-0.1,d2-0.1


				glTexCoord2f(0,0)
				glVertex3f(a1/3,a2/3,(a3-1)/3)
				glTexCoord2f(0,1)
				glVertex3f(b1/3,b2/3,(b3-1)/3)
				glTexCoord2f(1,1)
				glVertex3f(c1/3,c2/3,(c3-1)/3)
				glTexCoord2f(1,0)
				glVertex3f(d1/3,d2/3,(d3-1)/3)

				glEnd()
				
				glPopMatrix()

	def drawWin(self):
		position = (-0.55,-0.9,0)
		font = pygame.font.SysFont("chalkduster",64)
		textSurface = font.render("Level Passed!", True, (255,255,255))
		textData = pygame.image.tostring(textSurface, "RGBA", True)
		glRasterPos3d(*position)
		glLoadIdentity()
		glRotatef(15,-20,0,0)
		glPushMatrix()
		glDrawPixels(textSurface.get_width(), textSurface.get_height(),GL_RGBA, GL_UNSIGNED_BYTE, textData)     
		glPopMatrix()

	def drawmove(self):
		if self.turning % 8 ==0: 
			position1 = (-0.6,0.8,0)
			position2 = (-0.6,0.8,-0.5)
		if self.turning % 8 ==1: 
			position1 = (-0.85,0.64,0)
			position2 = (-0.55,0.62,-0.3)
		if self.turning % 8 ==2: 
			position1 = (0,0.8,-0.6)
			position2 = (0.5,0.8,-0.6)
		if self.turning % 8 ==3: 
			position1 = (0.85,0.96,0)
			position2 = (0.85,0.828,0)
		if self.turning % 8 ==4: 
			position1 = (0.6,0.8,0)
			position2 = (0.6,0.8,0.5)
		if self.turning % 8 ==5: 
			position1 = (0.85,0.64,0)
			position2 = (1.15,0.39,-0.3)
		if self.turning % 8 ==6: 
			position1 = (0,0.8,0.6)
			position2 = (-0.5,0.8,0.6)
		if self.turning % 8 ==7: 
			position1 = (-0.85,0.96,0)
			position2 = (-0.85,0.828,0)
		if self.fly: 
			position1 = (-0.6,0.8,0)
			position2 = (-0.6,0.8,-0.5)

		font = pygame.font.SysFont("chalkduster",30)
		text = "  moves: " + str(self.count) + "    " + self.timetext
		textSurface1 = font.render(text, True, (255,255,255))
		font = pygame.font.SysFont("chalkduster",15)
		text2 = "  Press Esc to Go Back, R to Retry, <- & -> to Rotate"
		textSurface2 = font.render(text2, True, (255,255,255))
		textData1 = pygame.image.tostring(textSurface1, "RGBA", True)
		textData2 = pygame.image.tostring(textSurface2, "RGBA", True)

		glRasterPos3d(*position1)
		glPushMatrix()
		glDrawPixels(textSurface1.get_width(), textSurface1.get_height(),GL_RGBA, GL_UNSIGNED_BYTE, textData1) 
		glPopMatrix()

		glRasterPos3d(*position2)
		glPushMatrix()
		glDrawPixels(textSurface2.get_width(), textSurface2.get_height(),GL_RGBA, GL_UNSIGNED_BYTE, textData2)
		glPopMatrix()

	def mousePresseds(self,x,y):
		global curk1,k1,x1,y1
		global curk2,k2,x2,y2
		global curk3,k3,x3,y3
		global curk4,k4,x4,y4
		global p1,p2,p2_3,p3,p3_3,p4,p4_3

		pos=(x,y)
		k1=isin1(pos)
		if k1 in range(1,10) and not self.win:
			if abs(curk1-k1)==1 or abs(curk1-k1)==3:
				self.count += 1
				effect = pygame.mixer.Sound('sound/slide01.wav')
				effect.play()
				j=(curk1-1)//3
				i=(curk1-1)%3
				x=x1+65*j
				y=y1+65*i
				if k1 in p1:
					p1.remove(k1)
					p1.append(curk1)
					temp = self.gears
					for gear in self.gears:
						if gear.num == k1:
							temp.remove(gear)
					temp.append(Gear(x,y,curk1,0))
					self.gears = temp
				temp = self.tiles
				for tile in self.tiles:
					if tile.num == k1:
						temp.remove(tile)
				temp.append(Tile(x,y,curk1))
				self.tiles = temp
				curk1=k1
			return

		pos=(x,y)
		k2=isin2(pos)
		if k2 in range(10,19) and not self.win:
			if (abs(curk2-k2)==1 or abs(curk2-k2)==3) and (not k2 in p2_3):
				self.count += 1
				effect = pygame.mixer.Sound('sound/slide01.wav')
				effect.play()
				j=(curk2-10)//3
				i=(curk2-10)%3
				x=x2+65*j
				y=y2+65*i
				if k2 in p2:
					p2.remove(k2)
					p2.append(curk2)
					for gear in self.gears:
						if gear.num == k2:
							self.gears.remove(gear)
					self.gears.append(Gear(x,y,curk2,0))
				for tile in self.tiles:
					if tile.num == k2:
						self.tiles.remove(tile)
				self.tiles.append(Tile(x,y,curk2))
				curk2=k2
			return

		pos=(x,y)
		k3=isin3(pos)
		if k3 in range(19,28) and not self.win:
			if (abs(curk3-k3)==1 or abs(curk3-k3)==3) and (not k3 in p3_3):
				self.count += 1
				effect = pygame.mixer.Sound('sound/slide01.wav')
				effect.play()
				j=(curk3-19)//3
				i=(curk3-19)%3
				x=x3+65*j
				y=y3+65*i
				if k3 in p3:
					p3.remove(k3)
					p3.append(curk3)
					for gear in self.gears:
						if gear.num == k3:
							self.gears.remove(gear)
					self.gears.append(Gear(x,y,curk3,0))
				for tile in self.tiles:
					if tile.num == k3:
						self.tiles.remove(tile)
				self.tiles.append(Tile(x,y,curk3))
				curk3=k3
			return

		pos=(x,y)
		k4=isin4(pos)
		if k4 in range(28,37) and not self.win:
			if (abs(curk4-k4)==1 or abs(curk4-k4)==3) and (not k4 in p4_3):
				self.count += 1
				effect = pygame.mixer.Sound('sound/slide01.wav')
				effect.play()
				j=(curk4-28)//3
				i=(curk4-28)%3
				x=x4+65*j
				y=y4+65*i
				if k4 in p4:
					p4.remove(k4)
					p4.append(curk4)
					for gear in self.gears:
						if gear.num == k4:
							self.gears.remove(gear)
					self.gears.append(Gear(x,y,curk4,0))
				for tile in self.tiles:
					if tile.num == k4:
						self.tiles.remove(tile)
				self.tiles.append(Tile(x,y,curk4))
				curk4=k4
			return

	def timercheck(self):
		for gear in self.gears:
			if gear.num == -1: 
				start=gear
				gear.rotate=1
			else:
				gear.rotate=0
				gear.angleSpeed = 0
		self.checkconnect1(start,1)
		if self.checkwin1()!=0: 
			for gear in self.gears:
				if gear.num == -3: 
					start=gear
					gear.rotate=self.checkwin1() * -1
					gear.angleSpeed = gear.rotate * 5
			self.checkconnect2(start,start.rotate)
		if self.checkwin2()!=0:
			for gear in self.gears:
				if gear.num == -5:
					start=gear
					gear.rotate=self.checkwin2() * -1
					gear.angleSpeed = gear.rotate * 5
			self.checkconnect3(start,start.rotate)
		if self.checkwin3()!=0:
			for gear in self.gears:
				if gear.num == -7:
					start=gear
					gear.rotate=self.checkwin3() * -1
					gear.angleSpeed = gear.rotate * 5
			self.checkconnect4(start,start.rotate)
		if not self.win: self.checkwin4()

		#writeFile
		s = ""
		for tile in self.tiles:
			if tile.style != 3: s += str(tile.num)+","
		s += "\n"
		for tile in self.tiles:
			if tile.style == 3: s += str(tile.num)+","
		s += "\n"
		for gear in self.gears:
			if gear.num>0: s += str(gear.num) + ","
		s += "\n"
		s += str(curk1)+","+str(curk2)+","
		s += str(curk3)+","+str(curk4)+"\n"

		for gear in self.gears:
			if gear.rotate != 0: 
				if gear.num == -2: s += "39,"
				elif gear.num == -4: s += "40,"
				elif gear.num == -6: s += "41,"
				elif gear.num == -1: s += "42,"
				else: s += str(gear.num) + ","
		s += "\n"

		if self.win: 
			s += "True"
		else:
			s += "False"
		writeFile("foo.txt",s)
		
		if self.win: pass 
			#self.playing = False

	def checkwin1(self):
		for gear in self.gears:
			if gear.num == -2 and gear.rotate != 0:
				return gear.rotate
		return 0

	def checkwin2(self):
		for gear in self.gears:
			if gear.num == -4 and gear.rotate != 0:
				return gear.rotate
		return 0

	def checkwin3(self):
		for gear in self.gears:
			if gear.num == -6 and gear.rotate != 0:
				return gear.rotate
		return 0
				
	def checkwin4(self):
		for gear in self.gears:
			if gear.num == 32 and gear.rotate != 0:
				self.win = True

				s = readFile("gamepass.txt")
				count = 0 
				new = ""
				for line in s.splitlines():
					if count == 4:
						new += "1\n"
					else:
						new += line + "\n"
					count += 1
				writeFile("gamepass.txt",new)

				effect = pygame.mixer.Sound('sound/puzzleDone.wav')
				effect.play()

	def checkconnect1(self,start,rotation):
		if start.num == -1:
			for gear in self.gears:
				if gear.num==6:
					gear.rotate = -1
					gear.angleSpeed = -5
					self.checkconnect1(gear,-1)
		else:
			for gear in self.gears:
				if gear.num in range(1,10) or gear.num == -2:
					n1,n2=start.num,gear.num
					row1,row2 = (n1-1)//3, (n2-1)//3
					if ((abs(n1-n2)==1) and (row1==row2)) or abs(n1-n2)==3 or ((n1==8) and (n2==-2)):
						if gear.rotate==0:
							rotation *= (-1)
							gear.rotate = rotation
							gear.angleSpeed = gear.rotate * 5
							self.checkconnect1(gear,rotation)

	def checkconnect2(self,start,rotation):
		if start.num == -3:
			for gear in self.gears:
				if gear.num==11:
					gear.rotate = -1
					gear.angleSpeed = -5
					self.checkconnect2(gear,-1)
		else:
			for gear in self.gears:
				if (gear.num>9) and (gear.num<19) or gear.num==-4:
					n1,n2=start.num,gear.num
					row1,row2 = (n1-1)//3, (n2-1)//3
					if ((abs(n1-n2)==1) and (row1==row2)) or abs(n1-n2)==3 or ((n1==17) and (n2==-4)):
						if gear.rotate==0:
							rotation *= (-1)
							gear.rotate = rotation
							gear.angleSpeed = gear.rotate * 5
							self.checkconnect2(gear,rotation)

	def checkconnect3(self,start,rotation):
		if start.num == -5:
			for gear in self.gears:
				if gear.num==26:
					gear.rotate = -1
					gear.angleSpeed = -5
					self.checkconnect3(gear,-1)
		else:
			for gear in self.gears:
				if (gear.num>18) and (gear.num<28) or gear.num==-6:
					n1,n2=start.num,gear.num
					row1,row2 = (n1-1)//3, (n2-1)//3
					if ((abs(n1-n2)==1) and (row1==row2)) or abs(n1-n2)==3 or ((n1==20) and (n2==-6)):
						if gear.rotate==0:
							rotation *= (-1)
							gear.rotate = rotation
							gear.angleSpeed = gear.rotate * 5
							self.checkconnect3(gear,rotation)

	def checkconnect4(self,start,rotation):
		if start.num == -7:
			for gear in self.gears:
				if gear.num==35:
					gear.rotate = -1
					gear.angleSpeed = -5
					self.checkconnect4(gear,-1)
		else:
			for gear in self.gears:
				if (gear.num>27) or gear.num==32:
					n1,n2=start.num,gear.num
					row1,row2 = (n1-1)//3, (n2-1)//3
					if ((abs(n1-n2)==1) and (row1==row2)) or abs(n1-n2)==3 or ((n1==35) and (n2==32)):
						if gear.rotate==0:
							rotation *= (-1)
							gear.rotate = rotation
							gear.angleSpeed = gear.rotate * 5
							self.checkconnect4(gear,rotation)

	def running(self):
		self.init()
		display = (800,600)
		pygame.display.set_mode(display,DOUBLEBUF|OPENGL)

		glRotatef(15,-20,0,0)
		self.playing = True
		self.turning = 800
		self.fly = False
		self.count = 0
		self.sec = 0 
		self.min = 0
		self.timetext = "TIME : 0:00"

		self.rotatetimer = 0

		while self.playing:
			#glClearColor(255,255,255,1)
			self.rotatetimer += 1
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RIGHT:
						glRotatef(45,0,45,0)
						self.turning += 1
					if event.key == pygame.K_LEFT:
						glRotatef(45,0,-45,0)
						self.turning -= 1
					if event.key == pygame.K_r:
						self.init(800,600,-1)
					if event.key == pygame.K_ESCAPE:
						self.playing = False
				if event.type == pygame.MOUSEBUTTONDOWN:
					x,y = (event.pos)
					if self.turning%8 == 0:
						x = int((x-265)*65/90 + 120)
						y = int((y-250) + 45)
					if self.turning%8 == 2:
						x = int((x-130)*65/90 + 445)
						y = int((y-225) + 45)
					if self.turning%8 == 4:
						x = 800-x
						y = 600-y
						x = int((x-265)*65/90 + 445)
						y = int((y-200) + 350)
					if self.turning%8 == 6:
						x = int((x-400)*65/90 + 120)
						y = int((y-225) + 345)
						x = 435-x
						y = 890-y
					
					self.mousePresseds(x,y)

			s=readFile("foo.txt")
			temp,self.surfaces = s.splitlines()[0],[]
			for element in temp.split(","):
				if element!="": self.surfaces += [int(element)]

			temp,self.surfacegrey = s.splitlines()[1],[]
			for element in temp.split(","):
				if element!="": self.surfacegrey += [int(element)]
			self.surfacegrey += [37,38]

			self.surfacescrew = [43]

			temp,self.surfacegear = s.splitlines()[2],[]
			for element in temp.split(","):
				if element!="": self.surfacegear += [int(element)]
			self.surfacegear += [39,40,41,42]

			temp,self.surfaceblack = s.splitlines()[3],[]
			for element in temp.split(","):
				if element!="": self.surfaceblack += [int(element)]

			temp,self.surfacerotategear = s.splitlines()[4],[42]
			for element in temp.split(","):
				if element!="": self.surfacerotategear += [int(element)]

			self.Cube()
			self.drawmove()

			if s.splitlines()[5] == "True": 
				self.fly = True
				self.drawWin()

			if not self.fly: self.sec += 10
			if self.fly: 
				effect = pygame.mixer.Sound("sound/wheel.wav")
				effect.play()
				effect.set_volume(0.3)
				self.flysec += 1

			if self.sec >= 6000:
				self.sec = 0
				self.min += 1

			if self.sec%100 == 0 :
				if (self.sec//100) < 10:
					self.timetext = "TIME : " + str(self.min) + ":0" + str(self.sec//100)	
				else:
					self.timetext = "TIME : " + str(self.min) + ":" + str(self.sec//100)

			pygame.display.flip()
			self.timercheck()

#Game3demo(800,600).running()













