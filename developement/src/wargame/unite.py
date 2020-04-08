#Version : 0.2.0

#Pour ajouter le dossier parent dans le Path et pouvoir tout importer
import sys
sys.path.append('../')

from algorithmes.Astar import *
from random import *
from copy import deepcopy

class Dicoref(object):
	'''
	Dictionnaire qui contient en clé le nom des races, en valeur des
	dictionnaires avec en clé le nom des unités et en valeur une liste
	des stats des unités.
	'''

	def __init__(self):
		self.dico={}
		self.imparmee()

	def imparmee(self):
		'''
		Méthode permmettant de créer le dictionnaire des armées,
		en accédant aux csv des armées.
		'''
		race=("humains","nains","demons","orks","elfes") #liste des différentes races dispos
		for i in race:
			try:
				open("../armee/"+i+".csv","r",encoding="utf-8")
				link = "../armee/"
			except:
				link = "../../armee/"
			finally:
				files=open(link+i+".csv","r",encoding="utf-8") # ouverture du csv
				Ndico={} # dico qui contiendra les unités et leurs stats
				for j in files.readlines(): # lecture du csv
					j=j.split(",")
					j[-1]=j[-1][:-1]
					Ndico[j[0]]=j[1:]
				self.dico[i]=Ndico # ajoute dans le dictionnaire des races le dictionnaire contenant les unités et leurs stats
				files.close()




class Armee(object):

	def __init__(self,armee):
		self.armee=armee
		self.nbunite=0
		self.solde=1000
		self.compo={}
		self.id=None

	def __repr__(self):
		composion={}
		for i in self.compo :
			if self.compo[i].nom not in composion:
				composion[self.compo[i].nom]=1
			else :
				composion[self.compo[i].nom]+=1

		return "Armée de type : "+str(self.armee)+"\nNombre d'unités : "+str(self.nbunite)+"\nComposition : "+str([str(i)+" "+str(composion[i]) for i in composion])
		# return "Armée id#"+str(self.id) #Temporaire pour permettre un meilleur traçage des armées

	def json(self):
		"""
		Renvoie la composition de l'Armée de façon structurée pour les données JSON
		"""
		composion={}
		for i in self.compo :
			if self.compo[i].nom not in composion:
				composion[self.compo[i].nom]=1
			else :
				composion[self.compo[i].nom]+=1

		return [str(i)+" "+str(composion[i]) for i in composion]

	def prix(self):
		"""
		(re)Calcul le prix de l'armée, ce qui permet de valider l'addition de 2 armées
		"""
		return sum([self.compo[i].prix for i in self.compo])

	def __add__(self,objet):
		if isinstance(objet,Armee):
			if self.armee != objet.armee:raise TypeError("Les deux armées doivent être de même race")
			if self.solde - objet.prix() < 0:raise ValueError("La fusion des 2 armées fait dépasser le solde fixé")
			##Sinon, même race, solde suffisant, pas d'objection ?
			newArmee = Armee(self.armee)
			#On ajoute "manuellement", sans addUnite, les unités une à une, celles-ci pouvent potentiellement déjà être blessé (Pour une utilisation X ou Y future)
			keyIndex = 0
			for i in self.compo:
				newArmee.compo[keyIndex] = deepcopy(self.compo[i])#Ajout des unités
				newArmee.compo[keyIndex].num = keyIndex     #Mise à jour de leur numéro
				keyIndex += 1
			for i in objet.compo:
				newArmee.compo[keyIndex] = deepcopy(objet.compo[i])
				newArmee.compo[keyIndex].num = keyIndex
				keyIndex += 1
			#Mise à jour du solde réel de newArmee et du nombre d'unité
			newArmee.solde -= newArmee.prix()
			newArmee.nbunite = keyIndex
			return newArmee

		elif isinstance(objet,Unite):
			if self.armee != objet.race:raise TypeError("L'unité doit être de même race que l'armée pour la rejoindre")
			if self.solde < objet.prix:raise ValueError("L'ajout de l'unité fait dépasser le solde fixé")
			if objet.pv <= 0:raise Exception("L'unité doit posséder des vies pour être ajoutée à cette armée")
			#Plus d'objection ?
			#Ajout dans l'armée
			keyIndex = 0    #Pour les clés du dictionnaire, on suppose que ces armées ont peut être subi des pertes donc que si la clé 5 est libre, 6 ne l'est peut être pas
			while self.compo.get(keyIndex,0):       #On cherche une clé disponible
				keyIndex += 1
			objet = deepcopy(objet)
			objet.num = keyIndex
			self.compo[keyIndex] = objet    #Ajout de l'unité
			#Arrangement des détails
			self.nbunite += 1
			self.solde -= objet.prix

		else:
			raise TypeError("Armee + OBJET, OBJET doit être une instance de Armee ou Unite")

	def __sub__(self,objet):
		if isinstance(objet,Unite):
			if objet in self.compo.values():
				del self.compo[objet.num]
			else:raise Exception("L'unité renseignée ne semble pas faire partie de cette armée")
		else:raise Exception("Armee - OBJET, OBJET doit être une instance de Unite")


class Unite(object):

	def __init__(self,num,nom,race,pv,armure,prec,attq,depl,portee,esq,crit,prix,typeu,perteprec):
		self.num=num
		self.nom=nom
		self.race=race
		self.pv=int(pv)
		self.armure=int(armure)
		self.precision=int(prec)
		self.attaque=int(attq)
		self.capaDeplacement=int(depl)
		self.portee=int(portee)
		self.esquive=int(esq)
		self.critique=int(crit)
		self.prix=int(prix)
		self.type=typeu
		self.pertePrecision=int(perteprec)
		self.deplacementRestant = self.capaDeplacement
		self.attaqueRestante = 1
		self.coord=(0,0)#coordonnées de l'unité, correspond à (xd,yd)

	def __repr__(self):
		return str(self.nom)+str(self.num)

	def deplacement(self,plateau,xa,ya):
		"""
		Effectue, si cela est possible, un déplacement d'une unité choisie.

		:param self.coord[0]: Coordonnée X de l'unité à déplacer.
		:type self.coord[0]: int
		:param self.coord[1]: Coordonnée Y de l'unité à déplacer.
		:type self.coord[1]: int
		:param xa: Coordonnée X de la destination ciblée.
		:type xa: int
		:param ya: Coordonnée Y de la destination ciblée.
		:type ya: int
		"""
		#On s'assure que les coordonnées d'arriver sont valides, donc si elles appartiennent bien au plateau de jeu
		if 0 <= ya < len(plateau.troupes) and 0 <= xa < len(plateau.troupes[0]):
			#On regarde la distance de déplacement maximale de l'unité
			distance = self.capaDeplacement
			#Si le chemin, ne serait-ce que par les coordonnées, est trop long, pas la peine d'intéragir (Utile surtout pour les Joueurs réels, l'IA réflechira differamment)
			if (abs(xa-self.coord[0])+abs(ya-self.coord[1])) <= self.capaDeplacement:#On regarde si l'unité a assez de déplacement restant pour effectuer un chemin direct
				grille = plateau.grilleObstacle(self.coord[0],self.coord[1],distance)  #Les coordonnées self.coord[0],self.coord[1] se retrouvent au centre dans la grille renvoyée
				x0,y0 = int(((len(grille)-1)/2)),int(((len(grille)-1)/2))   #Coordonnées centrales, plus pratique pour la suite
				#On test d'abord si un chemin direct est possible pour éviter le Astar
				Chemin1 = True  #Va virer à False s'il rencontre un obstacle
				Chemin2 = True
				for i in range(abs(xa-self.coord[0])):     #Voir explications schématisées (Diaporama)
					if grille[y0][x0+(i+1)*int((xa-self.coord[0])/(abs(xa-self.coord[0])))] == 0:
						Chemin1 = False
					if grille[y0+(ya-self.coord[1])][x0+(i)*int((xa-self.coord[0])/(abs(xa-self.coord[0])))] == 0:
						Chemin2 = False
				for i in range(abs(ya-self.coord[1])):
					if grille[y0+i*int((ya-self.coord[1])/abs(ya-self.coord[1]))][x0+(xa-self.coord[0])] == 0:
						Chemin1 = False
					if grille[y0+(i+1)*int((ya-self.coord[1])/abs(ya-self.coord[1]))][x0] == 0:
						Chemin2 = False
				#Si un chemin direct est possible, on effectue le déplacement
				if Chemin1 or Chemin2:
					#RAJOUTER ici condition de auPlusProche ou non, ce qui influera sur l'effectuation d'un déplacement ou non
					plateau.troupes[self.coord[1]][self.coord[0]],plateau.troupes[ya][xa] = plateau.troupes[ya][xa],plateau.troupes[self.coord[1]][self.coord[0]]#Change la position de l'unité dans la grille plateau
					self.coord=(xa,ya)#change les coordonnées de l'unité
					# self.capaDeplacement -= abs(xa-self.coord[0])+abs(ya-self.coord[1])

				#S'il n'y a pas de chemin direct, on lance alors l'Algorithme A*
				else:
					CheminA = Astar(grille,(x0,y0),(x0+xa-self.coord[0],y0+ya-self.coord[1]))
					if CheminA:
						while len(CheminA) > self.capaDeplacement:
							CheminA=CheminA[:-1]
							#RAJOUTER ici condition de auPlusProche ou non, ce qui influera sur l'effectuation d'un déplacement ou non
						plateau.troupes[self.coord[1]][self.coord[0]],plateau.troupes[ya][xa] = plateau.troupes[ya][xa],plateau.troupes[self.coord[1]][self.coord[0]]#Change la position de l'unité dans la grille plateau
						self.coord=(xa,ya)#change les coordonnées de l'unité

					else:
						return False
			else:
				raise Exception("Le chemin est trop long pour cette unité")
##                PLANTé : A VIRER OU A MODIFIER
##                distance = self.capaDeplacement
##                grille = plateau.grilleObstacle(self.coord[0],self.coord[1],20)  #Les coordonnées self.coord[0],self.coord[1] se retrouvent au centre dans la grille renvoyée
##                x0,y0 = int(((len(grille)-1)/2)),int(((len(grille)-1)/2))   #Coordonnées centrales, plus pratique pour la suite
##                CheminA = Astar(grille,(x0,y0),(x0+xa-self.coord[0],y0+ya-self.coord[1]))
##                if CheminA:
##                    while len(CheminA) > self.capaDeplacement:
##                        CheminA=CheminA[:-1]
##                        #RAJOUTER ici condition de auPlusProche ou non, ce qui influera sur l'effectuation d'un déplacement ou non
##                    plateau.troupes[self.coord[1]][self.coord[0]],plateau.troupes[ya][xa] = plateau.troupes[ya][xa],plateau.troupes[self.coord[1]][self.coord[0]]#Change la position de l'unité dans la grille plateau
##                    self.coord=(xa,ya)#change les coordonnées de l'unité
		else:
			raise Exception("Coordonnées en dehors des limites possibles")

	def placerUnite(self,plateau,x,y,caseVide=1):
		"""
		Positionne une unité donnée aux coordonnées renseignées si cela est possible, donc si la case cible est vide.

		:param unite: Objet correspondant à l'unité voulue.
		:type unite: object
		:param x: Coordonnée X à laquelle positionner l'unité.
		:type x: int
		:param y: Coordonnée Y à laquelle positionner l'unité.
		:type y: int
		:param caseVide: Valeur correspondant à une case vide, ou du moins une case valable pour positionner l'unité.
		:param caseVide: int/str (Tout dépend du choix réalisé, par défaut vaut 1)
		"""
		if  0 <= x < len(plateau.troupes[0]) and 0 <= y < len(plateau.troupes):
			if plateau.troupes[y][x] == caseVide:
				plateau.troupes[y][x] = self
				self.coord=(x,y)



	def testPrecision(self,distance):
		"""
		Renvoie True si l'unité à réussi son test de précision, False sinon

		:param distance : distance entre l'acher et la cible
		:type distance : int
		"""
		return randint(0,100)<=self.precision - self.pertePrecision*(distance-1)

	def testEsquive(self):
		"""
		Renvoie True si l'unité à réussi son test d'equive, False sinon

		:param distance : distance entre l'acher et la cible
		:type distance : int
		"""
		return randint(0,100)<=self.esquive

	def calculDegats(self):
		'''
		Renvoie les dégats infligés à une unité
		'''
		crit=1
		if randint(0,100)<=self.critique:
			crit=1.5
		return int(self.attaque*crit)

	def ajusterArmure(self,taux):   #En mode défense, à l'heure actuelle, les unités reçoivent 20% d'armure en plus
		"""
		Renvoie la valeur de l'armure de l'unité en fcontion du mode défense

		:param taux : modification appliquée à la défense de l'unité
		:type taux : int
		"""
		return self.armure * taux

	def reinitAttaque(self):
		"""
		Reset le nombre d'attaque restantes pour l'unité
		"""
		self.attaqueRestant = 1

	def reinitDeplacement(self):
		"""
		Reset le nombre de cases de déplacement restantes pour l'unité
		"""
		self.deplacementRestant = self.capaDeplacement

	def supprimerPV(self,degats):
		"""
		Retire des pv à l'unité d'une valeur de degats

		:param degats : pv qui seront perdus par l'unité
		:type degats : int
		"""
		self.pv -= degats*(1-self.armure/100)


	def ennemisAPortee(self,plateau,armeeEnnemie,contenuArmees):
		"""
		Renvoie une liste des ennemis à portée de l'unité

		:param plateau : plateau de jeu
		:type degats : object
		"""
		cibles=[]
		print(len(contenuArmees[armeeEnnemie].compo))
		for i in range(len(contenuArmees[armeeEnnemie].compo)):
			if abs(contenuArmees[armeeEnnemie].compo[i].coord[0]-self.coord[0])+abs(contenuArmees[armeeEnnemie].compo[i].coord[1]-self.coord[1])<=self.portee:
				cibles+=[ [ contenuArmees[armeeEnnemie].compo[i],contenuArmees[armeeEnnemie].compo[i].coord ] ]
		return cibles



	def factory(race,unite,num,dicoref):
		"""
		Méthode abstraite qui crée une unité à partir d'une race et d'un nom d'unité

		:param race : race de l'unité qui sera créée
		:type race : str
		:param unite : nom de l'unité qui sera créée
		:type unite : str
		"""
		stats=dicoref.dico[race][unite]
		return Unite(num,unite,race,stats[0],stats[1],stats[2],stats[3],stats[4],stats[5],stats[6],stats[7],stats[8],stats[9],stats[10])


def addUnite(armee,unite,dicoref):
	"""
	Fonction abstraite fait appelle à la factory pour crée une unité (si le solde de points est suffisant) dans une armée et qui met à jour les informations de l'armée en question

	:param armee : objet dans lequel l'unité créée par la factory sera ajoutée
	:type armee : object
	:param unite : nom de l'unité qui sera ajoutée
	:type unite : str
	"""
	newUnite=Unite.factory(armee.armee,unite,len(armee.compo),dicoref)
	if armee.solde-newUnite.prix>=0:
		armee.solde-=newUnite.prix
		armee.nbunite += 1
		armee.compo[len(armee.compo)]=newUnite
	else :
		raise ValueError("solde trop bas !")
	# return armee

if __name__=="__main__":
	dicoref=Dicoref()
	from plateau import *
	P = Plateau(5,5)
	class U(object):
		def __init__(self):
			self.capaDeplacement = 3    #Pour le moment, marche pour 2 mais pas pour 3 (qui est trop proche du bord)
		def __repr__(self):
			return "U"

	#Test des opérations sur les armées
	A = Armee("humains")
	addUnite(A,"cavalier",dicoref)
	addUnite(A,"cavalier",dicoref)
	a = Armee("humains")
	addUnite(a,"archer",dicoref)
	B = A+a
	B + a.compo[0]
	addUnite(A,"cavalier",dicoref)
	B - B.compo[1]
