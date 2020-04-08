from algorithmes.AlgoG import *
from optimisateur.tournoisModified import *
from wargame.plateau import *
from algorithmes.Astar import *
from ia.bebeBeel import *
from wargame import unite
from wargame.jeu import Jeu
from wargame import maker
from optimisateur.croisement import *
from optimisateur.mutator import *
import time,pickle


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
        #print(comptesCommuns[i],"+",comptesNouveaux.get(i,0))
        if comptesCommuns[i] : comptesCommuns[i] = comptesCommuns[i]+[comptesNouveaux.get(i,0)]
        else : comptesCommuns[i] = [comptesNouveaux.get(i,0)]
def outData(comptes,chemin,details=""):
    texte = details
    for i in comptes:
        texte += "\n"+i
        for j in comptes[i]:
            texte += ","+str(j)
    file = open(chemin,"w")
    file.write(texte)
    file.close()

def savePopulation(population,chemin):
    file = open(chemin,"wb")
    monPickler = pickle.Pickler(file)
    monPickler.dump(population)
    file.close()


T_debut = time.time()

population = maker.créer(10)
##population = []
##TMP
##f = open("SAVE_ARMEES","rb")
##md = pickle.Unpickler(f)
##listA = md.load()
##population.extend(listA)
##
dicoref = unite.Dicoref()

##TEMPO ID de traçage
for i in range(len(population)):
    population[i].id = str(i)
##

G = AlgorithmeGenetique(population,tournois,croisementMultiple,mutationMultiple,specificArgsSelection={"progressbar":True},specificArgsMutation={"tauxMutation":[0.05,0.3]},inputCroisement="60%-100%",ifInputCroisementUnsatisfied="+",outputCroisement="60%-100%",inputMutation="20%-100%",outputMutation="20%-100%",reference=dicoref)


comptesCommuns = {i:[] for i in dicoref.dico[population[0].armee]}
comptesDesPremiers = {i:[] for i in dicoref.dico[population[0].armee]}
#addData(comptesCommuns,compteurArmees(population)) Devenu inutile avec la modification du yield de l'algoG, la génération 0 sera renvoyée en première et triée.
nbArmeesPremiersPourAnalyse = 2

for i in range(10):
    population = next(G)
    addData(comptesCommuns,compteurArmees(population))
    addData(comptesDesPremiers,compteurArmees(population[:nbArmeesPremiersPourAnalyse]))
    print("###################################\n###### Génération",i,"terminée ######\n###################################")

outData(comptesCommuns,"Tests AlgoG/[24-03-2017]#1.csv",'"{nbArmees=10;nbGeneration=50}{select=all;mutation=20%-100%;croisement=60%-100%}tempsPris='+str(time.time()-T_debut)+' (newAstar)"')
outData(comptesDesPremiers,"Tests AlgoG/[24-03-2017]#1.2 (2 premières armées uniquement).csv",'"{nbArmees=10;nbGeneration=50}{select=all;mutation=20%-100%;croisement=60%-100%}tempsPris='+str(time.time()-T_debut)+' (newAstar)"')




