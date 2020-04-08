from algorithmes.AlgoG import AlgorithmeGenetique
from optimisateur.tournois import tournois
import pickle



f = open("armeeia/humains.save","rb")
md = pickle.Unpickler(f)
listA = md.load()
