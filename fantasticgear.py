#home interface

import pygame
from game1 import Game1
from game2 import Game2
from game3demo import Game3demo
from game4 import Game4
from game5 import Game5
from game6 import Game6
from game7 import Game7
from game8 import Game8
from game1timing import Game1timing
from game2timing import Game2timing
from game4timing import Game4timing
from game7timing import Game7timing
from game1move import Game1move
from game4move import Game4move
from game5move import Game5move
from game7move import Game7move

mode="home"
mute=-1

def mousePressed(x,y):
	effect = pygame.mixer.Sound('sound/buttonPress.wav')
	effect.play()
	global mode,mute
	if x>=720 and x<=770 and y>=520 and y<=570: mute *= (-1)
	if x>=15 and x<=75 and y>=520 and y<=560: 
		if mode in "adventurechallengehelp":
			mode = "home"
		if mode=="timechallenge" or mode=="movechallenge":
			mode = "challenge"
	if mode == "adventure":
		if x>=90 and x<=290 and y>=240 and y<=300: return 1
		if x>=90 and x<=290 and y>=330 and y<=390: return 2
		if x>=90 and x<=290 and y>=420 and y<=480: return 4
		if x>=90 and x<=290 and y>=510 and y<=570: return 3
		if x>=300 and x<=500 and y>=240 and y<=300: return 5
		if x>=350 and x<=500 and y>=330 and y<=390: return 6
		if x>=350 and x<=500 and y>=420 and y<=480: return 7
		if x>=350 and x<=500 and y>=510 and y<=570: return 8


	if mode == "home":
		if x>=250 and x<=550 and y>=240 and y<=320: return -1
		if x>=250 and x<=550 and y>=340 and y<=420: return -2
		if x>=250 and x<=550 and y>=440 and y<=520: return -3

	if mode == "challenge":
		if x>=250 and x<=550 and y>=280 and y<=360: return -4
		if x>=250 and x<=550 and y>=380 and y<=460: return -5

	if mode == "timechallenge":
		if x>=90 and x<=340 and y>=240 and y<=300: return 11
		if x>=450 and x<=700 and y>=240 and y<=300: return 12
		if x>=90 and x<=340 and y>=420 and y<=480: return 13
		if x>=450 and x<=700 and y>=420 and y<=480: return 14

	if mode == "movechallenge":
		if x>=90 and x<=340 and y>=240 and y<=300: return 15
		if x>=450 and x<=700 and y>=240 and y<=300: return 16
		if x>=90 and x<=340 and y>=420 and y<=480: return 17
		if x>=450 and x<=700 and y>=420 and y<=480: return 18

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

def main():
	screen = pygame.display.set_mode((800,600))

	s="1\n"
	for i in range(7):
		s += "0\n"
	writeFile("gamepass.txt",s)

	pygame.init()
	playing = True

	while playing:

		gamepass = readFile("gamepass.txt")

		global mode,mute

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if (event.type == pygame.KEYDOWN):
				if event.key == pygame.K_ESCAPE:
					if mode == "adventure" or mode == "challenge" or mode == "help":
						mode = "home"
					elif mode == "timechallenge" or mode == "movechallenge":
						mode = "challenge"
			if (event.type == pygame.MOUSEBUTTONDOWN):
				modenum = mousePressed(*(event.pos))
				if modenum == 1:
					mode = "game1"
					gearsound = pygame.mixer.Sound('sound/gear1.wav')
					gearsound.play(-1)
					Game1(800,600).run()
					gearsound.stop()
					mode = "adventure"
				if modenum == 2:
					mode = "game2"
					if gamepass.splitlines()[1] == "1":
						Game2(800,600).run()
					pygame.mixer.music.stop()
					mode = "adventure"
				if modenum == 3:
					mode = "game3"
					gearsound = pygame.mixer.Sound('sound/gear1.wav')
					gearsound.play(-1)
					if gamepass.splitlines()[3] == "1":
						Game3demo(800,600).running()
					gearsound.stop()
					pygame.mixer.music.stop()
					mode = "adventure"
					screen = pygame.display.set_mode((800,600))
				if modenum == 4:
					mode = "game4"
					if gamepass.splitlines()[2] == "1":
						Game4(800,600).run()
					pygame.mixer.music.stop()
					mode = "adventure"
				if modenum == 5:
					mode = "game5"
					if gamepass.splitlines()[4] == "1":
						Game5(800,600).run()
					mode = "adventure"
				if modenum == 6:
					mode = "game6"
					if gamepass.splitlines()[5] == "1":
						Game6(800,600).run()
					mode = "adventure"
				if modenum == 7:
					mode = "game7"
					if gamepass.splitlines()[6] == "1":
						Game7(800,600).run()
					mode = "adventure"
				if modenum == 8:
					mode = "game8"
					if gamepass.splitlines()[7] == "1":
						Game8(800,600).run()
					mode = "adventure"
				if modenum == 11:
					mode = "game1timing"
					gearsound = pygame.mixer.Sound('sound/gear1.wav')
					gearsound.play(-1)
					Game1timing(800,600).run()
					gearsound.stop()
					mode = "timechallenge"
				if modenum == 12:
					mode = "game2timing"
					if gamepass.splitlines()[1] == "1":
						Game2timing(800,600).run()
					pygame.mixer.music.stop()
					mode = "timechallenge"
				if modenum == 13:
					mode = "game4timing"
					if gamepass.splitlines()[2] == "1": 
						Game4timing(800,600).run()
					pygame.mixer.music.stop()
					mode = "timechallenge"
				if modenum == 14:
					mode = "game7timing"
					if gamepass.splitlines()[6] == "1":
						Game7timing(800,600).run()
					mode = "timechallenge"
				if modenum == 15:
					mode = "game1move"
					gearsound = pygame.mixer.Sound('sound/gear1.wav')
					gearsound.play(-1)
					Game1move(800,600).run()
					gearsound.stop()
					mode = "movechallenge"
				if modenum == 16:
					mode = "game5move"
					if gamepass.splitlines()[4] == "1":
						Game5move(800,600).run()
					mode = "movechallenge"
				if modenum == 17:
					mode = "game4move"
					if gamepass.splitlines()[2] == "1":
						Game4move(800,600).run()
					pygame.mixer.music.stop()
					mode = "movechallenge"
				if modenum == 18:
					mode = "game7move"
					if gamepass.splitlines()[6] == "1":
						Game7move(800,600).run()
					mode = "movechallenge"
				if modenum == -1: mode = "adventure"		
				if modenum == -2: mode = "challenge"
				if modenum == -3: mode = "help"	
				if modenum == -4: mode = "timechallenge"
				if modenum == -5: mode = "movechallenge"

		image = pygame.image.load("image/bg2.png").convert_alpha()
		image = pygame.transform.scale(image, (800,600))
		screen.blit(image, (0,0))

		if mode != "home":
			font = pygame.font.SysFont("arial", 30)
			text = font.render("Back", True, (255,255,255))
			screen.blit(text,(15,520))

		if mute == 1 and mode in "homeadventuretimechallengemovechallengehelp": 
			image = pygame.image.load("image/mute.png").convert_alpha()
			image = pygame.transform.scale(image, (50,50))
			screen.blit(image, (720,520))
		else:
			image = pygame.image.load("image/audio.png").convert_alpha()
			image = pygame.transform.scale(image, (50,50))
			screen.blit(image, (720,520))				

		titlefont = pygame.font.SysFont("comicsansms", 80)
		font = pygame.font.SysFont("comicsansms", 25)

		text = titlefont.render("Fantastic Gears", True, (255,255,255))
		screen.blit(text,(100,100))

		if mode == "help":
			image = pygame.image.load("image/tutor1.png").convert_alpha()
			image = pygame.transform.scale(image, (300,300))
			screen.blit(image, (100,220))
			
			image = pygame.image.load("image/tutor2.png").convert_alpha()
			image = pygame.transform.scale(image, (300,300))
			screen.blit(image, (420,220))
		if mode == "home":
			font = pygame.font.SysFont("comicsansms", 45)
			text = font.render("Adventure", True, (0, 0, 0))
			image = pygame.image.load("image/board1.png").convert_alpha()
			image = pygame.transform.scale(image, (300,80))
			screen.blit(image, (250,240))
			screen.blit(text,(280,245))
			
			font = pygame.font.SysFont("comicsansms", 40)
			text = font.render("Challenge", True, (0, 0, 0))
			image = pygame.image.load("image/board1.png").convert_alpha()
			image = pygame.transform.scale(image, (300,80))
			screen.blit(image, (250,340))
			screen.blit(text,(308,345))

			font = pygame.font.SysFont("comicsansms", 45)
			text = font.render("Help", True, (0, 0, 0))
			image = pygame.image.load("image/board1.png").convert_alpha()
			image = pygame.transform.scale(image, (300,80))
			screen.blit(image, (250,440))
			screen.blit(text,(340,445))

		if mode == "challenge":
			font = pygame.font.SysFont("comicsansms", 45)
			text = font.render("Timing", True, (0, 0, 0))
			image = pygame.image.load("image/board1.png").convert_alpha()
			image = pygame.transform.scale(image, (300,80))
			screen.blit(image, (250,280))
			screen.blit(text,(320,285))
			
			font = pygame.font.SysFont("comicsansms", 40)
			text = font.render("Moves", True, (0, 0, 0))
			image = pygame.image.load("image/board1.png").convert_alpha()
			image = pygame.transform.scale(image, (300,80))
			screen.blit(image, (250,380))
			screen.blit(text,(330,385))

		if mode == "timechallenge":
			pygame.draw.rect(screen, (255,255,255), pygame.Rect(90,240,250,60))
			text = font.render("Timing: Gears", True, (0, 0, 0))
			image = pygame.image.load("image/board1.png").convert_alpha()
			image = pygame.transform.scale(image, (250,60))
			screen.blit(image, (90,240))
			screen.blit(text,(120,245))

			pygame.draw.rect(screen, (255,255,255), pygame.Rect(450,240,250,60))
			text = font.render("Timing: Pipe", True, (0, 0, 0))
			image = pygame.image.load("image/board1.png").convert_alpha()
			image = pygame.transform.scale(image, (250,60))
			screen.blit(image, (450,240))
			screen.blit(text,(480,245))
			if gamepass.splitlines()[1] == "0":
				image = pygame.image.load("image/lock.png").convert_alpha()
				image = pygame.transform.scale(image, (60,60))
				screen.blit(image,(540,240))

			pygame.draw.rect(screen, (255,255,255), pygame.Rect(90,420,250,60))
			text = font.render("Timing: Gear & Pipe", True, (0, 0, 0))
			image = pygame.image.load("image/board1.png").convert_alpha()
			image = pygame.transform.scale(image, (250,60))
			screen.blit(image, (90,420))
			screen.blit(text,(100,425))
			if gamepass.splitlines()[2] == "0":
				image = pygame.image.load("image/lock.png").convert_alpha()
				image = pygame.transform.scale(image, (60,60))
				screen.blit(image,(180,420))

			pygame.draw.rect(screen, (255,255,255), pygame.Rect(450,420,250,60))
			text = font.render("Timing: Leak", True, (0, 0, 0))
			image = pygame.image.load("image/board1.png").convert_alpha()
			image = pygame.transform.scale(image, (250,60))
			screen.blit(image, (450,420))
			if gamepass.splitlines()[6] == "0":
				image = pygame.image.load("image/lock.png").convert_alpha()
				image = pygame.transform.scale(image, (60,60))
				screen.blit(image,(540,420))
			screen.blit(text,(480,425))

		if mode == "movechallenge":
			pygame.draw.rect(screen, (255,255,255), pygame.Rect(90,240,250,60))
			text = font.render("Moves: Gears", True, (0, 0, 0))
			image = pygame.image.load("image/board1.png").convert_alpha()
			image = pygame.transform.scale(image, (250,60))
			screen.blit(image, (90,240))
			screen.blit(text,(120,245))

			pygame.draw.rect(screen, (255,255,255), pygame.Rect(450,240,250,60))
			text = font.render("Moves: Wiggle", True, (0, 0, 0))
			image = pygame.image.load("image/board1.png").convert_alpha()
			image = pygame.transform.scale(image, (250,60))
			screen.blit(image, (450,240))
			screen.blit(text,(480,245))
			if gamepass.splitlines()[4] == "0":
				image = pygame.image.load("image/lock.png").convert_alpha()
				image = pygame.transform.scale(image, (60,60))
				screen.blit(image,(540,240))

			pygame.draw.rect(screen, (255,255,255), pygame.Rect(90,420,250,60))
			text = font.render("Moves: Gear & Pipe", True, (0, 0, 0))
			image = pygame.image.load("image/board1.png").convert_alpha()
			image = pygame.transform.scale(image, (250,60))
			screen.blit(image, (90,420))
			screen.blit(text,(100,425))
			if gamepass.splitlines()[2] == "0":
				image = pygame.image.load("image/lock.png").convert_alpha()
				image = pygame.transform.scale(image, (60,60))
				screen.blit(image,(180,420))

			pygame.draw.rect(screen, (255,255,255), pygame.Rect(450,420,250,60))
			text = font.render("Moves: Leak", True, (0, 0, 0))
			image = pygame.image.load("image/board1.png").convert_alpha()
			image = pygame.transform.scale(image, (250,60))
			screen.blit(image, (450,420))
			if gamepass.splitlines()[6] == "0":
				image = pygame.image.load("image/lock.png").convert_alpha()
				image = pygame.transform.scale(image, (60,60))
				screen.blit(image,(540,420))
			screen.blit(text,(480,425))
		if mode == "adventure":
			#pygame.draw.rect(screen, (255,255,255), pygame.Rect(90,240,250,60))
			font = pygame.font.SysFont("comicsansms", 25)
			text = font.render("Level 1: Gears", True, (0, 0, 0))
			image = pygame.image.load("image/board1.png").convert_alpha()
			image = pygame.transform.scale(image, (200,60))
			screen.blit(image, (90,240))
			screen.blit(text,(115,250))

			#pygame.draw.rect(screen, (255,255,255), pygame.Rect(90,330,250,60))
			text = font.render("Level 2: Pipe", True, (0, 0, 0))
			image = pygame.image.load("image/board1.png").convert_alpha()
			image = pygame.transform.scale(image, (200,60))
			screen.blit(image, (90,330))
			if gamepass.splitlines()[1] == "0":
				image = pygame.image.load("image/lock.png").convert_alpha()
				image = pygame.transform.scale(image, (60,60))
				screen.blit(image,(175,330))
			screen.blit(text,(102,340))

			#pygame.draw.rect(screen, (255,255,255), pygame.Rect(90,420,250,60))
			font = pygame.font.SysFont("comicsansms", 20)
			text = font.render("Level 3: Gear & Pipe", True, (0, 0, 0))
			image = pygame.image.load("image/board1.png").convert_alpha()
			image = pygame.transform.scale(image, (200,60))
			screen.blit(image, (90,420))
			if gamepass.splitlines()[2] == "0":
				image = pygame.image.load("image/lock.png").convert_alpha()
				image = pygame.transform.scale(image, (60,60))
				screen.blit(image,(175,420))
			screen.blit(text,(100,435))

			#pygame.draw.rect(screen, (255,255,255), pygame.Rect(90,510,250,60))
			text = font.render("Level 4: Dimension", True, (0, 0, 0))
			image = pygame.image.load("image/board1.png").convert_alpha()
			image = pygame.transform.scale(image, (200,60))
			screen.blit(image, (90,510))
			if gamepass.splitlines()[3] == "0":
				image = pygame.image.load("image/lock.png").convert_alpha()
				image = pygame.transform.scale(image, (60,60))
				screen.blit(image,(175,510))
			screen.blit(text,(100,525))

			#pygame.draw.rect(screen, (255,255,255), pygame.Rect(450,240,250,60))
			font = pygame.font.SysFont("comicsansms", 25)
			text = font.render("Level 5: Wiggle", True, (0, 0, 0))
			image = pygame.image.load("image/board1.png").convert_alpha()
			image = pygame.transform.scale(image, (200,60))
			screen.blit(image, (300,240))
			screen.blit(text,(315,250))
			if gamepass.splitlines()[4] == "0":
				image = pygame.image.load("image/lock.png").convert_alpha()
				image = pygame.transform.scale(image, (60,60))
				screen.blit(image,(375,240))

			#pygame.draw.rect(screen, (255,255,255), pygame.Rect(450,330,250,60))
			text = font.render("Level 6: Balloon", True, (0, 0, 0))
			image = pygame.image.load("image/board1.png").convert_alpha()
			image = pygame.transform.scale(image, (200,60))
			screen.blit(image, (300,330))
			screen.blit(text,(315,340))
			if gamepass.splitlines()[5] == "0":
				image = pygame.image.load("image/lock.png").convert_alpha()
				image = pygame.transform.scale(image, (60,60))
				screen.blit(image,(375,330))

			#pygame.draw.rect(screen, (255,255,255), pygame.Rect(450,420,250,60))
			text = font.render("Level 7: Leak", True, (0, 0, 0))
			image = pygame.image.load("image/board1.png").convert_alpha()
			image = pygame.transform.scale(image, (200,60))
			screen.blit(image, (300,420))
			if gamepass.splitlines()[6] == "0":
				image = pygame.image.load("image/lock.png").convert_alpha()
				image = pygame.transform.scale(image, (60,60))
				screen.blit(image,(375,420))
			screen.blit(text,(325,430))

			#pygame.draw.rect(screen, (255,255,255), pygame.Rect(450,510,250,60))
			font = pygame.font.SysFont("comicsansms", 20)
			text = font.render("Level 8: Two Sides", True, (0, 0, 0))
			image = pygame.image.load("image/board1.png").convert_alpha()
			image = pygame.transform.scale(image, (200,60))
			screen.blit(image, (300,510))
			screen.blit(text,(310,520))
			if gamepass.splitlines()[7] == "0":
				image = pygame.image.load("image/lock.png").convert_alpha()
				image = pygame.transform.scale(image, (60,60))
				screen.blit(image,(375,510))

		x,y = pygame.mouse.get_pos()
		if mode == "adventure":
			instruction = 0
			if x>=90 and x<=290 and y>=240 and y<=300: instruction=1
			if x>=90 and x<=290 and y>=330 and y<=390: instruction=2
			if x>=90 and x<=290 and y>=420 and y<=480: instruction=3
			if x>=90 and x<=290 and y>=510 and y<=570: instruction=4
			if x>=300 and x<=500 and y>=240 and y<=300: instruction=2
			if x>=300 and x<=500 and y>=330 and y<=390: instruction=6
			if x>=300 and x<=500 and y>=420 and y<=480: instruction=7
			if x>=300 and x<=500 and y>=510 and y<=570: instruction=8
			if instruction!=0: 
				instructionstring = "image/instruction"+str(instruction)+".png"
				image = pygame.image.load(instructionstring).convert_alpha()

				image = pygame.transform.scale(image, (300,280))
				screen.blit(image, (500,240))


		pygame.display.flip()

#main()
