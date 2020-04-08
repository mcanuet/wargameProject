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

class AlgoV2(object):

	def __init__(self,nbTour=10,nbArmee=10,pourcentPur=40,pourcentMute=30,pourcentCroises=30,pop="pure"):
		self.nbTour=nbTour
		self.nbArmee=nbArmee

		if pop == None :
			self.population = maker.Maker.alea(self,nbACreer=10,race="humains")

		if pop == "pure" :
			self.population = maker.Maker.pure('humains')
			while len(self.population)<nbArmee :
				self.population += maker.Maker.alea(self,nbACreer=1,race="humains")
	

		self.pourcentPur=int(pourcentPur/100*len(self.population))
		self.pourcentMute=int(pourcentMute/100*len(self.population))
		self.pourcentCroises=int(pourcentCroises/100*len(self.population))
		self.total=pourcentPur+pourcentMute+pourcentCroises



	def dataCroisement(self,dico,tournoisnb,armeeCroise):
		if tournoisnb not in dico:
			dico[tournoisnb]=[armeeCroise]
		else:
			dico[tournoisnb]+=[armeeCroise]
		return dico

	def dataMutation(self,listeDico,armee,mute,mutant,prix):
		if armee not in listeDico:
			listeDico.append({armee:{"qui":mute,"quoi":mutant, "combien":prix}})
		
	def makeMutaDico(self,dico,listeMuta,cle):
		for i in listeMuta:
			if cle not in dico:
				dico[cle]={}
			dico[cle].update(i)
		return dico



	def algo(self):
		
		dicoCroisement={}
		dicoMutatation={}
		t=time.time()


		if self.total!=100:
			print("Pourcentages biaisés")
			print(self.total)

		else :

			for tours in range(self.nbTour):
				print('Tours numero',tours)
				self.population,data = tournois(self.population,backData=True,save="web/data")

				newPop=[]

				for i in range(self.pourcentPur):
					newPop.append(self.population[i])



		## Début des mutations

				listeDico=[]
				for i in range(self.pourcentPur,self.pourcentPur+self.pourcentMute):
					M=Mutator(self.population[i])
					M.mutation()
					self.dataMutation(listeDico,"armee"+str(i),M.qui,M.quoi,M.combien)
					newPop.append(M.newCompo)
				dicoMutatation=self.makeMutaDico(dicoMutatation,listeDico,"tournois"+str(tours))


		## Début des croisements

				for i in range(self.pourcentCroises):
					C = Crossover([self.population[2*i],self.population[2*i+1]])
					C.croisement()
					dicoCroisement=self.dataCroisement(dicoCroisement,"tournois"+str(tours),("armee"+str([2*i]),"armee"+str([2*i+1])))
					newPop.append(C.enfant)

				
				self.population=newPop

				recupe.listing()

		## Exportation des données

			file=open("web/data/croisement0.json","w")
			file.write(json.dumps(dicoCroisement))
			file.close()

			file=open("web/data/mutation0.json","w")
			file.write(json.dumps(dicoMutatation))
			file.close()

		## Affichage du temps d'exectution de l'algoG

			seconde = int(time.time()-t)
			heure = seconde /3600
			seconde %= 3600
			minute = seconde/60
			seconde%=60
			print (int(heure),'H,',int(minute),'min,',int(seconde),'s')


if __name__=="__main__":
	algorithme=AlgoV2()
	algorithme.algo()
