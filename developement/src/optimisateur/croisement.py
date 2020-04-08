#Pour ajouter le dossier parent dans le Path et pouvoir tout importer
import sys
sys.path.append('../')

from wargame.unite import *
#from mutator import autoCompletion      #Pour pouvoir auto-compléter des armées
import random

class Crossover():

    def __init__(self,armees):

# prend en entré une liste contenant deux objets armées
        self.pere=armees[0].compo
        self.mere=armees[1].compo
        self.race=armees[0].armee
        self.enfant=Armee(self.race)
        self.dicoref=Dicoref()

    def croisement(self):

        start=True
        i=0
        mini=min([self.pere[i].prix for i in range(len(self.pere))]+[self.mere[i].prix for i in range(len(self.mere))])
        while start:
            if i%2==0:
                choixP=self.pere[random.randint(0,len(self.pere)-1)]
                try:
                    i+=1
                    addUnite(self.enfant,choixP.nom,self.dicoref)
                except:
                    pass


            elif i%2==1:
                i+=1
                choixM=self.mere[random.randint(0,len(self.mere)-1)]
                try:
                    addUnite(self.enfant,choixM.nom,self.dicoref)
                except:
                    pass

            if self.enfant.solde<mini:
                start=False
                

def croisementMultiple(population,reference,*args,**kw):
    """
    :param population: Population d'armées à croiser.
    :type population: list of Armee object
    :param reference: Dictionnaire de référence des unités (cf DicoRef).
    :type reference: dict
    """
    ###TEMP###
    reste = random.sample(population,int(len(population)/2))
    ##########
    newPopulation = []
    for i in range(int(len(population)/2)):
        parents = random.sample(population,2)
        newPopulation.append(croisement(parents[0],parents[1],reference))
        for j in parents : population.remove(j)
    newPopulation.extend(population)    #Armées non mutées ajoutées à la nouvelle population
    newPopulation.extend(reste)         #Temporaire, pour avoir un nombre constant d'armées dans l'algoG
    return newPopulation

def croisement(armee1,armee2,reference):
    """
    :param armee1: Première Armée parente pour le croisement.
    :type armee1: Armee object
    :param armee2: Seconde Armée parente pour le croisement.
    :type armee2: Armee object
    :param reference: Référence de toutes les armées et unités (cd DicoRef).
    :type reference: dict

    :note: Le croisement effectue un réel croisement, il part donc des compositions des 2 armées parentes pour en composer une nouvelle. La sélection des unités se fait de façon aléatoire. Dans le cas où les armées parentes engendres un reste de solde, l'armée ne sera pas auto-complétée, utiliser donc la fonction associée pour cela.
    """
    armee1,armee2 = deepcopy(armee1),deepcopy(armee2)
    if armee1.armee != armee2.armee : raise ValueError("Les deux armées ne sont pas de la même race")
    newArmee = Armee(armee1.armee)

    #Début du croisement
    disponible1,disponible2 = embauchable(newArmee,armee1.compo),embauchable(newArmee,armee2.compo)
    while disponible1 or disponible2:
        disponible1 = embauchable(newArmee,armee1.compo)
        if disponible1 :
            addUnite(newArmee,armee1.compo[disponible1[random.randint(0,len(disponible1)-1)]].nom,reference)
            del armee1.compo[disponible1[random.randint(0,len(disponible1)-1)]]
        disponible2 = embauchable(newArmee,armee2.compo)
        if disponible2 :
            addUnite(newArmee,armee2.compo[disponible2[random.randint(0,len(disponible2)-1)]].nom,reference)
            del armee2.compo[disponible2[random.randint(0,len(disponible2)-1)]]
    ##TEMPO ID de traçage
    newArmee.id = "("+str(armee1.id)+"x"+str(armee2.id)+")"
    ##
    return newArmee

def embauchable(armee,reference):
    """
    Version où les références sont des objets Unites.

    :param armee: Armée dans laquelle effectuer une embauche.
    :type solde: Armee object
    :param reference: Référence des unités disponible (des armées parentes, autrement dit leur composition restante).
    :type reference: dict

    :note: Les unités de type Général (gen) ne sont pas considérées comme embauchable
    """
    return [i for i in reference if reference[i].prix <= armee.solde and "gen" not in reference[i].type]     #Indice 8 = prix de l'unité




if __name__=="__main__":
# création d'un objet armée pour le teste
    dicoref=Dicoref()
    listeUnite1=["archer","archer","archer","archer","archer","stop"]
    listeUnite2=["enrole","enrole","enrole","enrole","enrole","stop"]
    A=Armee("humains")
    B=Armee("humains")
    for i in listeUnite1:
        if i != "stop":
            addUnite(A,i,dicoref)
    for i in listeUnite2:
        if i != "stop":
            addUnite(B,i,dicoref)
    listeArmee=[A,B]
# lancement du croisement
    fils=Crossover(listeArmee)
    fils.croisement()
    print("Composition via l'objet croisement:\n",fils.enfant)
    print(fils.enfant.solde)

#Test des croisements via fonctions
    testCroisMultiple = croisementMultiple([A,A,A,B,B],dicoref)
    print("\n\nCompositions via les fonctions croisements:\n",testCroisMultiple)

