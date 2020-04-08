#Import classique
import pygame
from pygame.locals import *

#Pour ajouter le dossier parent dans le Path et pouvoir tout importer
import sys
sys.path.append('../')

#Nouveux imports
from gui.crea import *

pygame.init()

fen=pygame.display.set_mode((1200,680))
pygame.display.set_caption('grille')



def affichegrille(fen):

	decal=20
	taillecase=30

	fondgr=pygame.draw.rect(fen,white,(decal,decal,600,600))

	i=0
	while i<=600 :
		pygame.draw.line(fen,black,(decal,i+decal),(600+decal,i+decal))
		pygame.draw.line(fen,black,(decal+i,decal),(i+decal,600+decal))
		i+=taillecase


	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()

			if event.type==MOUSEBUTTONUP:
					pos=event.pos
					
					if fondgr.collidepoint(pos):
						x,y=(pos[0]-decal)//taillecase,(pos[1]-decal)//taillecase
						text=maketext(str((x,y)),white,24)
						print(x,y)

		pygame.display.update()
