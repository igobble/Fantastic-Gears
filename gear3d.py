import pygame
from GameObject import GameObject

class Gear():
	@staticmethod
	def init():
		pass

	def __init__(self,x,y,num,rotate):
		#image = pygame.image.load("image/gear2.png").convert_alpha()
		#w,h = image.get_size()
		#image = pygame.transform.scale(image, (84,84))
		#super(Gear,self).__init__(x,y,image,w/2)
		self.x = x
		self.y = y
		self.num = num
		self.rotate = rotate
		if rotate == 0: self.angleSpeed = 0
		if rotate == 1: self.angleSpeed = 5
		if rotate == -1: self.angleSpeed = -5

	#def update(self,width,height):
		#self.angle += self.angleSpeed
		#super(Gear, self).update(width,height)
