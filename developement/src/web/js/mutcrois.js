window.onload=function(){
	Croisement();
	Mutation();
}

function ecrire(type,contenu,conteneur,nomClass,index,nomId="voide"){
	var node = document.createElement(type);
	if (nomClass!=="voide") {node.className=nomClass;}
	if (nomId!=="voide") {node.id=nomId};
	var text = document.createTextNode(contenu);
	node.appendChild(text);
	document.getElementsByClassName(conteneur)[index].appendChild(node);
}

function makeEvent(){
	for (var i = 0; i < document.getElementsByClassName("spoiler2").length; i++) {
		document.getElementsByClassName("spoiler2")[i].value="0";
		document.getElementsByClassName("spoiler2")[i].getElementsByTagName("div")[0].style.height="0px";
		document.getElementsByClassName("spoiler2")[i].getElementsByTagName("div")[0].style.opacity="0";
		document.getElementsByClassName("spoiler2")[i].getElementsByTagName("button")[0].addEventListener("click",spoilFunction);
	};
}

function spoilFunction(){
	if(this.parentNode.value=="1"){
		this.parentNode.value = "0";
		this.parentNode.getElementsByTagName("div")[0].style.height = "0px";
		this.parentNode.getElementsByTagName("div")[0].style.opacity = "0";
	}
	else{
		this.parentNode.value = "1";
		this.parentNode.getElementsByTagName("div")[0].style.height = "auto";
		this.parentNode.getElementsByTagName("div")[0].style.opacity = "1";
	}
}

// traitement des croisements
function Croisement(){
	var url="../data/croisement0.json";
	var xhr=new XMLHttpRequest();
	xhr.open("GET",url);
	xhr.responseType="json";
	xhr.onload=function(){
		ecrire("h2","Croisement","conteneur","txt",0);
		var doc=xhr.response;
		for (var i in doc){
			ecrire("div","","conteneur","Tournois",0);
			ecrire("div","","Tournois","spoiler",document.getElementsByClassName("Tournois").length-1);


			ecrire("div","","spoiler","spoiler2",document.getElementsByClassName("Tournois").length-1);
			ecrire("button",i,"spoiler2","but",document.getElementsByClassName("spoiler2").length-1);

			ecrire("div","Qui est croisé avec qui :","spoiler2","spoiler3",document.getElementsByClassName("spoiler2").length-1);

			for (var j = 0; j < doc[i].length; j++) {
				ecrire("p",doc[i][j],"spoiler3","listeCrois",document.getElementsByClassName("spoiler3").length-1);
			}
		}
	}
	xhr.send();
}

// traitement pour les mutations
function Mutation(){
	var url="../data/mutation0.json";
	var xhr=new XMLHttpRequest();
	xhr.open("GET",url);
	xhr.responseType="json";
	xhr.onload=function(){
		ecrire("h2","Mutation","conteneur","txt",1);
		ecrire("div","","conteneur","mutaTournois",1);
		var doc=xhr.response;
		for(var i in doc){
			ecrire("div","","mutaTournois","spoiler",document.getElementsByClassName("mutaTournois").length-1);
			ecrire("div","","spoiler","spoiler2",document.getElementsByClassName("spoiler").length-1);
			ecrire("button",i,"spoiler2","but",document.getElementsByClassName("spoiler2").length-1);
			ecrire("div","","spoiler2","spoiler3",document.getElementsByClassName("spoiler2").length-1);
			for(var j in doc[i]){

				ecrire("div","","spoiler3","mutation",document.getElementsByClassName("spoiler3").length-1);
				ecrire("h3",j,"mutation","voide",document.getElementsByClassName("mutation").length-1);

				ecrire("h4","qui est mutés:","mutation","voide",document.getElementsByClassName("mutation").length-1);
				ecrire("p","totale de point utilisés: "+doc[i][j].combien[0],"mutation","voide",document.getElementsByClassName("mutation").length-1)
				ecrire("p",doc[i][j].qui,"mutation","voide",document.getElementsByClassName("mutation").length-1);
				ecrire("h4","en quoi sont ils mutés:","mutation","voide",document.getElementsByClassName("mutation").length-1);
				ecrire("p","totale de point utilisés: "+doc[i][j].combien[1],"mutation","voide",document.getElementsByClassName("mutation").length-1)
				ecrire("p",doc[i][j].quoi,"mutation","voide",document.getElementsByClassName("mutation").length-1);	

				makeEvent();
			}
		}

	}
	xhr.send();
}