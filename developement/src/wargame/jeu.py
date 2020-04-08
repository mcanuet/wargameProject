import pickle

class Jeu(object):

    def __init__(self,joueurs,typeJoueurs,plateau,dossierSauvegarde=""):
        """
        Représentation d'un jeu, facilitant ainsi le système de tour à tour, la bonne prise en compte des potentielles modifications de règle dans tout les modules faisant appel à un jeu, plus de maléabilité notamment sur le nombre de joueurs dans une partie ou encore sur les règles de jeu appliquée etc.
        
        :param joueurs: Liste des joueurs, pour le wargame : Liste des armées s'affrontant
        :type joueurs: list or tuple
        :param typeJoueurs: Correspond à la liste d'objets correspondant aux joueurs. Par exemple, l'élément de liste correspondant à un joueur humain sera l'objet associé à celui-ci lui permettant d'effectuer les fonctions déplacements, attaques ou autre. Pour une IA, cela correspond à l'objet associé à ce dernier, par exemple bebeBeel regroupant les fonctions de déplacement, d'attaque, etc.
        :type typeJoueurs: list or tuple
        :param plateau: Plateau sur lequel se joueront les affrontements.
        :type plateau: Plateau object
        :param dossierSauvegarde: Chemin du dossier regroupant les sauvegardes d'une partie.
        :type dossierSauvegarde: str
        """
        self.joueurs = joueurs
        self.typeJoueurs = typeJoueurs
        self.plateau = plateau
        self.tour = 0
        self.dossierSauvegarde = dossierSauvegarde

    def start(self):
        pass

    def tourSuivant(self):
        self.tour = self.tour+1

    def jouerTour(self):
        joueur = self.tour%len(self.joueurs)
        #Correspond par exemple à IA.#          #Ici, pourri parce que les fonctions d'IA limité à 2 joueurs
        self.typeJoueurs[joueur].deplacerUnites(self.plateau,joueur,(self.tour+1)%len(self.joueurs),self.joueurs)
        #Pareil
        self.typeJoueurs[joueur].attaqueAuto(self.plateau,(self.tour+1)%len(self.joueurs),joueur,self.joueurs)

    def isEnd(self,joinNumberWinner=False):
        if all(i.compo!={} for i in self.joueurs):
            return False
        else:
            if not joinNumberWinner:
                return True
            else:
                #Spécifique à un 1VS1
                if self.joueurs[0].compo!={}:
                    return True,0
                else:
                    return True,1
        
    def sauvegarder(self):
        file = open(self.dossierSauvegarde+"/"+str(time.strftime('%d.%m.%y-%H.%M',time.localtime())),"wb")
        monPickler = pickle.Pickler(file)
        monPickler.dump(self)
        file.close()

    def load(save):
        file = open(save,"rb")
        monDepickler = pickle.Unpickler(file)
        monJeu = monDepickler.load()
        file.close()
        return monJeu
