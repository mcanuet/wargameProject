#Version : 0.2.0

class Plateau(object):

    def __init__(self,largeur = 20,hauteur = 20):
        self.troupes = []   #Contient les troupes et leur position etc...
        self.terrain = []   #A déterminer le code/codage des types de terrains
        self.creerGrille(largeur,hauteur)

    def __repr__(self):     #Sert surtout pour la représentation console
        txt=""
        for i in range(len(self.terrain)):
            txt+="|"
            for j in range(len(self.terrain[i])):
                if self.terrain[i][j]!=int(1):
                    txt+=" "+str(self.terrain[i][j])
                elif self.troupes[i][j]!=int(1):
                    txt+=" "+str(self.troupes[i][j])
                else :
                    txt+=" 1"
            txt+=" |\n"

        return txt

    def creerGrille(self,largeur = 20,hauteur = 20,caseVide = 1):
        """
        Génère des grilles pour troupes et terrain de dimensions largeur et hauteur voulues.

        :param largeur: Largeur de la grille, correspond aux coordonnées X.
        :type largeur: int
        :param hauteur: Hauteur de la grille, correspond aux coordonnées Y.
        :type hauteur: int
        """
        #Réinitialise si besoin
        self.troupes = [caseVide]*hauteur  #Les 1 permettent une traduction plus simple de case/chemin libre, notamment pour l'Algorithme A*
        self.terrain = [caseVide]*hauteur

        for i in range(hauteur):
            self.troupes[i] = [caseVide]*largeur
            self.terrain[i] = [caseVide]*largeur


    def supprimerUnite(self,x,y,caseVide = 1):
        """
        Supprime une unité du plateau, utile notamment lorsqu'une unité meurt.

        :param x: Coordonnée X à laquelle supprimer l'unité.
        :type x: int
        :param y: Coordonnée Y à laquelle supprimer l'unité.
        :type y: int
        :param caseVide: Valeur correspondant à une case vide, permet donc de remplacer l'unité par cette valeur.
        :type caseVide: int/str (Tout dépend du choix réalisé, par défaut vaut 1)
        """
        if 0 <= x < len(self.troupes[0]) and 0 <= y < len(self.troupes):
            self.troupes[y][x] = caseVide
        else:
            raise Exception("Coordonnées en dehors des limites possibles")

    def grilleObstacle(self,xd,yd,portee):   #Rajouter la condition comme quoi si c'est la même armée, le déplacement est possible
        """
        Renvoie une grille ne contenant que des 1 (Cases accessibles) et des 0 (Obstacles/Cases innaccessibles).

        :param xd: Coordonnée X à laquelle se situe l'unité concernée par un déplacement.
        :type xd: int
        :param yd: Coordonnée Y à laquelle se situe l'unité concernée par un déplacement.
        :type yd: int
        """
        grille = []
        XD,YD = xd-portee,yd-portee
        
        for i in range(portee*2+1):   #Pour chaque ligne
            ligne = []
            for j in range(portee*2+1):  #Pour chaque colonne
                if YD+i < 0 or YD+i >= len(self.troupes) or XD+j < 0 or XD+j >= len(self.troupes[0]):   #Si les coordonnées obtenues ne sont pas valide (coordonnées hors plateau), on applique l'équivalent d'un obstacle
                    ligne.append(0)
                elif self.troupes[YD+i][XD+j] == self.terrain[YD+i][XD+j]:
                    ligne.append(1)
                else:
                    ligne.append(0)
            grille.append(ligne)
        return grille

if __name__ == "__main__":
    P = Plateau(5,5)
    class U(object):
        def __init__(self):
            self.deplacement = 3    #Pour le moment, marche pour 2 mais pas pour 3 (qui est trop proche du bord)
        def __repr__(self):
            return "U"
    P.troupes[2][2] = U()
    print(P)
    P.deplacement(2,2,3,3)
    print(P)
    #Gérer lorsque l'on est sur le bord du plateau















