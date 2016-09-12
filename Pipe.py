
import pygame
from GameObject import GameObject

class Pipe(GameObject):
	@staticmethod
	def init():
		pass

	def __init__(self,x,y,num,style):
		if style == 1:
			image = pygame.image.load("image/pipe1-2.png").convert_alpha()
		if style == 2:
			image = pygame.image.load("image/pipe2-2.png").convert_alpha()
		if style == 3:
			image = pygame.image.load("image/pipe3-2.png").convert_alpha()
		if style == 4:
			image = pygame.image.load("image/pipe4-2.png").convert_alpha()
		if style == 5:
			image = pygame.image.load("image/pipe5-2.png").convert_alpha()
		if style == 6:
			image = pygame.image.load("image/pipe6-2.png").convert_alpha()
		if style == 7:
			image = pygame.image.load("image/pipe7.png").convert_alpha()

		w,h = image.get_size()

		image = pygame.transform.scale(image, (66, 66))
		super(Pipe,self).__init__(x,y,image,w/2)
		self.num = num
		self.style = style
		self.steam = False
		if style == 7:
			self.entrance1 = 0
			self.entrance2 = 0
			self.entrance3 = 0

	def update(self,width,height):
		pass

