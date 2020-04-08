import pickle

def lecteur(file):
	fichier=open(file,"rb")
	lecture=pickle.load(fichier)
	print(lecture)
	fichier.close()

if __name__=="__main__":
	file=None
	while file!="stop":
		file=input("quel fichier doit être ouvert (stop pour arréter le programme) ?: ")
		try :
			lecteur(file)
		except:
			pass
