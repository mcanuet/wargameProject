#Import classique
import pygame
from pygame.locals import *
from random import *
from time import *

#Pour ajouter le dossier parent dans le Path et pouvoir tout importer
import sys
sys.path.append('../')

#Nouveaux imports
from wargame.plateau import *
from algorithmes.Astar import *
from wargame import unite

contenuArmees=[]
Victory=False
Tours=0
p=Plateau(20,20)
typeJoueurs=["",""]
dicoref=unite.Dicoref()
t=time()

#objet pour image, text et sond

class image():

	def __init__(self,chemin):
		self.image=pygame.image.load(chemin).convert_alpha()
		self.pos=self.image.get_rect()

class maketext():

	def __init__(self,txt,color,fontsize):
		self.text=txt
		self.font=pygame.font.Font("ressources/font/asgard.ttf",fontsize)
		self.size=self.font.size(self.text)
		self.ren=self.font.render(self.text,0,color)

class sound():

	def __init__(self,chemin):
		self.son=pygame.mixer.Sound(chemin)



#--- couleur 
black=(0,0,0)
white=(255,255,255)
red=(255, 102, 102)
green=(0,255,0)
blue=(153, 153, 255)
grey=(120,120,120)
trueRed=(255,0,0)


#1 ----------------launch screen--------------
def launchScreen(launch,fen):

	while launch:

		#images pour l'écran
		fond=image("ressources/img/fond.png")
		jouerbut=image("ressources/img/jouer.png")
		quitbut=image("ressources/img/quitter.png")

		#position de base des images
		jouerbut.pos=jouerbut.pos.move(520,350)
		quitbut.pos=quitbut.pos.move(1100,620)

		# son pour l'écran

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()

			if event.type==MOUSEBUTTONUP:
				pos=event.pos

				if quitbut.pos.collidepoint(pos):
					pygame.quit()

				if jouerbut.pos.collidepoint(pos):
					launch=False
					return launch

		fen.blit(fond.image,fond.pos)
		fen.blit(jouerbut.image,jouerbut.pos)
		fen.blit(quitbut.image,quitbut.pos)
		pygame.display.update()

#2 ---------choix des types de joueur------------------
typeJoueurs=["",""]
def playerTypeChoiceScreen(playerTypeChoice,fen):
		
		#images pour l'écran
		quitbut=image("ressources/img/quitter.png")

		if typeJoueurs[0]!="ia":
			humainimg=image("ressources/img/humain.png")
		if typeJoueurs[0]!="humain":
			ia0img=image("ressources/img/ia0.png")
			ia1img=image("ressources/img/ia1.png")
			ia2img=image("ressources/img/ia2.png")
		if typeJoueurs[1]!="ia":
			humainimg2=image("ressources/img/humain.png")
		if typeJoueurs[1]!="humain":
			ia0img2=image("ressources/img/ia0.png")
			ia1img2=image("ressources/img/ia1.png")
			ia2img2=image("ressources/img/ia2.png")

		# position des images
		quitbut.pos=quitbut.pos.move(1100,0)

		if typeJoueurs[0]=="":
			humainimg.pos=humainimg.pos.move(200,50)
			ia0img.pos=ia0img.pos.move(600,50)
			ia1img.pos=ia1img.pos.move(600,155)
			ia2img.pos=ia2img.pos.move(820,100)
		if typeJoueurs[1]=="":
			humainimg2.pos=humainimg2.pos.move(200,350)
			ia0img2.pos=ia0img2.pos.move(600,360)
			ia1img2.pos=ia1img2.pos.move(600,465)
			ia2img2.pos=ia2img2.pos.move(820,415)

		# texte pour l'écran
		j1=maketext("joueur 1:",white,25)
		j2=maketext("joueur 2:",white,25)
		
		# son pour l'écran

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()

			if event.type==MOUSEBUTTONUP:
				pos=event.pos

				if quitbut.pos.collidepoint(pos):
					pygame.quit()

				if typeJoueurs[0]=="" and humainimg.pos.collidepoint(pos):
					typeJoueurs[0]="humain"

				if typeJoueurs[0]=="" and ia0img.pos.collidepoint(pos):
					typeJoueurs[0]="IA0"

				if typeJoueurs[0]=="" and ia1img.pos.collidepoint(pos):
					typeJoueurs[0]="IA1"

				if typeJoueurs[0]=="" and ia2img.pos.collidepoint(pos):
					typeJoueurs[0]="IA2"
				
				#------

				if typeJoueurs[1]=="" and humainimg2.pos.collidepoint(pos):
					typeJoueurs[1]="humain"

				if typeJoueurs[1]=="" and ia0img2.pos.collidepoint(pos):
					typeJoueurs[1]="IA0"

				if typeJoueurs[1]=="" and ia1img2.pos.collidepoint(pos):
					typeJoueurs[1]="IA1"

				if typeJoueurs[1]=="" and ia2img2.pos.collidepoint(pos):
					typeJoueurs[1]="IA2"

		# réinitialisation de la fenêtre
		fen.fill(grey)
		
		# teste des choix pour afficher un text si choisie
		if typeJoueurs[0]=="":
			fen.blit(j1.ren,(10,150))
			fen.blit(humainimg.image,humainimg.pos)
			fen.blit(ia0img.image,ia0img.pos)
			fen.blit(ia1img.image,ia1img.pos)
			fen.blit(ia2img.image,ia2img.pos)
		# ---
		if typeJoueurs[1]=="" and typeJoueurs[0]!="":
			fen.blit(j2.ren,(10,450))
			fen.blit(humainimg2.image,humainimg2.pos)
			fen.blit(ia0img2.image,ia0img2.pos)
			fen.blit(ia1img2.image,ia1img2.pos)
			fen.blit(ia2img2.image,ia2img2.pos)

		if typeJoueurs[0]!="":
			choixJ1=maketext("le choix pour j1 est: "+typeJoueurs[0],white,30)
			fen.blit(choixJ1.ren,(400,150))
			# ---
		if typeJoueurs[1]!="":
			choixJ2=maketext("le choix pour j2 est: "+typeJoueurs[1],white,30)
			fen.blit(choixJ2.ren,(400,550))

		# ---
		fen.blit(quitbut.image,quitbut.pos)
		pygame.display.update()

		# teste pour le passage à la fenêtre suivante
		if typeJoueurs[0]!="" and typeJoueurs[1]!="":
			return False,typeJoueurs

#3 --------écran de fabrication des armées-----------

def raceScreen(fen):
	
	race=""

	#images fixe pour l'écran
	quitbut=image("ressources/img/quitter.png")
	# position des images
	quitbut.pos=quitbut.pos.move(1100,0)

	while True:

		# son pour l'écran

		if race=="":
			#--- images
			humainsimg=image("ressources/img/race/humains.png")
			nainsimg=image("ressources/img/race/nains.png")
			demonsimg=image("ressources/img/race/demons.png")
			orksimg=image("ressources/img/race/orks.png")
			elfesimg=image("ressources/img/race/elfes.png")
			#position images
			humainsimg.pos=humainsimg.pos.move(200,250)
			nainsimg.pos=nainsimg.pos.move(500,250)
			demonsimg.pos=demonsimg.pos.move(800,250)
			orksimg.pos=orksimg.pos.move(350,450)
			elfesimg.pos=elfesimg.pos.move(650,450)
			#--- texte
			txt1=maketext("choisissez une race :",white,42)

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()

			if event.type==MOUSEBUTTONUP:
				pos=event.pos
				
				if quitbut.pos.collidepoint(pos):
					pygame.quit()

				if race=="":
					if humainsimg.pos.collidepoint(pos):
						 race="humains"
					if nainsimg.pos.collidepoint(pos):
						 race="nains"
					if demonsimg.pos.collidepoint(pos):
						 race="demons"
					if orksimg.pos.collidepoint(pos):
						 race="orks"
					if elfesimg.pos.collidepoint(pos):
						 race="elfes"


		# réinitialisation de la fenêtre
		fen.fill(grey)
		if race=="":
			#collage sur la fenêtre
			fen.blit(humainsimg.image,humainsimg.pos)
			fen.blit(nainsimg.image,nainsimg.pos)
			fen.blit(demonsimg.image,demonsimg.pos)
			fen.blit(orksimg.image,orksimg.pos)
			fen.blit(elfesimg.image,elfesimg.pos)
			# collage du text
			fen.blit(txt1.ren,(20,20))
		else:
			return race

		fen.blit(quitbut.image,quitbut.pos)
		pygame.display.update()

#-------------------------écran de choix des unités 

def uniteScreen(race,soldeArmee,fen):
	uniteChoisie=[]
	soldeRestant=soldeArmee

	#images fixe pour l'écran
	quitbut=image("ressources/img/quitter.png")
	add0=image("ressources/img/+.png")
	add1=image("ressources/img/+.png")
	add2=image("ressources/img/+.png")
	add3=image("ressources/img/+.png")
	add4=image("ressources/img/+.png")
	add5=image("ressources/img/+.png")
	add6=image("ressources/img/+.png")

	sub0=image("ressources/img/-.png")
	sub1=image("ressources/img/-.png")
	sub2=image("ressources/img/-.png")
	sub3=image("ressources/img/-.png")
	sub4=image("ressources/img/-.png")
	sub5=image("ressources/img/-.png")
	sub6=image("ressources/img/-.png")

	nbu0=0
	nbu1=0
	nbu2=0
	nbu3=0
	nbu4=0 
	nbu5=0
	nbu6=0

	stopimg=image("ressources/img/stop.png")
	
	# création de texte fixe
	nomUnite=list(dicoref.dico[race].keys())
	for i in range(len(nomUnite)-1):
		if nomUnite[i] in ["general","Jarl","reine du chaos","General"]:
			del(nomUnite[i])

	u0=maketext(nomUnite[0]+" --prix: "+str(dicoref.dico[race][nomUnite[0]][-3]),white,20)
	u1=maketext(nomUnite[1]+" --prix: "+str(dicoref.dico[race][nomUnite[1]][-3]),white,20)
	u2=maketext(nomUnite[2]+" --prix: "+str(dicoref.dico[race][nomUnite[2]][-3]),white,20)
	u3=maketext(nomUnite[3]+" --prix: "+str(dicoref.dico[race][nomUnite[3]][-3]),white,20)
	u4=maketext(nomUnite[4]+" --prix: "+str(dicoref.dico[race][nomUnite[4]][-3]),white,20)
	u5=maketext(nomUnite[5]+" --prix: "+str(dicoref.dico[race][nomUnite[5]][-3]),white,20)
	u6=maketext(nomUnite[6]+" --prix: "+str(dicoref.dico[race][nomUnite[6]][-3]),white,20)

	msg=maketext("Appuyez sur stop quand vous aurez terminer de choisire vos unités",white,20)

	# position des images
	quitbut.pos=quitbut.pos.move(1100,0)

	add0.pos=add0.pos.move(555,10)
	add1.pos=add1.pos.move(555,90)
	add2.pos=add2.pos.move(555,170)
	add3.pos=add3.pos.move(555,250)
	add4.pos=add4.pos.move(555,330)
	add5.pos=add5.pos.move(555,410)
	add6.pos=add6.pos.move(555,490)

	sub0.pos=sub0.pos.move(500,10)
	sub1.pos=sub1.pos.move(500,90)
	sub2.pos=sub2.pos.move(500,170)
	sub3.pos=sub3.pos.move(500,250)
	sub4.pos=sub4.pos.move(500,330)
	sub5.pos=sub5.pos.move(500,410)
	sub6.pos=sub6.pos.move(500,490)

	stopimg.pos=stopimg.pos.move(300,570)

	# son pour l'écran
	while True:	

		solde=maketext("solde restant:  "+str(soldeRestant),white,20)
		compU0=maketext("total: "+str(nbu0),white,20)
		compU1=maketext("total: "+str(nbu1),white,20)
		compU2=maketext("total: "+str(nbu2),white,20)
		compU3=maketext("total: "+str(nbu3),white,20)
		compU4=maketext("total: "+str(nbu4),white,20)
		compU5=maketext("total: "+str(nbu5),white,20)
		compU6=maketext("total: "+str(nbu6),white,20)
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()

			if event.type==MOUSEBUTTONUP:
				pos=event.pos

				if quitbut.pos.collidepoint(pos):
					pygame.quit()

	#------ pour ajouter une unité à sa compo
				if add0.pos.collidepoint(pos):
					if soldeRestant-int(dicoref.dico[race][nomUnite[0]][-3])>=0:
						uniteChoisie.append(nomUnite[0])
						soldeRestant-=int(dicoref.dico[race][nomUnite[0]][-3])
						nbu0+=1

				if add1.pos.collidepoint(pos):
					if soldeRestant-int(dicoref.dico[race][nomUnite[1]][-3])>=0:
						uniteChoisie.append(nomUnite[1])
						soldeRestant-=int(dicoref.dico[race][nomUnite[1]][-3])
						nbu1+=1

				if add2.pos.collidepoint(pos):
					if soldeRestant-int(dicoref.dico[race][nomUnite[2]][-3])>=0:
						uniteChoisie.append(nomUnite[2])
						soldeRestant-=int(dicoref.dico[race][nomUnite[2]][-3])
						nbu2+=1

				if add3.pos.collidepoint(pos):
					if soldeRestant-int(dicoref.dico[race][nomUnite[3]][-3])>=0:
						uniteChoisie.append(nomUnite[3])
						soldeRestant-=int(dicoref.dico[race][nomUnite[3]][-3])
						nbu3+=1

				if add4.pos.collidepoint(pos):
					if soldeRestant-int(dicoref.dico[race][nomUnite[4]][-3])>=0:
						uniteChoisie.append(nomUnite[4])
						soldeRestant-=int(dicoref.dico[race][nomUnite[4]][-3])
						nbu4+=1

				if add5.pos.collidepoint(pos):
					if soldeRestant-int(dicoref.dico[race][nomUnite[5]][-3])>=0:
						uniteChoisie.append(nomUnite[5])
						soldeRestant-=int(dicoref.dico[race][nomUnite[5]][-3])
						nbu5+=1

				if add6.pos.collidepoint(pos):
					if soldeRestant-int(dicoref.dico[race][nomUnite[6]][-3])>=0:
						uniteChoisie.append(nomUnite[6])
						soldeRestant-=int(dicoref.dico[race][nomUnite[6]][-3])
						nbu6+=1

	#------ pour enlever une unité à sa compo
				if len(uniteChoisie)>0:
					if sub0.pos.collidepoint(pos):
						if nomUnite[0] in uniteChoisie:
							uniteChoisie.remove(nomUnite[0])
							nbu0-=1
							soldeRestant+=int(dicoref.dico[race][nomUnite[0]][-3])

					if sub1.pos.collidepoint(pos):
						if nomUnite[1] in uniteChoisie:
							uniteChoisie.remove(nomUnite[1])
							nbu1-=1
							soldeRestant+=int(dicoref.dico[race][nomUnite[1]][-3])

					if sub2.pos.collidepoint(pos):
						if nomUnite[2] in uniteChoisie:
							uniteChoisie.remove(nomUnite[2])
							nbu2-=1
							soldeRestant+=int(dicoref.dico[race][nomUnite[2]][-3])

					if sub3.pos.collidepoint(pos):
						if nomUnite[3] in uniteChoisie:
							uniteChoisie.remove(nomUnite[3])
							nbu3-=1
							soldeRestant+=int(dicoref.dico[race][nomUnite[3]][-3])

					if sub4.pos.collidepoint(pos):
						if nomUnite[4] in uniteChoisie:
							uniteChoisie.remove(nomUnite[4])
							nbu4-=1
							soldeRestant+=int(dicoref.dico[race][nomUnite[4]][-3])

					if sub5.pos.collidepoint(pos):
						if nomUnite[5] in uniteChoisie:
							uniteChoisie.remove(nomUnite[5])
							nbu5-=1
							soldeRestant+=int(dicoref.dico[race][nomUnite[5]][-3])

					if sub6.pos.collidepoint(pos):
						if nomUnite[6] in uniteChoisie:
							uniteChoisie.remove(nomUnite[6])
							nbu6-=1
							soldeRestant+=int(dicoref.dico[race][nomUnite[6]][-3])



	#------ pour finir sa compo d'armée
				if stopimg.pos.collidepoint(pos):
					uniteChoisie.append("stop")

		# remise à zero
		fen.fill(grey)

		# text
		fen.blit(u0.ren,(10,20 ))
		fen.blit(u1.ren,(10,100))
		fen.blit(u2.ren,(10,180))
		fen.blit(u3.ren,(10,260))
		fen.blit(u4.ren,(10,340))
		fen.blit(u5.ren,(10,420))
		fen.blit(u6.ren,(10,500))

		fen.blit(compU0.ren,(620,20 ))
		fen.blit(compU1.ren,(620,100))
		fen.blit(compU2.ren,(620,180))
		fen.blit(compU3.ren,(620,260))
		fen.blit(compU4.ren,(620,340))
		fen.blit(compU5.ren,(620,420))
		fen.blit(compU6.ren,(620,500))

		# image 
		fen.blit(add0.image,add0.pos)
		fen.blit(add1.image,add1.pos)
		fen.blit(add2.image,add2.pos)
		fen.blit(add3.image,add3.pos)
		fen.blit(add4.image,add4.pos)
		fen.blit(add5.image,add5.pos)
		fen.blit(add6.image,add6.pos)

		fen.blit(sub0.image,sub0.pos)
		fen.blit(sub1.image,sub1.pos)
		fen.blit(sub2.image,sub2.pos)
		fen.blit(sub3.image,sub3.pos)
		fen.blit(sub4.image,sub4.pos)
		fen.blit(sub5.image,sub5.pos)
		fen.blit(sub6.image,sub6.pos)

		fen.blit(stopimg.image,stopimg.pos)
		fen.blit(solde.ren,(850,200))
		fen.blit(quitbut.image,quitbut.pos)
		fen.blit(msg.ren,(100,640))


		pygame.display.update()

		if len(uniteChoisie)>0 and uniteChoisie[-1]=="stop":
			return uniteChoisie


# ------------écran de jeux principal--------------

def afficheGrille(fen,listeUnite,error=None):

	decal=30
	taillecase=30
	fen.fill(grey)
	fondgr=pygame.draw.rect(fen,white,(decal,decal,600,600))

	i=0
	while i<=600 :
		pygame.draw.line(fen,black,(decal,i+decal),(600+decal,i+decal))
		pygame.draw.line(fen,black,(decal+i,decal),(i+decal,600+decal))
		i+=taillecase

	# parcour de la liste des unité
	joueur=0
	for i in listeUnite:
		race=i.armee
		for j in i.compo:
			unite=i.compo[j]
			try:
				imgUnite=pygame.image.load("ressources/img/pions/"+race+"/"+unite.nom+".png").convert_alpha()
			except:
				imgUnite=pygame.image.load("ressources/img/pions/unkown.png").convert_alpha()
			x=unite.coord[0]*30+decal+2
			y=unite.coord[1]*30+decal+2
			imgUnitePos=(x,y)
			if joueur==0:
				pygame.draw.rect(fen,blue,(x-2,y-2,30,30))
			else:
				pygame.draw.rect(fen,red,(x-2,y-2,30,30))
			fen.blit(imgUnite,imgUnitePos)
		joueur+=1

	if error!=None:
		if error=="chemin":
			txterror=maketext("le chemin est trop longt ou un obstacle bloc le passage !",trueRed,14)
			fen.blit(txterror.ren,(30,0))

	pygame.display.update()

def placePionts(fen,listeUnite,plateau,joueur):

	p=plateau
	decal=30
	taillecase=30

	txt=maketext("cliquez sur la case ou vous voulez placez vôtre unité",white,14)

	for i in listeUnite[joueur].compo:

		click=False
		unite=listeUnite[joueur].compo[i]
		#écran d'info sur l'unité
		try:
			imgIcones=pygame.image.load("ressources/img/icones/"+listeUnite[joueur].armee+"/"+unite.nom+".png").convert_alpha()
		except:
			imgIcones=pygame.image.load("ressources/img/icones/unknow.png").convert_alpha()
		imgIconesPos=(640,35)
		uniteNom=maketext("nom: "+str(unite.nom),white,20)
		unitePv=maketext("pv: "+str(unite.pv),white,20)
		uniteArmure=maketext("armure: "+str(unite.armure),white,20)
		uniteAttaque=maketext("Attaque: "+str(unite.attaque),white,20)
		uniteDeplacement=maketext("Déplacement restant: "+str(unite.deplacementRestant),white,20)
		unitePortee=maketext("portée de l'attaque: "+str(unite.portee),white,20)

		fen.blit(txt.ren,(610,10))
		fen.blit(imgIcones,imgIconesPos)
		fen.blit(uniteNom.ren,(830,100))
		fen.blit(unitePv.ren,(650,250))
		fen.blit(uniteArmure.ren,(650,300))
		fen.blit(uniteAttaque.ren,(650,350))
		fen.blit(uniteDeplacement.ren,(650,400))
		fen.blit(unitePortee.ren,(650,450))
		pygame.display.update()

		while click==False:

			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()

				if event.type==MOUSEBUTTONUP:
					pos=event.pos

					if pos[0] in range(decal,600+decal) and pos[1] in range(decal,600+decal) :
						x,y=(pos[0]-decal)//taillecase,(pos[1]-decal)//taillecase
						if joueur==0 and y in range(0,4):
							if p.troupes[y][x]==1 and p.terrain[y][x]==1:
								unite.placerUnite(p,x,y)
								# p.troupes[y][x]=unite
								# unite.coord=(x,y)
								afficheGrille(fen,listeUnite)
								click=True

						elif joueur==1 and y in range(16,21):
							if p.troupes[y][x]==1 and p.terrain[y][x]==1:
								unite.placerUnite(p,x,y)
								# p.troupes[y][x]=unite
								# unite.coord=(x,y)
								afficheGrille(fen,listeUnite)
								click=True
	return(p)

def afficheInfo(fen,race,unite):

	#efface info précédente
	pygame.draw.rect(fen,grey,(635,0,1200,680))

	try:
		imgIcones=pygame.image.load("ressources/img/icones/"+race+"/"+unite.nom+".png").convert_alpha()
	except:
		imgIcones=pygame.image.load("ressources/img/icones/unknow.png").convert_alpha()
	imgIconesPos=(640,35)
	uniteNom=maketext("nom: "+str(unite.nom),white,20)
	unitePv=maketext("pv: "+str(unite.pv),white,20)
	uniteArmure=maketext("armure: "+str(unite.armure),white,20)
	uniteAttaque=maketext("Attaque: "+str(unite.attaque),white,20)
	uniteDeplacement=maketext("Déplacement restant: "+str(unite.deplacementRestant),white,20)
	unitePortee=maketext("portée de l'attaque: "+str(unite.portee),white,20)

	fen.blit(imgIcones,imgIconesPos)
	fen.blit(uniteNom.ren,(830,100))
	fen.blit(unitePv.ren,(650,250))
	fen.blit(uniteArmure.ren,(650,300))
	fen.blit(uniteAttaque.ren,(650,350))
	fen.blit(uniteDeplacement.ren,(650,400))
	fen.blit(unitePortee.ren,(650,450))
	pygame.display.update()

def bougerPions(fen,listeUnite,plateau,joueur):

	decal=30
	taillecase=30
	uniteClick=None
	uniteValues=list(listeUnite[joueur].compo.values())
	uniteBouger=[]

	while len(uniteBouger)!=len(listeUnite[joueur].compo) :

			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()

				if event.type==MOUSEBUTTONUP:
					pos=event.pos

					if pos[0] in range(decal,600+decal) and pos[1] in range(decal,600+decal) :
						x,y=(pos[0]-decal)//taillecase,(pos[1]-decal)//taillecase

						if plateau.troupes[y][x]!=1:
							try:
								afficheInfo(fen,listeUnite[0].armee,plateau.troupes[y][x])
							except:
								afficheInfo(fen,listeUnite[1].armee,plateau.troupes[y][x])
							uniteClick=plateau.troupes[y][x]

						elif plateau.troupes[y][x]==1 and uniteClick!=None:
							if uniteClick in uniteValues:
								for i in uniteValues:
									if i==uniteClick and i.coord==uniteClick.coord:
										if not uniteClick in uniteBouger and plateau.troupes[y][x]==1 :
											coord=uniteClick.coord
											try :
												uniteClick.deplacement(p,x,y)
												uniteBouger.append(uniteClick)
												plateau.troupes[y][x]=uniteClick
												plateau.troupes[coord[1]][coord[0]]=1
												afficheGrille(fen,listeUnite)
											except:
												afficheGrille(fen,listeUnite,"chemin")
												
											

	return plateau


def attaquer(fen,listeUnite,plateau,joueur):
	decal=30
	taillecase=30

#création d'une liste avec les unité des deux armées
	if joueur==0:
		ennemi=1
	else:
		ennemi=0
	
	uniteValues=list(listeUnite[joueur].compo.values())
	print(uniteValues)
	uniteValuesEnennmi=list(listeUnite[ennemi].compo.values())
#liste des unité ayant attaqué	
	uniteAttaquer=[]

	msgATQ=maketext("choisissez l'unité qui vas attaquer: ",black,12)
	msgDEF=maketext("coissisez l'unité que vous voulez attaquer: ",black,12)
	

	while True:

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()

			if event.type==MOUSEBUTTONUP:
				pos=event.pos

				if pos[0] in range(decal,600+decal) and pos[1] in range(decal,600+decal) :
						x,y=(pos[0]-decal)//taillecase,(pos[1]-decal)//taillecase

##<<<<<<< HEAD:developement/src/gui/GUIfunc.py
##						
##=======
##						if plateau.troupes[y][x] in uniteValues:
##							uniteAttaquante=plateau.troupes[y][x]
##							cibles=uniteAttaquante.ennemisAPortee(p,ennemi,listeUnite)
##							print(cibles)
##>>>>>>> 626a460ad5120803d01cf9423c92cf48f0cae8cc:developement/src/GUIfunc.py
