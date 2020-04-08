window.onload = function(){
	
	importerDonnees(donnee);	//donnee fait référence aux données JSON des tournois
	
	spoilerParent = new Array();	//Contient les premiers spoilers visible
	for (var i=0;i<document.getElementById("Listing").getElementsByClassName("spoiler").length;i++){
		if(document.getElementById("Listing").getElementsByClassName("spoiler")[i].nodeName=="DIV"){
			spoilerParent.push(document.getElementById("Listing").getElementsByClassName("spoiler")[i])
			document.getElementById("Listing").getElementsByClassName("spoiler")[i].value = "0";
			document.getElementById("Listing").getElementsByClassName("spoiler")[i].getElementsByTagName("div")[0].style.display = "none"
			//console.log(document.getElementById("Listing").getElementsByClassName("spoiler")[i].getElementsByTagName("p")[0])
			document.getElementById("Listing").getElementsByClassName("spoiler")[i].getElementsByTagName("p")[0].addEventListener("click",spoilFunction)
		}
	}
}

function importeJSON(link){
	XHR = new XMLHttpRequest();
	XHR.open("GET","test.json");
	XHR.responseType = "json";
	XHR.onload = function(ev){
		donnees = ev.target.response;
		console.log(donnees)
		//Mettre ici l'application de l'affichage des données obtenues (Vidage des éléments déjà présent + ajout des nouveaux)
	}
	XHR.send()
}


function spoilFunction(){
	/*console.log(this.parentNode)
	console.log(this.parentNode.value);
	console.log(this.parentNode.getElementsByTagName("div")[0].style.display)*/
	if(this.parentNode.value=="1"){
		this.parentNode.value = "0";
		this.parentNode.getElementsByTagName("div")[0].style.display = "none";
	}
	else{
		this.parentNode.value = "1";
		this.parentNode.getElementsByTagName("div")[0].style.display = "block";
	}
	console.log(this.parentNode.value)
	console.log(this.parentNode.getElementsByTagName("div")[0].style.display)
}

function importerDonnees(data){
	for(var i in data){
		//Les premiers éléments des données sont les tournois
		console.log(i)
		//On créait alors une div spoiler
		var newTournament = document.createElement("div");
		newTournament.className = "spoiler";
		newTournament.id = i;
		//On créait les sous-éléments textes visible de prime abord
		var newParagraphe = document.createElement("p");
		var newTitle = document.createElement("span");
		newTitle.textContent = traitementNom(i);
		newParagraphe.appendChild(newTitle);
		/********************************************
		***AJOUTER ICI LES ELEMENTS FIGURANT SUPL.***
		********************************************/
		var newScrollButton = document.createElement("span");
		newScrollButton.textContent = "▼";
		newParagraphe.appendChild(newScrollButton);
		newTournament.appendChild(newParagraphe);
		//Remplir ici les sous-spoiler correspondant aux Combats
		var newContainer = document.createElement("div");
		for(var j in data[i]){
			console.log(j)
			var newBattle = document.createElement("div");
			newBattle.className = "spoiler";
			newBattle.id = j;
			//Partie similaire à précédemment.
			var newParagraphe = document.createElement("p");
			var newTitle = document.createElement("span");
			newTitle.textContent = traitementNom(j);
			newParagraphe.appendChild(newTitle);
			/********************************************
			***AJOUTER ICI LES ELEMENTS FIGURANT SUPL.***
			********************************************/
			var newScrollButton = document.createElement("span");
			newScrollButton.textContent = "▼";
			newParagraphe.appendChild(newScrollButton);
			newBattle.appendChild(newParagraphe);
			newContainer.appendChild(newBattle);
			//Ajout des divs correspondant à chaque versions du combat
			var newDivContainer = document.createElement("div");
			for(var k in data[i][j]){
				var newVersion = document.createElement("div")
				newVersion.id = k;
				//Partie similaire à précédemment.
				var newParagraphe = document.createElement("p");
				var newTitle = document.createElement("span");
				newTitle.textContent = traitementNom(k);
				newParagraphe.appendChild(newTitle);
				/********************************************
				***AJOUTER ICI LES ELEMENTS FIGURANT SUPL.***
				********************************************/
				newVersion.appendChild(newParagraphe);
				newDivContainer.appendChild(newVersion);
			}
			newBattle.appendChild(newDivContainer);
			
			newTournament.appendChild(newContainer);
		}
		
		document.getElementById("Listing").appendChild(newTournament)
	}
}

function traitementNom(nom){
	if(nom.substring(0,4)=="tour"){return "Tournoi "+nom.substring(7)} //7 puisque Tournoi contient 6 lettres donc le nombre associé commence à l'indice 7
	if(nom.substring(0,4)=="comb"){return "Combat "+nom.substring(6)}
	return nom
}