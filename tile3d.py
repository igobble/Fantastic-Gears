
import pygame
from GameObject import GameObject

class Tile():
	@staticmethod
	def init():
		pass

	def __init__(self,x,y,num,style=2):
		#if style == 2:
	#		image = pygame.image.load("image/tile2.png").convert_alpha()
	#	if style == 3:
	#		image = pygame.image.load("image/tile3.png").convert_alpha()
	#	w,h = image.get_size()
	#	image = pygame.transform.scale(image, (66, 66))
	#	super(Tile,self).__init__(x,y,image,w/2)
		self.x = x
		self.y = y
		self.num = num
		self.style = style


	def update(self,width,height):
		pass

