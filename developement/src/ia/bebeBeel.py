#Imports normaux
import pickle
import time
from random import randint

#Pour ajouter le dossier parent dans le Path et pouvoir tout importer
import sys
sys.path.append('../')

#Nouveaux imports
from algorithmes.Astar import *
#from wargame import unite #Inutile ?


class bebeBeel(object):
# IA qui joue sans créer ses armées (les récupère), effectue les attaques,
# les déplacements et place les unités en début de partie.
	'''
	AI qui possède des méthodes pour récupèrer des armées déjà créées dans un fichier et créer une armée, la placer sur un plateau, déplacer ses unités et les faire attaquer
	'''



	def creationArmee():
		"""
		Méthode qui permet d'ouvrir un fichier pour récupérer des armées déjà créées 
		"""
		try:
			open("armeeia/humains.save",'rb')
			link = "armeeia/humains.save"
		except:
			link = "../armeeia/humains.save"
		finally:
			with open(link,'rb') as fichier :
				mon_depickler=pickle.Unpickler(fichier)
				listArmee=mon_depickler.load()
				armee=listArmee[randint(0,len(listArmee)-1)]
				listArmee=None
				return armee

			# récupère la race et la composition de son armée dans un fichier 
			# txt/csv/bin... (éventuellement suscrée par l'algoG) ?
			# Retourne l'armée créée

	def placerUnites(plateau,joueur,listeDesArmees):
		"""
		Permet de placer les unités de l'armée placée en position joueur dans l'armée listeDesArmees[joueur] sur plateau

		:param plateau: Plateau de jeu
		:type plateau: object
		:param joueur: Numéro du joueur (joueur 0 ou 1)
		:type joueur: int
		:param listeDesArmees: Liste contenant les armées de la partie
		:type listeDesArmees: list
		"""

		cases=[]
		if joueur == 0 :
			for j in range(0,4):
				for i in range(len(plateau.troupes[j])):
					if plateau.troupes[j][i]==1 and plateau.terrain[j][i]==1:
						cases+=[(i,j)]
			for j in listeDesArmees[joueur].compo:
				k=randint(0,len(cases)-1)
				listeDesArmees[joueur].compo[j].coord=cases[k]
				plateau.troupes[cases[k][1]][cases[k][0]]=listeDesArmees[joueur].compo[j]
				del cases[k]
		else :
			for j in range(16,20):
				for i in range(len(plateau.troupes[j])):
					if plateau.troupes[j][i]==1 and plateau.terrain[j][i]==1:
						cases+=[(i,j)]
			for j in range(len(listeDesArmees[joueur].compo)):
				k=randint(0,len(cases)-1)
				listeDesArmees[joueur].compo[j].coord=cases[k]
				plateau.troupes[cases[k][1]][cases[k][0]]=listeDesArmees[joueur].compo[j]
				del cases[k]

	def deplacerUnites(plateau,armeeEnnemie,joueur,listeDesArmees):
		"""
		Permet de déplacer les unités de l'armée placée en position joueur dans l'armée listeDesArmees[joueur] sur plateau

		:param plateau: Plateau de jeu
		:type plateau: object
		:param armeeEnnemie: Numéro du joueur ennemi (0 ou 1)
		:type armeeEnnemie: int
		:param joueur: Numéro du joueur (joueur 0 ou 1)
		:type joueur: int
		:param listeDesArmees: Liste contenant les armées de la partie
		:type listeDesArmees: list
		"""
		for k in listeDesArmees[joueur].compo:
			cibles=[]
			for i in listeDesArmees[armeeEnnemie].compo:
				if abs(listeDesArmees[armeeEnnemie].compo[i].coord[0]-listeDesArmees[joueur].compo[k].coord[0])+abs(listeDesArmees[armeeEnnemie].compo[i].coord[1]-listeDesArmees[joueur].compo[k].coord[1])<=listeDesArmees[joueur].compo[k].portee:
					cibles+=[1]
			if cibles==[]:
				cases=[]
				for i in range(len(plateau.troupes)):
					for j in range(len(plateau.troupes[i])):
						if plateau.troupes[j][i]==1 and plateau.terrain[j][i]==1 and abs(listeDesArmees[joueur].compo[k].coord[0]-i)+abs(listeDesArmees[joueur].compo[k].coord[1]-j)<=listeDesArmees[joueur].compo[k].capaDeplacement:
							cases+=[(i,j)]
				arrivee=randint(0,len(cases)-1)

				# listeDesArmees[joueur].compo[k].deplacement(plateau,cases[arrivee][0],cases[arrivee][1])
				try :
					listeDesArmees[joueur].compo[k].deplacement(plateau,cases[arrivee][0],cases[arrivee][1])
				except :
					pass
			




	def attaqueAuto(plateau,armeeEnnemie,joueur,listeDesArmees):
		"""
		Permet à toutes les unités de l'armée placée en position joueur dans l'armée listeDesArmees[joueur] d'effectuer leur attaque si possible

		:param plateau: Plateau de jeu
		:type plateau: object
		:param armeeEnnemie: Numéro du joueur ennemi (0 ou 1)
		:type armeeEnnemie: int
		:param joueur: Numéro du joueur (joueur 0 ou 1)
		:type joueur: int
		:param listeDesArmees: Liste contenant les armées de la partie
		:type listeDesArmees: list
		"""

		for j in listeDesArmees[joueur].compo:
			uniteAttaquante=listeDesArmees[joueur].compo[j]
			cibles=[]
			for i in listeDesArmees[armeeEnnemie].compo:
				if abs(listeDesArmees[armeeEnnemie].compo[i].coord[0]-listeDesArmees[joueur].compo[j].coord[0])+abs(listeDesArmees[armeeEnnemie].compo[i].coord[1]-listeDesArmees[joueur].compo[j].coord[1])<=listeDesArmees[joueur].compo[j].portee:
					cibles+=[ [ listeDesArmees[armeeEnnemie].compo[i],listeDesArmees[armeeEnnemie].compo[i].coord ] ]
			if cibles != []:
				k=randint(0,len(cibles)-1)
				defenseur=cibles[k][1]
				dist=abs(int(defenseur[0])-uniteAttaquante.coord[0])+abs(int(defenseur[-1])-uniteAttaquante.coord[-1])
				if uniteAttaquante.testPrecision(dist):
					if not plateau.troupes[int(defenseur[-1])][int(defenseur[0])].testEsquive():
						plateau.troupes[int(defenseur[-1])][int(defenseur[0])].supprimerPV(uniteAttaquante.calculDegats())	
						if plateau.troupes[int(defenseur[-1])][int(defenseur[0])].pv <= 0 :
							del listeDesArmees[armeeEnnemie].compo[plateau.troupes[int(defenseur[-1])][int(defenseur[0])].num]
							plateau.troupes[int(defenseur[-1])][int(defenseur[0])]=1

	# def donnéesAlgoG():
	# 	pass
	# 	# récupère des données sur le cours de la partie ?
