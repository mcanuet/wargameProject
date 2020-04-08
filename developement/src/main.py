#Version : 0.1.0
#Imports normaux
from random import *
from time import *
from pprint import *

#Anciens imports
#from plateau import *
#from Astar import *
#from unite import *
#from interface import *
#from bebeBeel import *

##Nouvelles importations des modules
##from ia import *
##from algorithmes import *
##from wargame import *
##from gui.interface import *
from wargame.plateau import *
from algorithmes.Astar import *
from ia.bebeBeel import *
from ia.IAmedium import *
from wargame import unite
from wargame.jeu import Jeu

#creér des armées
#ajouté des unité dans l'armée 

typeJoueurs=[]#input("Type de joueur : "),input("Type de joueur : ")
contenuArmees=[]
Victory=False
Tours=0
dicoref=unite.Dicoref()
t=time()



def creaArmee():
    """
    Fonction qui demande au joueur une race puis nombre d'unités afin de constituer une fière et grande armée pour la bataille
    """
    for i in range(2):

        if typeJoueurs[i] == "humain" :
            race = ""
            while race not in dicoref.dico:
                race=CreerArmee.quelle_armee()

            stop = False
            A = Armee(race)

            while not stop:
                U = CreerArmee.quelle_unitee()
                if U == "":
                    stop = True
                else:
                    try:
                        addUnite(A,U,dicoref)
                    except ValueError:
                        print("Prix de l'unité trop élevé !")
                    except :
                        print("Unité inexistante !")


            contenuArmees.append(A)

        elif typeJoueurs[i]=="IA0" :#test le numéro d'AI pour savoir quel méthode utiliser
            contenuArmees.append(bebeBeel.creationArmee())

def placeArmees():
    """
    Demande au joueur des coordonnées pour placer chacune des unités constituant sa liste d'armée
    """
    for r in range(2):
        if typeJoueurs[r]=="humain":
            for j in range(len(contenuArmees[r].compo)):
                x,y=int(input("Entrez la coordonnées x où placer l'unité "+str(contenuArmees[r].compo[j])+" ")),int(input("Entrez la coordonnées y où placer l'unité "+str(contenuArmees[r].compo[j])+" "))
                while p.troupes[x][y] != 1 or p.terrain[x][y] != 1 :
                    x,y=int(input("Entrez la coordonnées x où placer l'unité "+str(contenuArmees[r].compo[j])+" ")),int(input("Entrez la coordonnées y où placer l'unité "+str(contenuArmees[r].compo[j])+" "))
                contenuArmees[r].compo[j].placerUnite(p,x,y)

        elif typeJoueurs[r]=="IA0" :#test le numéro d'AI pour savoir quel méthode utiliser
            bebeBeel.placerUnites(p,r,contenuArmees)



def deplacementArmee(joueur):
    """
    Fonction qui demande au joueur des coordonées pour déplacer ses unités les unes après les autres
    """
    if joueur ==0:
        ennemi=1
    else :
        ennemi=0
    if typeJoueurs[joueur]=="humain":
        for j in range(len(contenuArmees[joueur].compo)):
            x,y=int(input("Entrez la coordonnées x où déplacer l'unité "+str(contenuArmees[joueur].compo[j])+" ")),int(input("Entrez la coordonnées y où déplacer l'unité "+str(contenuArmees[joueur].compo[j].nom)+" "))
            if (x,y) != contenuArmees[joueur].compo[j].coord :
                while p.troupes[y][x] != 1 or p.terrain[y][x] != 1 :
                    x,y=int(input("Entrez la coordonnées x où déplacer l'unité "+str(contenuArmees[joueur].compo[j])+" ")),int(input("Entrez la coordonnées y où déplacer l'unité "+str(contenuArmees[joueur].compo[j].nom)+" "))
                contenuArmees[joueur].compo[j].deplacement(p,x,y)

    elif typeJoueurs[joueur]=="IA0" :#test le numéro d'AI pour savoir quel méthode utiliser
        bebeBeel.deplacerUnites(p,ennemi,joueur,contenuArmees)


def attaquer(joueur):
    """
    fonction qui demande au joueur quelle unité ennemie attaquer pour chacune de ses unités ayant la possibilité d'attaquer
    """
    if joueur ==0:
        ennemi=1
    else :
        ennemi=0
    if typeJoueurs[joueur]=="humain":
        for j in range(len(contenuArmees[joueur].compo)):
            uniteAttaquante=contenuArmees[joueur].compo[j]
            cibles=uniteAttaquante.ennemisAPortee(p,ennemi,contenuArmees) 
            defenseur=[]
            if cibles != []:
                defenseur=input("Entres les cooronnées x,y que vous souhaitez vous attaquer avec votre "+str(uniteAttaquante)+" : "+str(cibles))

                dist=abs(int(defenseur[0])-uniteAttaquante.coord[0])+abs(int(defenseur[-1])-uniteAttaquante.coord[-1])
                if uniteAttaquante.testPrecision(dist):
                    if not p.troupes[int(defenseur[-1])][int(defenseur[0])].testEsquive():
                        p.troupes[int(defenseur[-1])][int(defenseur[0])].supprimerPV(uniteAttaquante.calculDegats())    
                        if p.troupes[int(defenseur[-1])][int(defenseur[0])].pv <= 0 :
                            del contenuArmees[ennemi].compo[p.troupes[int(defenseur[-1])][int(defenseur[0])].num]
                            p.troupes[int(defenseur[-1])][int(defenseur[0])]=1

    elif typeJoueurs[joueur]=="IA0" :#test le numéro d'AI pour savoir quel méthode utiliser
        bebeBeel.attaqueAuto(p,joueur,ennemi,contenuArmees)


if __name__== "__main__":
    armee0,armee1=0,0
    while time()-t<2:
        contenuArmees=[]
        Victory=False
        Tours=0
        p=Plateau(20,20)
        typeJoueurs=["IA0","IA0"]
        creaArmee()
        #print(contenuArmees)
        placeArmees()
        # print(p.troupes)
##        while contenuArmees[0].compo != {} and contenuArmees[1].compo != {} :
##            if Tours%2==0:
##                deplacementArmee(0)
##                attaquer(0)
##                Tours+=1
##            else :
##                deplacementArmee(1)
##                attaquer(1)
##                Tours+=1
##                
##        #print(p)
##
##        if contenuArmees[0].compo == {}:
##            armee1+=1
##        else:
##            armee0+=1
        jeu = Jeu(contenuArmees,(IAmedium,IAmedium),p)
        while not jeu.isEnd():
                jeu.jouerTour()
                jeu.tourSuivant()

        numGagnant = jeu.isEnd(True)[1]
        if numGagnant:
                armee1 += 1
        else:
                armee0 += 1
        
    print(armee0+armee1,"parties ",armee0,"/",armee1,"Temps:",str(time()-t))
