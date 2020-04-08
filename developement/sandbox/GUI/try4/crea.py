import pygame
from pygame.locals import *

class image():

	def __init__(self,chemin):
		self.image=pygame.image.load(chemin).convert_alpha()
		self.pos=self.image.get_rect()

class maketext():

	def __init__(self,txt,color,fontsize):
		self.text=txt
		self.font=pygame.font.Font(None,fontsize)
		self.size=self.font.size(self.text)
		self.ren=self.font.render(self.text,0,color)