import pygame

class GameObject(pygame.sprite.Sprite):
	def __init__(self,x,y,image,radius):
		super(GameObject,self).__init__()

		self.x=x
		self.y=y
		self.image=image
		self.radius = radius

		self.baseImage = image.copy()

		w,h = image.get_size()

		self.updateRect()
		self.velocity = (0,0)
		self.angle=0

	def updateRect(self):
		w,h = self.image.get_size()
		self.width,self.height = w,h
		self.rect = pygame.Rect(self.x-w/2, self.y-h/2, w, h)

	def update(self, width, height):
		self.image = pygame.transform.rotate(self.baseImage,self.angle)
		dx,dy = self.velocity
		self.x += dx
		self.y += dy

		self.updateRect()