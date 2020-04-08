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

def dataCroisement(dico,tournoisnb,armeeCroise):
	if tournoisnb not in dico:
		dico[tournoisnb]=[armeeCroise]
	else:
		dico[tournoisnb]+=[armeeCroise]
	return dico

def dataMutation(armee,mute,mutant):
	return {armee:{"qui":mute,"quoi":mutant}}

def algo(nbtour=1,nbarmee=10):
	population = maker.créer(nbarmee)
	dicoCroisement={}
	dicoMutatation={}
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


		for i in range(int(len(population)/2)):
			M = Mutator(population[i])
			M.mutation()
			dicoMutatation["tournois"+str(cpt)]=dataMutation("armee"+str(i),M.qui,M.quoi)
			# dicoMutatation[tournois+str(cpt)]={population[i]:{"qui":M.qui,"quoi":M.quoi}}
			population[i] = M.newCompo
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

if __name__=="__main__":
	algo(6,4)