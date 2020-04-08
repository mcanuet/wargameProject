#Imports normaux
from pprint import *
from random import *
from time import *
import pickle
from copy import deepcopy
import os
import json

#Pour ajouter le dossier parent dans le Path et pouvoir tout importer
import sys
sys.path.append('../')

#Nouveaux imports
from wargame.plateau import *
from algorithmes.Astar import *
from ia.bebeBeel import *
from wargame import unite
from wargame.jeu import Jeu




def tournois(population,IA=bebeBeel,jeu=Jeu,plateaux=Plateau(20,20),nbVersions=5,save=None,backData=False,joinScore=False,*args,**kw):  # *args et **kw pour palier aux potentiels problèmes via l'Algo G (Gestion de l'ensemble des arguments à repartager entre les fonctions de sélection, mutation et croisement)
    """
    La fonction tournois provoque des combats entre chaque armée d'une population donnée. Chaque armée s'affrontera nbVersions fois sur le ou l'un des plateau(x) renseigné(s) dans plateaux via les propriétés associées à l'IA renseignée.
    Des données peuvent être récupérées puis stockées dans un fichier si un chemin "save" est renseignée ou bien par retour de l'appel de la fonction en précisant True pour backData.
    Dans tout les cas, une population est retournée (donc seule, ou en indice 0 si backData vaut True), celle-ci est triée dans l'ordre de l'armée ayant fait le meilleur score à celle ayant fait le plus faible score.

    :param population: Population d'Armées avec lesquelles effectuer le tournoi.
    :type population: list of Armee objects
    :param IA: IA avec laquelle produire ce tournoi. Doit contenir les méthodes : placerUnite(3 args), deplacerUnites(3 args) et attaqueAuto(3 args).
    :type IA: object (IA with methods in description)
    :param plateaux: Plateau ou liste de Plateau sur laquelle/lesquelles le Tournoi peut se disputer.
    :type plateaux: list of Plateau objects or single Plateau object
    :param nbVersions: Nombre de versions d'un combat, autrement dit nombre de fois qu'une Armée i et une Armée j se combattent. Appliquer plusieurs versions permet de diminuer la chance de victoire par le hasard.
    :type nbVersions: int
    :param save: Si un chemin est renseigné, les données du tournoi seront stockées dans le dossier spécifié. /!\ Le chemin de destination doit être vers un DOSSIER et non un FICHIER.
    :type save: None or str
    :param backData: Si True, retourne les données en plus de la population obtenue
    :type backData: boolean
    :param joinScore: Indique si les scores doivent être joint aux éléments de la population (Notamment pour refaire un tri ultérieur).
    :type joinScore: boolean
    """

    data = {}       #Plus pratique pour passer à du JSON via le module json
    graine=0

    victoires = [0]*len(population) #population équivaux à l'ancien listArmees issu de fichierArmees
    for i in range(len(population)):
        for k in range(len(population)-i):      # -i pour gérer les doublets
            if i != (k+i):      #Pas suffisant, là on fait les combats Armeei vs Armeek ET Armeek vs Armeei, ce sont les mêmes.
                victoiresi=0
                victoiresk=0
                subData = {"armee"+str(i):{"composition":population[i].json(),"race":population[i].armee},
                       "armee"+str(k+i):{"composition":population[k+i].json(),"race":population[k+i].armee}}  #Correspond à un "combatNUM"
                for j in range(nbVersions):
                    ##Début d'un combat (Ou l'une des versions d'un combat entre Armées i et k)

                    #Remplissage des données JSON
                    subSubData = {"seed":graine}

                    #Graine itérée à la fin de chaque combat
                    seed(graine)
                    #Conteneur, temporaire, des 2 armées adverses
                    contenuArmees=[deepcopy(population[i]),deepcopy(population[k+i])]
                    #Application du Plateau par imposition ou par hasard dans une liste
                    if isinstance(plateaux,Plateau):
                        p=deepcopy(plateaux)
                    else:   #Sinon une liste de Plateau
                        p=deepcopy(plateaux[randint(0,len(plateaux))])
                    #Création d'un référencement des Tours et positionnement des unités
                    Tours=0
                    IA.placerUnites(p,0,contenuArmees)
                    IA.placerUnites(p,1,contenuArmees)

                    #Déroulement d'un combat
##                    while contenuArmees[0].compo != {} and contenuArmees[1].compo != {} :
##
##                        if Tours%2==0:
##                            IA.deplacerUnites(p,1,0,contenuArmees)
##                            IA.attaqueAuto(p,0,1,contenuArmees)
##                            Tours+=1
##                        else :
##                            IA.deplacerUnites(p,0,1,contenuArmees)
##                            IA.attaqueAuto(p,1,0,contenuArmees)
##                            Tours+=1
##                    if contenuArmees[0].compo == {}:
##                        victoiresk+=1
##                    else :
##                        victoiresi+=1

                    partie = jeu(contenuArmees,(IA,IA),p)
                    while not partie.isEnd():
                        partie.jouerTour()
                        partie.tourSuivant()

                    numGagnant = partie.isEnd(True)[1]
                    if numGagnant:
                        victoiresk+=1
                    else:
                        victoiresi+=1

                    #Itération de la graine pour le(s) combat(s) suivant
                    graine+=1
                    #Remplissage des données JSON
                    subSubData["armee"+str(i)] = contenuArmees[0].json()
                    subSubData["armee"+str(k+i)] = contenuArmees[1].json()
                    name = str(j)
                    if j <= 9: name = "0"+name
                    subData[name] = subSubData
                name = str(len(data))
                if len(data) <= 9: name = "0"+name
                data["combat"+name] = subData
                if victoiresk > victoiresi:
                    victoires[k+i] += victoiresk/(victoiresk+victoiresi)        #Modification du += 1 en ceci pour avoir une meilleure moyenne des victoires
                else :
                    victoires[i] += victoiresi/(victoiresk+victoiresi)          #Même modif'
    if save :
        #Création du dossier de destination si besoin
        if not os.path.isdir(save):
            os.makedirs(save)
        #Puis on stocke les données
        file = open(save+"/"+str(len(os.listdir(save)))+".json","w")     #Chaque fichier prend pour nom un numéro équivalent au nombre de fichiers déjà existant, ainsi aucun n'aura le même (Sauf intervention humaine)
        file.write(json.dumps(data))
        file.close()

    ##Tri de l'armée à plus haut score au plus faible pour le retour de population
    #Création du dico clé=score valeur=numéro de l'armée (Permet ensuite de trier par score et d'aller rechercher rapidement l'index de l'armée concernée)
    dicoTri = {victoires[i]:i for i in range(len(victoires))}
    dicoTri={}
    for i in range(len(victoires)):
        if not victoires[i] in dicoTri:
            dicoTri[victoires[i]]=[i]
        else :
            dicoTri[victoires[i]].append(i)



    triScore = list(dicoTri.keys())
    triScore.sort()
    triScore.reverse()
    if joinScore:
        newPopulation = []
        for i in triScore:
            for j in dicoTri[i]:
                newPopulation.append({"score":i,"element":population[j]})
        population = newPopulation
    else:
        population = [population[dicoTri[int(i)]] for i in triScore]
        newPopulation = []
        for i in triScore:
            for j in dicoTri[i]:
                newPopulation.append(population[j])
        population = newPopulation
    #population = list(zip(population,triScore))

    ##Gestion du return
    if backData:return (population,data)        #Si une demande de retour des données est appliquée
    else:return population                      #Sinon on renvoie simplement la population finale /!\ FAIRE UN TRIAGE DU MEILLEUR SCORE AU PLUS FAIBLE

if __name__=="__main__":
    #tournois("humains")
    f = open("../armeeia/humains.save","rb")
    md = pickle.Unpickler(f)
    listA = md.load()
    listB = listA+listA
