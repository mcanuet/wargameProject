#Version : 1.0.0
from random import shuffle
from math import floor


def AlgorithmeGenetique(population,fctSelection=None,fctCroisement=None,fctMutation=None,specificArgsSelection={},specificArgsCroisement={},specificArgsMutation={},inputSelection="*",outputPerSelection="*",outputSelection="*",ifInputSelectionUnsatisfied="*",inputCroisement="*",outputPerCroisement="*",outputCroisement="*",ifInputCroisementUnsatisfied="*",inputMutation="*",outputPerMutation="*",outputMutation="*",ifInputMutationUnsatisfied="*",ordreTri="décroissant",backData=False,*args,**kw):
    """
    AlgorithmeGenetique prend la forme d'un générateur afin de répondre à un maximum de besoin différent, par exemple pour se stopper lorsque l'on tend vers une armée unique, pour continuer indéfinimément etc... En récupérant facilement l'état de la population aux générations voulues

    :param population: Population d'Armées avec lesquels effectuer l'Algorithme Génétique.
    :type population: list of Armee objects
    :param fctSelection: Fonction (à renseigner) gérant la phase de sélection de l'Algorithme. Pour le Wargame, la fonction tournois peut être utilisée comme sélection
    :type fctSelection: function
    :param fctCroisement: Fonction (à renseigner) gérant la phase de croisement de l'Algorithme.
    :type fctCroisement: function
    :param fctMutation: Fonction (à renseigner) gérant la phase de mutation de l'Algorithme.
    :type fctMutation: function
    :param specificArgsSelection: Arguments à transmettre spécifiquement à la fonction sélection. Par exemple, pour la fonction sélection tournois, un argument backData est présent, de même que pour AlgorithmeGenetique. Avec AlgorithmeGenetique(backData=True), backData sera appliqué pour tournois et AlgorithmeGenetique (ainsi que les autres fonctions prenant cet argment) tandis qu'avec AlgorithmeGenetique(specificArgsSelection={"backData":True}), backData ne sera appliqué qu'à la fonction sélection tournois. L'argument doit être renseigné de la manière {"ARGUMENT":VALEUR} (sans oublier les guillements pour les clés)
    :type specificArgsSelection: dict
    :param specificArgsCroisement: Arguments à transmettre spécifiquement à la fonction de croisement. Voir explications sur l'argument specificArgsSelection.
    :type specificArgsCroisement: dict
    :param specificArgsMutation: Arguments à transmettre spécifiquement à la fonction de mutation. Voir explications sur l'argument specificArgsSelection.
    :type specificArgsMutation: dict
    :param inputSelection: Donnée indiquant la quantité de population à introduire par appel à la fonction de sélection. Peut prendre les valeurs "*", "all" ou du type entier "100" (=100 premiers éléments de la population sont introduit) ou encore du type entier suivi du signe pourcent "60%" (=60% des premiers éléments de la population sont introduit).
    :type inputSelection: str (With value constraints)
    :param outputSelection: Donnée indiquant la quantité de population à garder à la sortie de la fonction de sélection. Peut prendre les valeurs "*", "all" ou du type entier "100" (=100 premiers éléments de la population sont retournées) ou encore du type entier suivi du signe pourcent "60%" (=60% des premiers éléments de la population sont retournées). Peut aussi prendre pour valeur un entier négatif (= -5 signifie que toute la population est retournée excepté les 5 derniers éléments).
    :type outputSelection: str (With value constraints)
    :param ifInputSelectionUnsatisfied: Donnée indiquant que faire si la donnée relative à l'entrée (inputSelection) dans la fonction de sélection n'est pas satisfaisable, faute d'un nombre insuffisant de la population restante. Ces valeurs peuvent être "*" (=Entrer toutes les données restantes dans la fonction), "+" (=Préserver les éléments restant dans la population, sans les faire passer dans la fonction) ou "-" (=Supprimer les éléments restants de la population, sans les faire passer dans la fonction).
    :type ifInputSelectionUnsatisfied: str (With value constraints)
    :param inputCroisement: Donnée indiquant la quantité de population à introduire par appel à la fonction de croisement. Peut prendre les valeurs "*", "all" ou du type entier "100" (=100 premiers éléments de la population sont introduit) ou encore du type entier suivi du signe pourcent "60%" (=60% des premiers éléments de la population sont introduit).
    :type inputCroisement: str (With value constraints)
    :param outputCroisement: Donnée indiquant la quantité de population à garder à la sortie de la fonction de croisement. Peut prendre les valeurs "*", "all" ou du type entier "100" (=100 premiers éléments de la population sont retournées) ou encore du type entier suivi du signe pourcent "60%" (=60% des premiers éléments de la population sont retournées). Peut aussi prendre pour valeur un entier négatif (= -5 signifie que toute la population est retournée excepté les 5 derniers éléments).
    :type outputCroisement: str (With value constraints)
    :param ifInputCroisementUnsatisfied: Donnée indiquant que faire si la donnée relative à l'entrée (inputCroisement) dans la fonction de croisement n'est pas satisfaisable, faute d'un nombre insuffisant de la population restante. Ces valeurs peuvent être "*" (=Entrer toutes les données restantes dans la fonction), "+" (=Préserver les éléments restant dans la population, sans les faire passer dans la fonction) ou "-" (=Supprimer les éléments restants de la population, sans les faire passer dans la fonction).
    :type ifInputCroisementUnsatisfied: str (With value constraints)
    :param inputMutation: Donnée indiquant la quantité de population à introduire par appel la fonction de mutation. Peut prendre les valeurs "*", "all" ou du type entier "100" (=100 premiers éléments de la population sont introduit) ou encore du type entier suivi du signe pourcent "60%" (=60% des premiers éléments de la population sont introduit).
    :type inputMutation: str (With value constraints)
    :param outputMutation: Donnée indiquant la quantité de population à garder à la sortie de la fonction de mutation. Peut prendre les valeurs "*", "all" ou du type entier "100" (=100 premiers éléments de la population sont retournées) ou encore du type entier suivi du signe pourcent "60%" (=60% des premiers éléments de la population sont retournées). Peut aussi prendre pour valeur un entier négatif (= -5 signifie que toute la population est retournée excepté les 5 derniers éléments).
    :type outputMutation: str (With value constraints)
    :param ifInputMutationUnsatisfied: Donnée indiquant que faire si la donnée relative à l'entrée (inputMutation) dans la fonction de mutation n'est pas satisfaisable, faute d'un nombre insuffisant de la population restante. Ces valeurs peuvent être "*" (=Entrer toutes les données restantes dans la fonction), "+" (=Préserver les éléments restant dans la population, sans les faire passer dans la fonction) ou "-" (=Supprimer les éléments restants de la population, sans les faire passer dans la fonction).
    :type ifInputMutationUnsatisfied: str (With value constraints)
    :param ordreTri: Ordre du tri automatique (Si conditions respectées) réalisé, prend pour valeur "croissant" ou "décroissant". Un tri automatique est réalisé à la fin des fonctions renseignées (avec appel unique ou multiples, suite à une segmentation) si la syntaxe suivante est respectée : {"score":scoreAssociéIntOuFloat,"element":elementDeLaPopulation} (=Correspond à 1 élément de la population, les données transmises au tri sont donc une liste d'éléments ayant cette syntaxe).
    :type ordreTri: str (With value constraints)
    :param backData: Si True, retourne les données en plus de la population obtenue
    :type backData: boolean

    :note: Les fonctions fctSelection, fctCroisement et fctMutation se déclanchent dans le même ordre qu'elles viennent d'être citées. Pour changer cet ordre, changer simplement l'ordre de renseignement des fonctions (et autres attributs spécifiques), par exemple fctSelection=maFonctionDeMutation etc...
    :note: Le 21/03/2017, le yield du générateur AlgorithmeGénétique a été déplacé juste après la fonction de sélection, obtenant ainsi la population classée (et non modifié leur donnant un ordre hasardeux). La génération 0 correspond donc à la population initiale mais dans l'ordre du plus fort au plus faible.
    """

    ##Tests si les arguments renseignés permettent le bon déroulement de l'Algorithme (Ne test pas pour les fonctions de Sélection, Croisement et Mutation)
    if not fctSelection and not fctCroisement and not fctMutation:raise AttributeError("Au moins l'une des fonctions suivantes doit être renseignée pour faire évoluer l'Algorithme Génétique : fctSelection, fctCroisement, fctMutation")
    if not all(i == None or callable(i) for i in [fctSelection,fctCroisement,fctMutation]):raise AttributeError("fctSelection, fctCroisement et fctMutation doivent être des fonctions (sinon de valeur None)")
    #Test des inputSelection/outputSelection ...
    if not all(i in ["*","+","-"] for i in [ifInputSelectionUnsatisfied,ifInputCroisementUnsatisfied,ifInputMutationUnsatisfied]):raise AttributeError('Un attribut ifInput...Unsatisfied est incorrect, les données valide sont "*", "+" et "-"')
    ##FAIRE LA MÊME POUR LES INPUT ET OUTPUT
    if not all(isinstance(i,dict) for i in [specificArgsSelection,specificArgsCroisement,specificArgsMutation]):raise AttributeError("specificArgsSelection, specificArgsCroisement et specificArgsMutation doivent être des instances de dict")


    while True:

        ##Condition d'arrêt, notamment pour l'utiliser dans une boucle for i in ...
        if population == []:raise StopIteration

        ##Mélange pour que, par exemple dans la fonction de Sélection, les mêmes armées ne soient pas toujours ensemble lorsque population est travaillée morceau par morceaux
        shuffle(population)

        ##Phase de Sélection
        if fctSelection:
            print("Fonction sélection :",len(population),"armées")
            populationSegmente,reste = segmentation(population,inputSelection,ifInputSelectionUnsatisfied)  #Segmentation de la population, résultat du type [[Armee1,Armee2],[Armee3,Armee4],[Armee5]]
            argsSelection = fusionDict(specificArgsSelection,kw)                                            #Arguments spécifié par monArg=saValeur ainsi que ceux transmis par specificArgsSelection={"monArg":saValeur}
            population = []                                                                                 #Variable population réinitialisé, le travail de (re)remplissage se fera à l'aide de populationSegmente
            for i in populationSegmente:
                part, reste = segmentation(fctSelection(i,*args,**argsSelection),outputPerSelection,reste=reste,typeSeg="output")
                population.extend(part)              #Ajout de la population en sortie de fonction dans la population totale
            if population and isinstance(population[0],dict) and len(population[0])==2 and "score" in population[0] and "element" in population[0]:    #Test toutes les conditions d'un tri "auto"
                population = tri(population,ordreTri)                                                                                   #Le tri ne laisse que les éléments "element" de la population triée
            population,reste = segmentation(population,outputSelection,reste=reste,typeSeg="output")
            #print("POP:",population,"\nREST:",reste)
            print("Fonction fin sélection :",len(population),"armées sélectionnées + ",len(reste),"armées restantes")
            population.extend(reste)    #Reste correspond au reste laissé par segmentation. Si ifInputSelectionUnsatisfied = "*", "all" ou "-" alors reste = [] donc rien ne sera ajouté à population. Si ifInputSelectionUnsatisfied = "+", le reste de la population (n'ayant pu constituer une segmentation complète) est ajouté dans la population sans passer par la fonction.

        yield population

        ##Phase de croisement
        if fctCroisement:
            print("Fonction croisement :",len(population),"armées")
            populationSegmente,reste = segmentation(population,inputCroisement,ifInputCroisementUnsatisfied)#Segmentation de la population, résultat du type [[Armee1,Armee2],[Armee3,Armee4],[Armee5]]
            #print("populationSeg :",populationSegmente,"\nreste :",reste)
            argsCroisement = fusionDict(specificArgsCroisement,kw)                                          #Arguments spécifié par monArg=saValeur ainsi que ceux transmis par specificArgsSelection={"monArg":saValeur}
            population = []                                                                                 #Variable population réinitialisé, le travail de (re)remplissage se fera à l'aide de populationSegmente
            #print("###POPULATION SEGMENTE DU CROISEMENT:",populationSegmente,"\n###RESTE:",reste)
            for i in populationSegmente:
                part, reste = segmentation(fctCroisement(i,*args,**argsCroisement),outputPerCroisement,reste=reste,typeSeg="output")
                population.extend(part)           #Ajout de la population en sortie de fonction dans la population totale
            if population and isinstance(population[0],dict) and len(population[0])==2 and "score" in population[0] and "element" in population[0]:    #Test toutes les conditions d'un tri "auto"
                population = tri(population,ordreTri)                                                                                   #Le tri ne laisse que les éléments "element" de la population triée
            population,reste = segmentation(population,outputCroisement,reste=reste,typeSeg="output")
            print("Fonction fin croisement :",len(population),"armées croisées + ",len(reste),"armées restantes")
            population.extend(reste)    #Reste correspond au reste laissé par segmentation. Si ifInputSelectionUnsatisfied = "*", "all" ou "-" alors reste = [] donc rien ne sera ajouté à population. Si ifInputSelectionUnsatisfied = "+", le reste de la population (n'ayant pu constituer une segmentation complète) est ajouté dans la population sans passer par la fonction.

        ##Phase de mutation
        if fctMutation:
            print("Fonction mutation :",len(population),"armées")
            populationSegmente,reste = segmentation(population,inputMutation,ifInputMutationUnsatisfied)    #Segmentation de la population, résultat du type [[Armee1,Armee2],[Armee3,Armee4],[Armee5]]
            argsMutation = fusionDict(specificArgsMutation,kw)                                              #Arguments spécifié par monArg=saValeur ainsi que ceux transmis par specificArgsSelection={"monArg":saValeur}
            population = []                                                                                 #Variable population réinitialisé, le travail de (re)remplissage se fera à l'aide de populationSegmente
            for i in populationSegmente:
                part, reste = segmentation(fctMutation(i,*args,**argsMutation),outputPerMutation,reste=reste,typeSeg="output")
                population.extend(part)                 #Ajout de la population en sortie de fonction dans la population totale
            if population and isinstance(population[0],dict) and len(population[0])==2 and "score" in population[0] and "element" in population[0]:    #Test toutes les conditions d'un tri "auto"
                population = tri(population,ordreTri)                                                                                   #Le tri ne laisse que les éléments "element" de la population triée
            population,reste = segmentation(population,outputMutation,reste=reste,typeSeg="output")
            print("Fonction fin mutation :",len(population),"armées mutées + ",len(reste),"armées restantes")
            population.extend(reste)    #Reste correspond au reste laissé par segmentation. Si ifInputSelectionUnsatisfied = "*", "all" ou "-" alors reste = [] donc rien ne sera ajouté à population. Si ifInputSelectionUnsatisfied = "+", le reste de la population (n'ayant pu constituer une segmentation complète) est ajouté dans la population sans passer par la fonction.


        #Déplacé après la fonction de sélection : yield population




def fusionDict(d1,d2):
    """
    Permet la fusion de 2 dictionnaires d1 et d2 pour l'AlgorithmeGenetique.

    Si des clés sont présentes dans d1 et d2 à la fois, leur valeur n'est pas fusion, d1 étant le dictionnaire "prioritaire", seul sa/ses valeurs seront retenu.

    :param d1: Dictionnaire numéro 1 à fusionner. Celui-ci est le dictionnaire prioritaire, c'est à dire que si des clés sont présentes dans les 2 dictionnaires, seul les valeurs de d1 seront retenues.
    :type d1: dict
    :param d2: Dictionnaire numéro 2 à fusionner. Celui-ci est un dictionnaire secondaire, si des clés lui appartenant sont déjà dans d1, celles-ci seront ignorées au profit de celles présentes dans d1.
    :type d2: dict
    """
    d1,d2 = d1.copy(),d2.copy()
    for i in d2:
        if not d1.get(i,None):
            d1[i] = d2[i]
    return d1

def segmentation(population,segment="50%",segmentFailed="+",typeSeg="input",reste=[],*args,**kw):
    """
    Segmente une population donnée en fonction des paramètres prédéfini ou à définir.

    :param population: Population d'éléments, autrement dit une liste d'éléments.
    :type population: list
    :param segment: Définition d'un segment (ou partition). Peut prendre les valeurs : "*", "all", nombre entier (sous forme str) ou pourcentage (sous forme str). Peut aussi prendre un nombre entier négatif si typeSeg="output".
    :type segment: str
    :param segmentFailed: Définit que faire si une segmentation (ou partition) ne peut être complète, faute d'un nombre insuffisant d'éléments dans la population. Peut prendre les valeurs "*" ou "all" (=Les éléments restants sont tout de même renvoyés en tant que segment "complet"), "+" (=Les éléments restants sont préservés pour rejoindre la population ultérieurement) ou "-" (=Les éléments restants sont ignorés donc l'équivalent d'être supprimés).
    :type segmentFailed: str
    :param typeSeg: Permet de réaliser des segments en entrée comme en sortie. En entrée, la population est segmenté en différentes parties quant à la Sortie, on pourrait parler plutôt d'une troncature de la population.
    :type typeSeg: str

    :note: [MAJ 09/03/2017] +Ajout d'une segmentation plus large par interval, exemple: 10-20-40-50 va prendre les éléments 10 à 20 et 40 à50, ou encore 0%-33%-66%-100% (=0%-33%-66%) va prendre le premier et le dernier tier de la population.
                            +Ajout d'un "mode" de sélection aléatoire via l'ajout d'un "~" devant la méthode de segmentation (entier, pourcentage ou encore par intervalle).
    """

    #Suppression des potentiels espaces inutiles, permet une compréhensible plus large des segmentations entrées par l'utilisateur
    segment = segment.replace(" ","")

    #Application de l'aléatoire pour les segmentations par entier ou pourcentage contenant le préfixe "~"
    if segment[0] == "~":
        shuffle(population)
        segment = segment[1:]

    ##On ne reteste pas les valeurs de (ici) segment et segmentFailed, on les supposes correct et/ou vérifié dans AlgorithmeGenetique
    if typeSeg == "input":
        ##Valeurs possible de segment : "*", "all", nombre entier (sous forme str) ou pourcentage
        if segment in ["*","all"]:return [population],[]
        #Cas des intervalles
        elif (segment.count("-") >= 2 or segment[1:].count("-")==1) and all(i in ["0","1","2","3","4","5","6","7","8","9","%","-"] for i in segment):
            intervalles = segment.split("-")
            ##print("Intervalle de base :",intervalles)
            #Traitement des cas utilisant des raccourcis tels que "-20%" (="0%-20%") ou bien les cas de couple incomplet se fermant automatiquement à 100% tels que "10%-20%-80%" (="10%-20%-80%-100%")
            if intervalles[0] == "" : intervalles[0] = "0"
            if intervalles[-1] == "" : intervalles[-1] = str(len(population))
            if len(intervalles)%2 : intervalles.append(str(len(population)))
            ##print("Après gestion des extrêmités :",intervalles)
            #Convertion des pourcentages en entiers
            for i in range(len(intervalles)):
                #Pour les cas où n = k + 0.5, k un entier, python fait un arrondi "bancaire" autrement dit vers le nombre pair le plus proche. On ajoute "+0.0000001" afin d'avoir un réel arrondi (k+0.5 sera donc arrondi au plus haut)
                if intervalles[i][-1] == "%" :
                    ##print((len(population)),"*",(int(intervalles[i][:-1])/100),"=",str(round((len(population))*(int(intervalles[i][:-1])/100)+0.0000001)),"("+str((len(population))*(int(intervalles[i][:-1])/100)+0.0000001)[:5]+")")
                    intervalles[i] = str(round((len(population))*(int(intervalles[i][:-1])/100)+0.0000001))
            ##print("Convertion entiers :",intervalles)
            #Fusionnement de certains points inutiles, notamment à cause des arrondis lors du passage % à int. Exemple sur une liste de longueur 6 (indice 0 à 5): "20%-60%-65%-80%" = "1-3-3-4" = "1-4". Cas particulier (notamment sur les extrêmités) : "60%-65%-80%" (=60%-65%-80%-100%) = "3-3-4" = "4" soit "4-5" avec l'auto-complétion des couples. "0%-20%-25%-80%" = "0-1-1-4" = "0-4". "20%-25%" = "4-4" = ""
                #(Suite des cas) Cas d'intervalles successifs : "0%-40%-60%-100%" = "0-2-3-5" = "0-5" (Il n'existe pas d'élément entre les indices 2 et 3, on joint donc les 2 intervalles)
            #Gestion des doublons (Premier cas)
            intervallesClean = []
            decalage = 0
            for i in range(len(intervalles)):
                if i+decalage >= len(intervalles)-1:
                    ##print("\ti+decalage >= longueur des intervalles, ajout de l'élément",intervalles[-1])
                    intervallesClean.append(intervalles[-1])
                    break
                elif intervalles[i+decalage] == intervalles[i+decalage+1]:
                    ##print("\tDoublons détecté, incrémentation du décalage")
                    decalage += 1
                else:
                    ##print("\tPas de problème détecté, ajout de l'élément",intervalles[i+decalage])
                    intervallesClean.append(intervalles[i+decalage])
            intervalles = intervallesClean[:]
            ##print("Suppression des doublons :",intervalles)
            #Gestion des intervalles successifs (Second cas)
            if len(intervalles) >= 2:
                intervallesClean = [intervalles[0],intervalles[1]]
                for i in range(len(intervalles)-3):
                    if int(intervalles[1+2*i])+1 == int(intervalles[2+2*i]) :
                        ##print("\tContiguité détectée :",intervallesClean[-1],"remplacé par",intervalles[2+2*i])
                        intervallesClean[-1] = intervalles[3+2*i]
                    else : intervallesClean.extend([intervalles[2+2*i],intervalles[3+2*i]])
                intervalles = intervallesClean[:]
            else:   #Taille 0 ou 1, autrement dit ensemble vide
                return [],[population]
            ##print("Jointure des ensembles contigus :",intervalles)
            #Formation de la population segmenté et du reste (Eléments hors des intervalles)
            listeDesIndicesParIntervalles = [list(range(int(j[0]),int(j[1]))) for j in [(intervalles[i*2],intervalles[1+i*2]) for i in range(int(len(intervalles)/2))]]
            #print("Indices par intervalles :",listeDesIndicesParIntervalles)
            listeDesIndices = []
            for i in listeDesIndicesParIntervalles : listeDesIndices.extend(i)
            #print("Indices :",listeDesIndices)

            populationSegmente, reste = [], []
            for i in range(len(population)):
                if i in listeDesIndices:
                    populationSegmente.append(population[i])
                else:
                    reste.append(population[i])
            
            return [populationSegmente], reste

        #Cas des pourcentages
        elif segment[-1] == "%" and all(i in ["0","1","2","3","4","5","6","7","8","9"] for i in segment[:-1]):
            quantiteParSegment = round((int(segment[:-1])/100)*len(population))     #Discutable de remplacer round() par floor()
        #Cas des entiers
        elif all(i in ["0","1","2","3","4","5","6","7","8","9"] for i in segment):
            quantiteParSegment = int(segment)
        else:raise Exception("L'attribut 'segment' renseigné n'est pas compréhensible par la fonction segmentation")

        populationSegmente,reste = [],[]
        ##On ajoute segment par segment
        for i in range(floor(len(population)/quantiteParSegment)):
            populationSegmente.append(population[:quantiteParSegment])
            population = population[quantiteParSegment:]

        ##On traite les potentiels derniers éléments de la population
        if len(population)!=0:
            ##Valeurs possible de segmentFailed : "*", "all", "+" ou "-"
            if segmentFailed in ["*","all"]:
                populationSegmente.append(population[:])
            elif segmentFailed == "+":
                reste = population[:]
            elif segmentFailed == "-":
                pass    #Rien ne se passe, le 'reste' n'est pas renvoyé donc supprimé.
            else:raise Exception("L'attribut 'segmentFailed' doit prendre uniquement pour valeur '*', 'all', '+' ou '-'")

        return populationSegmente,reste


    elif typeSeg == "output":
        #print("#SEGMENTATION OUTPUT")
        #print("population (entrée du output):",population, "\nreste (entrée du output):",reste)
        ##Valeurs possible de segment : "*", "all", nombre entier (sous forme str) ou pourcentage ou entier négatif
        if segment in ["*","all"]:return population,reste
        elif (segment.count("-") >= 2 or segment[1:].count("-")==1) and all(i in ["0","1","2","3","4","5","6","7","8","9","%","-"] for i in segment):
            #print("##PAR INTERVALLES")
            intervalles = segment.split("-")
            ##print("Intervalle de base :",intervalles)
            #Traitement des cas utilisant des raccourcis tels que "-20%" (="0%-20%") ou bien les cas de couple incomplet se fermant automatiquement à 100% tels que "10%-20%-80%" (="10%-20%-80%-100%")
            if intervalles[0] == "" : intervalles[0] = "0"
            if intervalles[-1] == "" : intervalles[-1] = str(len(population)+len(reste))
            if len(intervalles)%2 : intervalles.append(str(len(population)+len(reste)))
            ##print("Après gestion des extrêmités :",intervalles)
            #Convertion des pourcentages en entiers
            for i in range(len(intervalles)):
                #Pour les cas où n = k + 0.5, k un entier, python fait un arrondi "bancaire" autrement dit vers le nombre pair le plus proche. On ajoute "+0.0000001" afin d'avoir un réel arrondi (k+0.5 sera donc arrondi au plus haut)
                if intervalles[i][-1] == "%" :
                    ##print((len(population)),"*",(int(intervalles[i][:-1])/100),"=",str(round((len(population))*(int(intervalles[i][:-1])/100)+0.0000001)),"("+str((len(population))*(int(intervalles[i][:-1])/100)+0.0000001)[:5]+")")
                    intervalles[i] = str(round((len(population)+len(reste))*(int(intervalles[i][:-1])/100)+0.0000001))
            ##print("Convertion entiers :",intervalles)
            #Fusionnement de certains points inutiles, notamment à cause des arrondis lors du passage % à int. Exemple sur une liste de longueur 6 (indice 0 à 5): "20%-60%-65%-80%" = "1-3-3-4" = "1-4". Cas particulier (notamment sur les extrêmités) : "60%-65%-80%" (=60%-65%-80%-100%) = "3-3-4" = "4" soit "4-5" avec l'auto-complétion des couples. "0%-20%-25%-80%" = "0-1-1-4" = "0-4". "20%-25%" = "4-4" = ""
                #(Suite des cas) Cas d'intervalles successifs : "0%-40%-60%-100%" = "0-2-3-5" = "0-5" (Il n'existe pas d'élément entre les indices 2 et 3, on joint donc les 2 intervalles)
            #Gestion des doublons (Premier cas)
            intervallesClean = []
            decalage = 0
            for i in range(len(intervalles)):
                if i+decalage >= len(intervalles)-1:
                    ##print("\ti+decalage >= longueur des intervalles, ajout de l'élément",intervalles[-1])
                    intervallesClean.append(intervalles[-1])
                    break
                elif intervalles[i+decalage] == intervalles[i+decalage+1]:
                    ##print("\tDoublons détecté, incrémentation du décalage")
                    decalage += 1
                else:
                    ##print("\tPas de problème détecté, ajout de l'élément",intervalles[i+decalage])
                    intervallesClean.append(intervalles[i+decalage])
            intervalles = intervallesClean[:]
            ##print("Suppression des doublons :",intervalles)
            #Gestion des intervalles successifs (Second cas)
            if len(intervalles) >= 2:
                intervallesClean = [intervalles[0],intervalles[1]]
                for i in range(len(intervalles)-3):
                    if int(intervalles[1+2*i])+1 == int(intervalles[2+2*i]) :
                        ##print("\tContiguité détectée :",intervallesClean[-1],"remplacé par",intervalles[2+2*i])
                        intervallesClean[-1] = intervalles[3+2*i]
                    else : intervallesClean.extend([intervalles[2+2*i],intervalles[3+2*i]])
                intervalles = intervallesClean[:]
            else:   #Taille 0 ou 1, autrement dit ensemble vide
                return [],[population+reste]
            ##print("Jointure des ensembles contigus :",intervalles)
            #Formation de la population segmenté et du reste (Eléments hors des intervalles)
            listeDesIndicesParIntervalles = [list(range(int(j[0]),int(j[1]))) for j in [(intervalles[i*2],intervalles[1+i*2]) for i in range(int(len(intervalles)/2))]]
            #print("Indices par intervalles :",listeDesIndicesParIntervalles)
            listeDesIndices = []
            for i in listeDesIndicesParIntervalles : listeDesIndices.extend(i)
            #print("Indices :",listeDesIndices)

            newPopulation = []
            for i in range(len(population)+len(reste)):
                #print("Population restante:",len(population),"\treste:",len(reste))
                if i in listeDesIndices:
                    if population:  #En cas de mauvaise utilisation par l'utilisateur
                        newPopulation.append(population[0])
                        del population[0]
                else:
                    if reste:       #En cas de mauvaise utilisation par l'utilisateur
                        newPopulation.append(reste[0])
                        del reste[0]
            #print("NEWPOP:",newPopulation,"\nRESTE:",reste+population)
            return newPopulation, reste+population
        elif segment[-1] == "%" and all(i in ["0","1","2","3","4","5","6","7","8","9"] for i in segment[:-1]):
            #print("##PAR SEGMENT POURCENT")
            quantiteDuSegment = round((int(segment[:-1])/100)*len(population))     #Discutable de remplacer round() par floor()
            return population[:quantiteDuSegment],reste
        elif all(segment[i] in ["0","1","2","3","4","5","6","7","8","9"] or (i==0 and segment[i]=="-") for i in range(len(segment))):
            #print("##PAR SEGMENT VALEUR ENTIERE")
            return population[:int(segment)],reste
        else:raise Exception("L'attribut 'segment' renseigné n'est pas compréhensible par la fonction segmentation")
    else:raise TypeError("typeSeg doit prendre uniquement pour valeur 'input' ou bien 'output'")


def tri(population,ordre="décroissant"):
    """
    Tri prend en argument une population dont chaque élément sont des dictionnaires du type : {"score":int/floatValue,"element":elementDeLaPopulation}. Le tri peut se faire dans l'ordre croissant ou décroissant des scores. Seulement les éléments de la population sont renvoyés.

    :param population: Liste, ou tuple, composé de dictionnaires du type {"score":int/floatValue,"element":elementDeLaPopulation}.
    :type population: list of dict
    :param ordre: Prend la valeur "croissant" ou "décroissant". Permet d'indiquer l'ordre dans lequel trier les éléments de la population en fonction des scores.
    :type ordre: str

    :note: Croissant et Décroissant trient en fonction des scores. Si vous souhaitez trier dans l'ordre du plus haut score (tendant potentiellement vers l'infini positif), choisissez donc l'ordre 'decroissant' (Conventionnellement correspondant au nombre le plus grand au plus petit)
    """
    if ordre not in ["croissant","décroissant"]:raise ValueError("L'argument 'ordre' doit prendre pour valeur 'croissant' ou 'décroissant'")

    listeScore = []
    for i in population:
        score = i.get("score",None)
        if score==None:   # == None pour éviter les ambiguïtés avec des scores nuls ou même négatif (Donc non utilisation de False ou encore -1 comme valeur retour du i.get())
            raise ValueError("Au moins un élément de la population ne comporte pas de score")
        else:
            listeScore.append(score)
    listeScore.sort()

    if ordre != "croissant":
        listeScore.reverse()

    newPopulation = []
    for i in listeScore:
        for j in population:
            if j["score"]==i:
                newPopulation.append(j["element"])
                population.remove(j)
    return newPopulation



def testSegmentation():
    return segmentation(["a","b","c","d","e","f","g","h","i"],"0%-33%-66%")

def testSegmentation2():
    population,reste = segmentation(["a","b","c","d","e","f","g","h","i"],"0%-33%-66%")
    return segmentation(population,"0%-33%-66%",reste=reste,typeSeg="output")


if __name__ == "__main__":
    p = [1,2,3,4,5,6,7,8,9,10]
    def T(x):
        X = [{"score":i,"element":i} for i in x]
        return X
    print("Pour réaliser un test, vous pouvez utiliser la population p (nombre de 1 à 10 inclus) ainsi que la fonction T (qui renvoie l'entrée).")
