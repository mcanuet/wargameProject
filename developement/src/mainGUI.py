from random import *
from time import *
import pygame
from pygame.locals import *

##Anciens imports
#from plateau import *
#from Astar import *
#from unite import *
#from interface import *
#from bebeBeel import *
#from GUIfunc import *
#from crea import *

##Nouveaux imports
from wargame.plateau import *
from algorithmes.Astar import *
from ia.bebeBeel import *
from wargame import unite
##from gui import interface
##from gui import GUIfunc
##from gui import crea
from gui import *


#________________________fonction de jeux___________________________

def creaArmee(typeJoueur):
	for i in typeJoueur:
		if i=="humain":
			#--- choix race
			raceScreenON=True
			while raceScreenON:
				race=GUIfunc.raceScreen(fen)
				if type(race)==str:
					A=unite.Armee(race)
					raceScreenON=False
			uniteScreenON=True
			while uniteScreenON:
				listeUnite=GUIfunc.uniteScreen(race,A.solde,fen)
				if type(listeUnite)==list:
					if listeUnite[-1]=="stop":
						uniteScreenON=False

			for i in listeUnite:
				if i != "stop":
					unite.addUnite(A,i,dicoref)

			contenuArmees.append(A)


		elif i=="IA0" :#test le numéro d'AI pour savoir quel méthode utiliser
				contenuArmees.append(bebeBeel.creationArmee())

#________________________lacement du jeux_________________________
if __name__=="__main__":

	#-------variables globales
	contenuArmees=[]
	Victory=False
	Tours=0
	p=Plateau(20,20)
	typeJoueurs=["",""]
	dicoref=unite.Dicoref()
	t=time()

	#-------initialisateur (package pygame)
	pygame.init()
	pygame.mixer.init()
	pygame.font.init()

	#---création de la fenêtre
	fen=pygame.display.set_mode((1200,680))
	pygame.display.set_caption("faquin's war")

	#--- écran 1
	launch=True
	if launch:
		launch=GUIfunc.launchScreen(launch,fen)

	#--- écran 2
	playerTypeChoice=True
	while playerTypeChoice:
		res=GUIfunc.playerTypeChoiceScreen(True,fen)
		if type(res)==tuple:
			playerTypeChoice=res[0]
			typeJoueurs=res[1]

	#--- écran 3
	creaArmee(typeJoueurs)

	#début du jeux, placement des pions
	GUIfunc.afficheGrille(fen,contenuArmees)
	for i in range(2):
		if typeJoueurs[i]=="humain":
			p=GUIfunc.placePionts(fen,contenuArmees,p,i)

		elif typeJoueurs[i]=="IA0":
			bebeBeel.placerUnites(p,i,contenuArmees)

	GUIfunc.afficheGrille(fen,contenuArmees)

	#jeux avec phase de déplacement et phase d'attaque
	while contenuArmees[0].compo != {} and contenuArmees[1].compo != {}:
		print("Tour n°"+str(Tours))

		if Tours%2==0:
			#remise à zero des déplacement et attaque des unitées
			if typeJoueurs[0]=="humain":
				for i in range(len(contenuArmees[0].compo)):
					contenuArmees[0].compo[i].reinitAttaque()
					contenuArmees[0].compo[i].reinitDeplacement()
				p=GUIfunc.bougerPions(fen,contenuArmees,p,0)
				print("j1 à bouger")
				contenuArmees=GUIfunc.attaquer(fen,contenuArmees,p,0)
				print("j1 à attaquer")

			elif typeJoueurs[0]=="IA0":
				bebeBeel.deplacerUnites(p,1,0,contenuArmees)
				bebeBeel.attaqueAuto(p,1,0,contenuArmees)
			GUIfunc.afficheGrille(fen,contenuArmees)

#tours du joueur 2
		else:
			#remise à zero des déplacement et attaque des unitées
			if typeJoueurs[1]=="humain":
				for i in range(len(contenuArmees[0].compo)):
					contenuArmees[0].compo[i].reinitAttaque()
					contenuArmees[0].compo[i].reinitDeplacement()
				p=GUIfunc.bougerPions(fen,contenuArmees,p,1)
				print("j2 à bouger")
				contenuArmees=GUIfunc.attaquer(fen,contenuArmees,p,1)
				print("j2 à attaquer")
			
			elif typeJoueurs[1]=="IA0":
				bebeBeel.deplacerUnites(p,0,1,contenuArmees)
				bebeBeel.attaqueAuto(p,0,1,contenuArmees)
			GUIfunc.afficheGrille(fen,contenuArmees)
		
		Tours+=1
