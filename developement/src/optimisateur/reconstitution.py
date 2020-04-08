#Imports normaux
from pprint import *
from random import *
from time import *
import pickle
from copy import deepcopy

#Pour ajouter le dossier parent dans le Path et pouvoir tout importer
import sys
sys.path.append('../')

#Nouveaux imports
from wargame.plateau import *
from algorithmes.Astar import *
from ia.bebeBeel import *
#from wargame import unite Inutile ?



def lecteur(armees="armeeia/humains.save",num_armee1=0,num_armee2=1,graine=0):
	try:
		open("armeeia/"+fichierArmees+".save","rb")
		link = "armeeia/"
	except:
		link = "../armeeia/"
	with open(link+armees+".save",'rb') as fichier :
		mon_depickler=pickle.Unpickler(fichier)
		listArmee=mon_depickler.load()

	seed(graine)

	contenuArmees=[deepcopy(listArmee[num_armee1]),deepcopy(listArmee[num_armee2])]

	p=Plateau(20,20)
	Tours=0

	bebeBeel.placerUnites(p,0,contenuArmees)
	bebeBeel.placerUnites(p,1,contenuArmees)

	while contenuArmees[0].compo != {} and contenuArmees[1].compo != {} :
		if Tours%2==0:
			bebeBeel.deplacerUnites(p,1,0,contenuArmees)
			bebeBeel.attaqueAuto(p,0,1,contenuArmees)

			Tours+=1
		else :
			bebeBeel.deplacerUnites(p,0,1,contenuArmees)
			bebeBeel.attaqueAuto(p,1,0,contenuArmees)


			Tours+=1
	print(p)

lecteur("humains",0,1,5)
lecteur("humains",0,1,5)
lecteur("humains",0,1,5)
lecteur("humains",0,1,5)
