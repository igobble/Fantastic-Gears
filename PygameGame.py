###pygamegame

import pygame

class PygameGame(object):
	def init(self):
		self.playing = True

	def mousePressed(self,x,y):
		pass

	def mouseReleased(self,x,y):
		pass

	def mouseMotion(self,x,y):
		pass

	def mouseDrag(self,x,y):
		pass

	def keyPressed(self,keyCode,modifier):
		if keyCode == pygame.K_ESCAPE:
			self.playing = False


	def keyReleased(self,keyCode,modifier):
		pass

	def timerFired(self,dt):
		pass

	def redrawAll(self,screen):
		pass

	def isKeyPressed(self,key):
		pass

	def __init__(self,width=800,height=600,fps=20):
		self.width = width
		self.height = height
		self.fps = fps
		self.bgColor = (0,0,0)
		pygame.init()

	def run(self):
		clock = pygame.time.Clock()
		screen = pygame.display.set_mode((self.width,self.height))

		self.init()
		
		while self.playing:
			time = clock.tick(self.fps)
			self.timerFired(time)
			for event in pygame.event.get():
				if (event.type == pygame.MOUSEBUTTONDOWN):
					self.mousePressed(*(event.pos))
				elif event.type == pygame.KEYDOWN:
					self.keyPressed(event.key, event.mod)
			screen.fill(self.bgColor)
			self.redrawAll(screen)
			pygame.display.flip()

def main():
	game = PygameGame()
	game.run()

if __name__ == '__main__':
	main()


