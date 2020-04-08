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



def compteurUnite(armee):
    comptes = {}
    for i in armee.compo:
        comptes[armee.compo[i].nom] = comptes.get(armee.compo[i].nom,0)+1
    return comptes

def compteurArmees(population):
    comptes = {}
    for i in population:
        comptesArmee = compteurUnite(i)
        for j in comptesArmee:
            comptes[j] = comptes.get(j,0)+comptesArmee[j]
    return comptes

def fusionComptes(comptes1,comptes2):
    """Aucune idée pourquoi je l'ai faite"""
    comptes = {}
    for i in comptes1:
        comptes[i] = comptes1.get(i,0)+comptes2.get(i,0)
        del comptes2[i]
    for i in comptes2:
        comptes[i] = comptes2[i]

    return comptes

def addData(comptesCommuns,comptesNouveaux):
    for i in comptesCommuns:
        print(comptesCommuns[i],"+",comptesNouveaux.get(i,0))
        if comptesCommuns[i] : comptesCommuns[i] = comptesCommuns[i]+[comptesNouveaux.get(i,0)]
        else : comptesCommuns[i] = [comptesNouveaux.get(i,0)]
def outData(comptes,chemin):
    texte = ""
    for i in comptes:
        texte += "\n"+i
        for j in comptes[i]:
            texte += ","+str(j)
    file = open(chemin,"w")
    file.write(texte)
    file.close()



population = maker.créer(5)
dicoref = unite.Dicoref()

G = AlgorithmeGenetique(population,tournois,croisementMultiple,mutationMultiple,inputCroisement="2",ifInputCroisementUnsatisfied="+",inputMutation="5",reference=dicoref)


comptesCommuns = {i:[] for i in dicoref.dico[population[0].armee]}
addData(comptesCommuns,compteurArmees(population))

for i in range(6):
    population = next(G)
    addData(comptesCommuns,compteurArmees(population))

outData(comptesCommuns,"test-24-02.csv")




