import pygame
from pygame.locals import *

contenuArmees=[]
Victory=False
Tours=0
typeJoueurs=["",""]

class image():

	def __init__(self,chemin):
		self.image=pygame.image.load(chemin).convert_alpha()
		self.pos=self.image.get_rect()

class maketext():

	def __init__(self,txt,color,fontsize):
		self.text=txt
		self.font=pygame.font.Font("ressources/font/asgard.ttf",fontsize)
		self.size=self.font.size(self.text)
		self.ren=self.font.render(self.text,0,color)

class sound():

	def __init__(self,chemin):
		self.son=pygame.mixer.Sound(chemin)

#--- couleur 
black=(0,0,0)
white=(255,255,255)
red=(255, 102, 102)
green=(0,255,0)
blue=(153, 153, 255)
grey=(120,120,120)
trueRed=(255,0,0)

#-------initialisateur (package pygame)
pygame.init()
pygame.mixer.init()
pygame.font.init()


class MainScreen(object):

	def __init__(self):
		self.fen=pygame.display.set_mode((1200,680))
		self.title=pygame.display.set_caption("faquin's war")
		bkg=image("ressources/img/fond.png")
		self.fen.blit(bkg.image,bkg.pos)

if __name__=="__main__":

	while not Victory:
		MainScreen()