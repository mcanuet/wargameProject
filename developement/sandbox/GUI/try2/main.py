import pygame
from pygame.locals import *
from crea import *

if __name__=="__main__":
	
	#-------initialisateur (package)
	pygame.init()
	pygame.mixer.init()
	pygame.font.init()

	#---création de la fenêtre
	fen=pygame.display.set_mode((1200,680))

	#---liste des fenêtre
	screen1=True

	#---couleurs
	white=(255,255,255)

	fondgrille=image("img/grille.png")
	fondgrille.pos=fondgrille.pos.move(10,60)
	text=maketext("",white,24)

	# run the game loop
	while screen1:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()

			if event.type==MOUSEBUTTONUP:
				pos=event.pos
				
				if fondgrille.pos.collidepoint(pos):
					x,y=(pos[0]-10)//30,(pos[1]-60)//30
					text=maketext(str((x,y)),white,24)
					print(x,y)

		fen.fill(pygame.Color("black"))
		fen.blit(text.ren,(10,20))
		fen.blit(fondgrille.image,fondgrille.pos)
		pygame.display.update()
