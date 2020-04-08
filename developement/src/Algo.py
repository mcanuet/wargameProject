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
import time

def dataCroisement(dico,tournoisnb,armeeCroise):
	if tournoisnb not in dico:
		dico[tournoisnb]=[armeeCroise]
	else:
		dico[tournoisnb]+=[armeeCroise]
	return dico

def dataMutation(listeDico,armee,mute,mutant,prix):
	if armee not in listeDico:
		listeDico.append({armee:{"qui":mute,"quoi":mutant, "combien":prix}})
	
def makeMutaDico(dico,listeMuta,cle):
	# print("---------\n",listeMuta,"\n---------")
	for i in listeMuta:
		# print("__________\n",i,"\n__________")
		if cle not in dico:
			dico[cle]={}
		dico[cle].update(i)
	return dico

def algo(nbtour=1,nbarmee=10):
	population = maker.créer(nbarmee)
	dicoCroisement={}
	dicoMutatation={}
	t=time.time()
	
	for cpt in range(nbtour):
		print(len(population))
		population,data = tournois(population,backData=True,save="dataTest.json")
		print("Tournois termine")

		newPop = []
		
		for i in range (int(len(population)/2)):
			C = Crossover([population[2*i+0],population[2*i+1]])
			C.croisement()
			dicoCroisement=dataCroisement(dicoCroisement,"tournois"+str(cpt),("armee"+str([2*i+0]),"armee"+str([2*i+1])))
			newPop.append(C.enfant)
		if nbarmee%2==0:
			population = population[:int(len(population)/2)]+newPop
		else :
			population = population[:int(len(population)/2)+1]+newPop
		print("croisement")

		listeDico=[]

		for i in range(int(len(population)/2)):
			M = Mutator(population[i])
			M.mutation()
			dataMutation(listeDico,"armee"+str(i),M.qui,M.quoi,M.combien)
			population[i] = M.newCompo
		dicoMutatation=makeMutaDico(dicoMutatation,listeDico,"tournois"+str(cpt))
		print("mutation\n")

		recupe.listing()

	if not os.path.isdir("modifData"):
		os.makedirs("modifData")
	file=open("modifData/croisement"+str(len(os.listdir("modifData")))+".json","w")
	file.write(json.dumps(dicoCroisement))
	file.close()

	file=open("modifData/mutation"+str(len(os.listdir("modifData"))-1)+".json","w")
	file.write(json.dumps(dicoMutatation))
	file.close()

	seconde = int(time.time()-t)
	heure = seconde /3600
	seconde %= 3600
	minute = seconde/60
	seconde%=60
	print (int(heure),'H,',int(minute),'min,',int(seconde),'s')

if __name__=="__main__":
	algo(6,4)