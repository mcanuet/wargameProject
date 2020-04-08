import pickle
from algorithmes.AlgoG import *
from optimisateur.tournois import *
from wargame.plateau import *
from algorithmes.Astar import *
from ia.bebeBeel import *
from wargame import unite
from wargame.jeu import Jeu
from wargame import maker
from optimisateur.croisement import *
from optimisateur.mutator import *
import json
import recupe

def lecteur(file):
	a=open(file,"rb")
	b=pickle.load(a)

	for k in b:
		composion={}
		prix = 0
		for i in k.compo :

			if k.compo[i].nom not in composion:
				composion[k.compo[i].nom]=1
			else :
				composion[k.compo[i].nom]+=1
			prix+=k.compo[i].prix
		print( [str(i)+" "+str(composion[i]) for i in composion],"   ",prix)

