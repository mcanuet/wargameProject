import os

def listing():
	a=os.listdir("web/data")
	b=[]
	for i in a:
		if i[-4:]=="json" and i[:4]!='croi' and i[:4]!='muta':
			b+=[i]

	variable="<catalog>\n"
	for i in b:
		variable+="	<file>\n"+"		"+i+"\n	</file>\n"
	variable+="</catalog>\n"
	fichier=open("web/listing.xml","w")
	fichier.write(variable)
	fichier.close()
