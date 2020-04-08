#Version : 1.1.0
#Mis-à-jour : Modification de l'heuristique et ajout de tests
from time import *

class Sommet(object):

    def __init__(self, x, y, F, predecesseur = None):

        self.x = x
        self.y = y
        self.F = F
        self.predecesseur = predecesseur

    def __repr__(self):
        if self.predecesseur == None:
            precedent = "None"
        else:
            precedent = "("+str(self.predecesseur.x)+","+str(self.predecesseur.y)+")"
        return "("+str(self.x)+","+str(self.y)+")  F = "+str(self.F)+"  prédécesseur = "+precedent
    
        



def vieuxAstar(grille, depart, arrivee, direction = [(1,0), (-1,0), (0,1), (0,-1)]):
    """
    :param grille: Grille contenant nécessairement le point de départ et le point d'arrivé. Au mieux, cette grille est seulement d'une largeur/hauteur correspondant au déplacement maximal de l'unité de départ. Cette grille ne doit contenir que des 1 (chemin possible) et des 0 (obstacles).
    :type grille: list
    :param depart: Coordonnées x,y de départ du chemin à réaliser.
    :type depart: tuple
    :param arrivee: Coordonnées x,y d'arrivée du chemin à réaliser.
    :type arrivee: tuple
    :param direction: Directions possible à partir d'une case. Exemple: [(1,0),(-1,0),(0,1),(0,-1)]
    :type direction: list of tuple
    """

    #Variables présentes
    #depart : Sommet source
    #arrivee : Sommet destination
    #E : Liste des sommets à explorer, par défaut contient depart
    #V : Liste des sommets visités, par défaut vide
    #X : Sommet, ou liste des sommets, le(s) plus court(s)
    #x et y les coordonnées d'un sommet
    #F le coût de déplacement entre le point de départ et l'arrivée
    #predecesseur le pointeur vers le sommet précédent du chemin en cours
    #newCoord : Variable temporaire permettant d'analyser les cases adjacentes à celle (la case) en cours d'analyse
    #FIN : Si None, aucun chemin n'est possible, sinon lance le retraçage du chemin
    #precedent: Variable temporaire permettant de "remonter" le chemin arrivé à la cible voulue
    #Chemin : Liste des coordonnées des sommets par lequel le chemin passe

    arrivee = Sommet(arrivee[0], arrivee[1], 0)
    depart = Sommet(depart[0], depart[1], 0, None)
    E = [depart]
    V = []

    while E != [] and (arrivee.x,arrivee.y) not in [(A.x,A.y) for A in E]:
        # print("E : ",E)
        #Récupération du sommet X de coût F minimum
        X = None
        for i in E:
            if X==None or i.F < X.F:
                X = i

        #Ajout de X à la liste V, donc on l'enlève de E
        E.remove(X)
        V.append(X)

        V_coords = [(i.x,i.y) for i in V]   #Permet des comparaisons de sommet plus facilement à l'aide de leurs coordonnées

        #Ajout des successeurs de X (non visités) à la liste E
        for i in direction:
            #Si les coordonnées appartiennent bien à la grille donnée
            if i[0]+X.x >= 0 and i[0]+X.x < len(grille[0]) and i[1]+X.y >= 0 and i[1]+X.y < len(grille):
                #Si ces coordonnées ne correspondent pas à un obstacle
                if grille[i[1]+X.y][i[0]+X.x]:
                                                            #Heuristique précédent + 1 (=déplacement) + Distance Manathan jusqu'à fin - Distance Manathan jusqu'à fin du précédent
                    newCoord = Sommet(i[0]+X.x, i[1]+X.y, ((V[-1].F+1)+abs(i[0]+X.x-arrivee.x)+abs(i[1]+X.y-arrivee.y)-(abs(V[-1].x-arrivee.x)+abs(V[-1].y-arrivee.y))), V[-1])
                    #Si ces coordonnées n'ont pas déjà été visité
                    if (newCoord.x,newCoord.y) not in V_coords:
                        #Si successeurs déjà dans E, et coût F inférieur au successeur déjà présent, alors remplacer coût et successeur
                        if (newCoord.x,newCoord.y) in [(k.x,k.y) for k in E]:
                            for j in E:
                                if (newCoord.x,newCoord.y) == (j.x,j.y):
                                    if newCoord.F < j.F:
                                        j.F = newCoord.F
                                        j.predecesseur = newCoord.predecesseur

                        else:
                            E.append(newCoord)

    #Récupération du chemin
    FIN = None
    for i in E:
        if (i.x,i.y) == (arrivee.x,arrivee.y):
            FIN = i

    #Si FIN n'est pas None, donc qu'un chemin existe bien
    if FIN:
        precedent = FIN.predecesseur
        Chemin = [(FIN.x,FIN.y,"Heuristique:"+str(FIN.F))]
        while precedent != None:
            Chemin.append((precedent.x,precedent.y,"Heuristique:"+str(precedent.F)))
            precedent = precedent.predecesseur
        Chemin.reverse()
        Chemin = Chemin[1:] #On supprime les coordonnées de départ
        #Test
        print('gentil astar')
        return Chemin
    else:
        print('astar de merde')
        return False



def test1():
    """
    Test 2 chemins, l'un d'eux s'éloigne dans un premier et peut aller directement sur la cible ensuite, il est le chemin le plus court, le second se rapproche directement de la cible en premier lieu puis passe quelques obstacle faisant de lui le chemin plus long.
    """
    return Astar([[1,1,1,1,1,1,1,1,1,1,1],[1,0,1,1,1,1,1,1,1,1,1],[1,0,1,1,1,1,1,1,1,1,1],[1,0,1,1,1,1,1,1,1,1,1],[1,0,0,1,1,1,1,1,1,1,1],[1,0,0,0,1,1,1,1,1,1,1],[1,0,0,0,0,1,1,1,1,1,1],[1,0,1,1,1,0,1,1,1,1,1],[1,0,1,0,1,0,0,1,1,1,1],[1,0,1,0,1,0,1,1,1,1,1],[1,1,1,0,1,1,1,0,0,1,1]],(0,2),(10,10))

def test2():
    """
    Cherche un chemin sur une zone sans obstacle
    """
    return Astar([[1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1]],(0,2),(10,10))

def test3():
    """
    Cherche un chemin entre le départ et l'arrivée, une ligne d'obstacle empêche le déplacement
    """
    return Astar([[1,1,1,1,1,0,1,1,1,1,1],[1,1,1,1,1,0,1,1,1,1,1],[1,1,1,1,1,0,1,1,1,1,1],[1,1,1,1,1,0,1,1,1,1,1],[1,1,1,1,1,0,1,1,1,1,1],[1,1,1,1,1,0,1,1,1,1,1],[1,1,1,1,1,0,1,1,1,1,1],[1,1,1,1,1,0,1,1,1,1,1],[1,1,1,1,1,0,1,1,1,1,1],[1,1,1,1,1,0,1,1,1,1,1],[1,1,1,1,1,0,1,1,1,1,1]],(0,2),(10,10))

def grandTest():
    pla=[1]*20
    for i in range(len(pla)) :
        pla[i]=[1]*20
    print(pla)
    return Astar(pla,[1,1],[18,18])

def TestTimeAstarDefaut(n=100):
    total = [0,0,0]
    for i in range(n):
        t = time()
        test1()
        total[0] += time()-t
        t = time()
        test2()
        total[1] += time()-t
        t = time()
        test3()
        total[2] += time()-t
    total2 = (total[0]/n,total[1]/n,total[2]/n)
    return (total,total2)













##############TEST D'OPTIMISATION#################

class Sommet2(object):

    def __init__(self, valeur, x, y, F = None, predecesseur = None):
        self.valeur = valeur
        self.x = x
        self.y = y
        self.F = F
        self.predecesseur = predecesseur

    def __repr__(self):
        if self.predecesseur == None:
            precedent = "None"
        else:
            precedent = "("+str(self.predecesseur.x)+","+str(self.predecesseur.y)+")"
        return "("+str(self.x)+","+str(self.y)+") valeur = "+str(self.valeur)+"  F = "+str(self.F)+"  prédécesseur = "+precedent
 

def Astar(grille, depart, arrivee, direction = [(1,0), (-1,0), (0,1), (0,-1)]):
    """
    :param grille: Grille contenant nécessairement le point de départ et le point d'arrivé. Au mieux, cette grille est seulement d'une largeur/hauteur correspondant au déplacement maximal de l'unité de départ. Cette grille ne doit contenir que des 1 (chemin possible) et des 0 (obstacles).
    :type grille: list
    :param depart: Coordonnées x,y de départ du chemin à réaliser.
    :type depart: tuple
    :param arrivee: Coordonnées x,y d'arrivée du chemin à réaliser.
    :type arrivee: tuple
    :param direction: Directions possible à partir d'une case. Exemple: [(1,0),(-1,0),(0,1),(0,-1)]
    :type direction: list of tuple
    """

    #Variables présente
    #depart : Sommet source
    #arrivee : Sommet destination
    #E : Liste des sommets à explorer, par défaut contient depart
    #V : Liste des sommets visités, par défaut vide
    #X : Sommet, ou liste des sommets, le(s) plus court(s)
    #x et y les coordonnées d'un sommet
    #F le coût de déplacement entre le point de départ et l'arrivée
    #predecesseur le pointeur vers le sommet précédent du chemin en cours
    #newCoord : Variable temporaire permettant d'analyser les cases adjacentes à celle (la case) en cours d'analyse
    #FIN : Si None, aucun chemin n'est possible, sinon lance le retraçage du chemin
    #precedent: Variable temporaire permettant de "remonter" le chemin arrivé à la cible voulue
    #Chemin : Liste des coordonnées des sommets par lequel le chemin passe


    ###Convertion de la grille 0/1 en grille d'objets sommets
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            grille[i][j] = Sommet2(grille[i][j],j,i)

    Arrivee = grille[arrivee[1]][arrivee[0]]    #Plus pratique pour récupérer les coordonnées d'arrivée après
    grille[depart[1]][depart[0]].F = 0
    E = [grille[depart[1]][depart[0]]]
    V = []

    while E != [] and grille[arrivee[1]][arrivee[0]] not in E:
        # print("E : ",E)
        #Récupération du sommet X de coût F minimum
        X = None
        for i in E:
            if X==None or i.F < X.F:
                X = i

        #Ajout de X à la liste V, donc on l'enlève de E
        E.remove(X)
        V.append(X)

        """OK jusqu'ici"""

        V_coords = [(i.x,i.y) for i in V]   #Permet des comparaisons de sommet plus facilement à l'aide de leurs coordonnées

        #Ajout des successeurs de X (non visités) à la liste E
        for i in direction:
            #Si les coordonnées appartiennent bien à la grille donnée
            if i[0]+X.x >= 0 and i[0]+X.x < len(grille[0]) and i[1]+X.y >= 0 and i[1]+X.y < len(grille):
                """Ok"""
                #Si ces coordonnées ne correspondent pas à un obstacle
                if grille[i[1]+X.y][i[0]+X.x].valeur:
                    """Jusqu'ici ok"""
                                                            #Heuristique précédent + 1 (=déplacement) + Distance Manathan jusqu'à fin - Distance Manathan jusqu'à fin du précédent
                    #newCoord = Sommet2(i[0]+X.x, i[1]+X.y, ((V[-1].F+1)+abs(i[0]+X.x-Arrivee.x)+abs(i[1]+X.y-Arrivee.y)-(abs(V[-1].x-Arrivee.x)+abs(V[-1].y-Arrivee.y))), V[-1])
                    newCoord = grille[i[1]+X.y][i[0]+X.x]
                    #Si ces coordonnées n'ont pas déjà été visité
                    if newCoord not in V:
                        #Si successeurs déjà dans E, et coût F inférieur au successeur déjà présent, alors remplacer coût et successeur
                        if newCoord in E:
                            for j in E:
                                if (newCoord.x,newCoord.y) == (j.x,j.y):
                                    if ((V[-1].F+1)+abs(i[0]+X.x-Arrivee.x)+abs(i[1]+X.y-Arrivee.y)-(abs(V[-1].x-Arrivee.x)+abs(V[-1].y-Arrivee.y))) < j.F:
                                        j.F = ((V[-1].F+1)+abs(i[0]+X.x-Arrivee.x)+abs(i[1]+X.y-Arrivee.y)-(abs(V[-1].x-Arrivee.x)+abs(V[-1].y-Arrivee.y)))
                                        j.predecesseur = V[-1]

                        else:
                            #print("newCoord.F : ",newCoord.F,"\nArrivee : ",Arrivee,"\ni : ",i,"\nV : ",V)
                            newCoord.F = ((V[-1].F+1)+abs(i[0]+X.x-Arrivee.x)+abs(i[1]+X.y-Arrivee.y)-(abs(V[-1].x-Arrivee.x)+abs(V[-1].y-Arrivee.y)))
                            newCoord.predecesseur = V[-1]
                            E.append(newCoord)
    """Normalement Ok jusqu'ici"""

    #Récupération du chemin
    FIN = None
    for i in E:
        if (i.x,i.y) == (Arrivee.x,Arrivee.y):
            FIN = i

    #Si FIN n'est pas None, donc qu'un chemi existe bien
    if FIN:
        precedent = FIN.predecesseur
        Chemin = [(FIN.x,FIN.y,"Heuristique:"+str(FIN.F))]
        while precedent != None:
            Chemin.append((precedent.x,precedent.y,"Heuristique:"+str(precedent.F)))
            precedent = precedent.predecesseur
        Chemin.reverse()
        Chemin = Chemin[1:] #On supprime les coordonnées de départ
        #Test
        return Chemin
    else:
        return False


def test11():
    """
    Test 2 chemins, l'un d'eux s'éloigne dans un premier et peut aller directement sur la cible ensuite, il est le chemin le plus court, le second se rapproche directement de la cible en premier lieu puis passe quelques obstacle faisant de lui le chemin plus long.
    """
    return Astar2([[1,1,1,1,1,1,1,1,1,1,1],[1,0,1,1,1,1,1,1,1,1,1],[1,0,1,1,1,1,1,1,1,1,1],[1,0,1,1,1,1,1,1,1,1,1],[1,0,0,1,1,1,1,1,1,1,1],[1,0,0,0,1,1,1,1,1,1,1],[1,0,0,0,0,1,1,1,1,1,1],[1,0,1,1,1,0,1,1,1,1,1],[1,0,1,0,1,0,0,1,1,1,1],[1,0,1,0,1,0,1,1,1,1,1],[1,1,1,0,1,1,1,0,0,1,1]],(0,2),(10,10))

def test21():
    """
    Cherche un chemin sur une zone sans obstacle
    """
    return Astar2([[1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1]],(0,2),(10,10))

def test31():
    """
    Cherche un chemin entre le départ et l'arrivée, une ligne d'obstacle empêche le déplacement
    """
    return Astar2([[1,1,1,1,1,0,1,1,1,1,1],[1,1,1,1,1,0,1,1,1,1,1],[1,1,1,1,1,0,1,1,1,1,1],[1,1,1,1,1,0,1,1,1,1,1],[1,1,1,1,1,0,1,1,1,1,1],[1,1,1,1,1,0,1,1,1,1,1],[1,1,1,1,1,0,1,1,1,1,1],[1,1,1,1,1,0,1,1,1,1,1],[1,1,1,1,1,0,1,1,1,1,1],[1,1,1,1,1,0,1,1,1,1,1],[1,1,1,1,1,0,1,1,1,1,1]],(0,2),(10,10))


def TestTimeNewAstar(n=100):
    total = [0,0,0]
    for i in range(n):
        t = time()
        test11()
        total[0] += time()-t
        t = time()
        test21()
        total[1] += time()-t
        t = time()
        test31()
        total[2] += time()-t
    total2 = (total[0]/n,total[1]/n,total[2]/n)
    return (total,total2)

