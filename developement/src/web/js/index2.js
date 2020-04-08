window.onload=function(){
	recupeListing();
}

function ecrire(type,contenu,conteneur,nomClass,index,nomId="voide"){
	var node = document.createElement(type);
	if (nomClass!=="voide") {node.className=nomClass};
	if (nomId!=="voide") {node.id=nomId};
	var text = document.createTextNode(contenu);
	node.appendChild(text);
	document.getElementsByClassName(conteneur)[index].appendChild(node);
}


function makeEvent(){
	for (var i = 0; i < document.getElementsByClassName("tournois").length; i++) {
		document.getElementsByClassName("tournois")[i].value="0";
		document.getElementsByClassName("tournois")[i].getElementsByTagName("div")[0].style.display="none";
		document.getElementsByClassName("tournois")[i].getElementsByTagName("button")[0].addEventListener("click",loadFunc);
	};
}

function loadFunc(){
	if(this.parentNode.value=="1"){
		this.parentNode.value = "0";
		this.parentNode.getElementsByTagName("div")[0].style.display = "none";
		// this.parentElement.lastChild.innerHTML="vide";
	}
	else{
		this.parentNode.value = "1";
		this.parentNode.getElementsByTagName("div")[0].style.display = "block";
		chargeContenu(this.parentElement.firstElementChild.innerHTML.slice(9));

	}
}

function recupeListing(){
	var url="listing.xml";
	var xhr=new XMLHttpRequest();
	xhr.open("GET",url);
	xhr.responseType="document";
	xhr.onload=function(){
		var doc=xhr.responseXML;
		var elmnt = doc.getElementsByTagName("file");
		for (var i = 0; i < elmnt.length; i++) {
			// elmnt[i]
			ecrire("div","","conteneur","tournois",0);
			ecrire("button","tournois "+elmnt[i].innerHTML.slice(0,-7),"tournois","but",document.getElementsByClassName("tournois").length-1);
			ecrire("div","","tournois","contenu",document.getElementsByClassName("tournois").length-1);
			ecrire("div","","contenu","total",document.getElementsByClassName("contenu").length-1);
		}
		makeEvent();
	}

	xhr.send();
	
};

function chargeContenu(num){
	var num = parseInt(num);

	var url="data/"+num+".json";
	var xhr=new XMLHttpRequest();
	xhr.open("GET",url);
	xhr.responseType="json";
	xhr.onload=function(){
		doc = xhr.response;
		var tableCombats=new Array;
		var compo = new Array;
		for(var i in doc){
			tableCombats.push(i);
		}

		document.getElementsByClassName("total")[num].innerHTML="";

// écriture des nombres totales de victoires par armées.
		var tableTotale= new Array;
		ecrire("h2","Totales des victoires","total","voide",num);
		for (var i in doc.total){
			tableTotale.push(i);
			
		}
		tableTotale.sort();
		for (var i = 0; i < tableTotale.length; i++) {
			ecrire("div",tableTotale[i]+": "+doc.total[tableTotale[i]],"total","voide",num);
		}

		tableCombats.sort();

		var tableCompos = []*tableTotale.length-1;
		console.log(tableCompos);
		for (var i = 0; i < tableCombats.length; i++) {
			// console.log(tableCombats[i]);
		}

// ecriture des compositions initiales des armées.
		// console.log(doc[tableCombats[0]].armee1.composition);

	}

	xhr.send();

}