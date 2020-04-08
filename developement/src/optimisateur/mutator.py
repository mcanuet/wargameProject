#Pour ajouter le dossier parent dans le Path et pouvoir tout importer
import sys
sys.path.append('../')

from wargame.unite import *
import random

class Mutator():

	def __init__(self,armee,perc=0.9):

		self.perc=perc
		self.compo=armee.compo
		self.newCompo=Armee(armee.armee)
		self.dico=Dicoref()
		self.qui=[]
		self.quoi=[]
		self.combien=[0,0]

	def mutation(self):
		#print(int(len(self.compo)*self.perc))
		nb=int(len(self.compo)*self.perc-1)
		choix=[]

		cpt=0
		while cpt!=nb :
			a=self.compo[random.randint(1,len(self.compo))-1]
			if not a in choix:
				choix.append(a)
				addUnite(self.newCompo,a.nom,self.dico)
				cpt+=1
		
		for i in range(nb,len(self.compo)):
			self.qui.append(self.compo[i].nom)
			self.combien[0]+=self.compo[i].prix


		# récupération des donées pour la sortie web
		# for z in self.compo:
		# 	if self.compo[z] not in self.newCompo.compo:
		# 		self.qui.append(self.compo[z].nom)
		# 		self.combien[0]+=self.compo[z].prix
			# self.qui.append(self.newCompo.compo[z].nom)
			# self.combien[0]+=self.newCompo.compo[z].prix

		choix2=[]

		for j in self.dico.dico[self.newCompo.armee] :
			if j not in ["general","Jarl","reine du chaos","General"]:
				choix2+=[j]

		while self.newCompo.solde>min(int(self.dico.dico[self.newCompo.armee][k][-3]) for k in self.dico.dico[self.newCompo.armee]):
			peon=randint(0,len(choix2)-1)
			if int(self.dico.dico[self.newCompo.armee][choix2[peon]][-3])<=self.newCompo.solde:
				self.quoi.append(choix2[peon])
				self.combien[1]+=int(self.dico.dico[self.newCompo.armee][choix2[peon]][-3])
				addUnite(self.newCompo,choix2[peon],self.dico)

		# print("solde nouvelle armee:	",self.newCompo.solde)

		self.amelioVisu()

	def amelioVisu(self):
		compo={}
		for i in self.qui:
			if i not in compo:
				compo[i]=1
			else:
				compo[i]+=1
		self.qui=[str(i)+" "+str(compo[i]) for i in compo]

		compo={}
		for i in self.quoi:
			if i not in compo:
				compo[i]=1
			else:
				compo[i]+=1
		self.quoi=[str(i)+" "+str(compo[i]) for i in compo]
			

def mutationMultiple(population,reference,*args,**kw):
	"""
	:param population: Population d'armées à muter.
	:type population: list of Armee object
	:param reference: Dictionnaire de référence des unités (cf DicoRef).
	:type reference: dict
	"""
	return [mutation(i,reference,*args,**kw) for i in population]

def mutation(armee,reference,tauxMutation=[0.05,0.15],*args,**kw):
	"""
	:param armee: Armée à muter.
	:type armee: Armee object
	:param reference: Référence de toutes les armées et unités (cf DicoRef).
	:type reference: dict
	:param tauxMutation: Taux de mutation à effectuer sur l'armée. Fournir un flottant pour imposer ce taux ou bien une liste de flottant pour tirer aléatoirement le taux de mutations entre ces bornes.
	:type tauxMutation: float or list of float

	:note: Dans le cas d'un solde insuffisant, une armée peut voir son nombre d'effectif réduire, en revanche, exactement autant d'unités mutées seront tentées d'être réintégré, autrement dit une armée n'augmentera jamais son effectif suite aux mutations. Si besoin, utiliser une fonction d'auto-complétion.
	"""
	newArmee = Armee(armee.armee)   #Création nouvelle armée de même race

	#Gestion de la détection d'un intervalle de mutation
	if isinstance(tauxMutation,list) : tauxMutation = random.uniform(min(tauxMutation),max(tauxMutation))

	#Conservations d'un certain taux de la population
	for i in random.sample(list(armee.compo),round(len(armee.compo)*(1-tauxMutation))):
		addUnite(newArmee,armee.compo[i].nom,reference)

	#Complétion des places libérées
	for i in range(round(len(armee.compo)*tauxMutation)):
		disponible = embauchable(newArmee,reference.dico)
		if disponible : addUnite(newArmee,disponible[random.randint(0,len(disponible)-1)],reference)

	##TEMPO ID de traçage
	newArmee.id = str(armee.id)+"+"
	##
	return newArmee

def embauchable(armee,reference):
	"""
	Version où les références sont les données textes des unités.

	:param armee: Armée dans laquelle vérifier la possibilité d'embauches.
	:type solde: Armee object
	:param reference: Référence de toutes les armées et unités (cf DicoRef).
	:type reference: dict

	:note: Les unités de type Général (gen) ne sont pas considérées comme embauchable
	"""
	return [i for i in reference[armee.armee] if int(reference[armee.armee][i][8]) <= armee.solde and "gen" not in reference[armee.armee][i][9]]     #Indice 8 = prix de l'unité

def autoCompletion(armee,reference):
	"""
	:param armee: Armée dans laquelle effectuer l'auto-complétion d'unités.
	:type solde: Armee object
	:param reference: Référence de toutes les armées et unités (cf DicoRef).
	:type reference: dict
	"""
	disponible = embauchable(armee,reference.dico)
	while disponible:
		addUnite(armee,disponible[random.randint(0,len(disponible)-1)],reference)
		disponible = embauchable(armee,reference.dico)


if __name__=="__main__":
# création d'un objet armée pour le teste
	dicoref=Dicoref()
	A=Armee("humains")
	while A.solde>int(dicoref.dico["humains"]["arbaletrier"][-3]):
		addUnite(A,"arbaletrier",dicoref)
# lancement du croisement
	mute=Mutator(A)
	mute.mutation()
	print("Composition via l'objet mutation:\n",mute.newCompo)

#Test des mutations via fonctions
	testMutMultiple = mutationMultiple([A,mute.newCompo],dicoref)
	print("\n\nCompositions via les fonctions mutations:\n",testMutMultiple)
	
