#Imports normaux
import pickle
from random import *

#Pour ajouter le dossier parent dans le Path et pouvoir tout importer que ce soit à partir du main ou du module même
import sys
sys.path.append('../')

#Nouveaux imports
from wargame import unite

dicoref=unite.Dicoref()

# def créer(nbACreer=1,dossier="tempo"):
# 	armees=[]
# 	dicoref=unite.Dicoref()
# 	for i in range(nbACreer):
# 		armees+=[unite.Armee("humains")]
# 		while armees[i].solde>min(int(dicoref.dico["humains"][k][-3]) for k in dicoref.dico["humains"]):
# 			for j in dicoref.dico["humains"] :
# 				if j!="general" and armees[i].solde/int(dicoref.dico["humains"][j][-3])>1:
# 					for l in range(randint(1,int(armees[i].solde//int(dicoref.dico["humains"][j][-3])/2)+1)):
# 						unite.addUnite(armees[i],j,dicoref)

# 	try:
# 		open("armeeia/"+dossier+".save","wb")
# 		link = "armeeia/"+dossier+".save"
# 	except:
# 		link = "../armeeia/"+dossier+".save"
# 	finally:
# 		with open(link, 'wb') as fichier:
# 			mon_pickler = pickle.Pickler(fichier)
# 			mon_pickler.dump(armees)

# 	return armees


class Maker(object):
	def alea(self,nbACreer=1,race='humains'):
		armees=[]
		for i in range(int(nbACreer)):
			armees.append(unite.Armee("humains"))
			while armees[i].solde>min(int(dicoref.dico["humains"][k][-3]) for k in dicoref.dico["humains"]):
				for j in dicoref.dico["humains"] :
					if j not in ['General','general','Jarl','reine du chaos'] :
						if armees[i].solde/int(dicoref.dico["humains"][j][-3])>1:
							for l in range(randint(1,int(armees[i].solde//int(dicoref.dico["humains"][j][-3])/2)+1)):
								unite.addUnite(armees[i],j,dicoref)

		try:
			open("armeeia/humainsalea.save","wb")
			link = "armeeia/humainsalea.save"
		except:
			link = "../armeeia/humainsalea.save"
		finally:
			with open(link, 'wb') as fichier:
				mon_pickler = pickle.Pickler(fichier)
				mon_pickler.dump(armees)

		return armees

	def pure(race="humains"):
		armees=[]
		for i in dicoref.dico["humains"]:
			if i not in ['General','general','Jarl','reine du chaos']:
				armees+=[unite.Armee("humains")]
				while armees[-1].solde>int(dicoref.dico["humains"][i][-3]):
					unite.addUnite(armees[-1],i,dicoref)


		try:
			open("armeeia/humainsalea.save","wb")
			link = "armeeia/humainsalea.save"
		except:
			link = "../armeeia/humainsalea.save"
		finally:
			with open(link, 'wb') as fichier:
				mon_pickler = pickle.Pickler(fichier)
				mon_pickler.dump(armees)

		return armees
