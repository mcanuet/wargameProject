window.onload=function(){
	recupeListing();
}

function ecrire(type,contenu,conteneur,nomClass,index,nomId="voide"){
	var node = document.createElement(type);
	if (nomClass!=="voide") {node.className=nomClass;}
	if (nomId!=="voide") {node.id=nomId};
	var text = document.createTextNode(contenu);
	node.appendChild(text);
	document.getElementsByClassName(conteneur)[index].appendChild(node);
}

function recupeListing(){
	var url="listing.xml";
	var xhr=new XMLHttpRequest();
	xhr.open("GET",url);
	xhr.responseType="document";
	xhr.onload=function(){
		console.log(xhr);
		var doc=xhr.responseXML.getElementsByTagName("file");
		for (var i = 0; i < doc.length; i++) {
			var txt="tournois : "+doc[i].innerHTML.slice(0,-7);
			ecrire("h2",txt,"conteneur","txt",0);
			ecrire("div","","conteneur","tournois",0);
			ecrire("div","","tournois","spoiler",document.getElementsByClassName("tournois").length-1);
			loadTournois(doc[i].innerHTML,i);
		}
	}
	xhr.send();
};

function loadTournois(tournois,index){
	var url="data/"+tournois;
	var xhr=new XMLHttpRequest();
	xhr.open("GET",url);
	xhr.responseType="json";
	xhr.onload=function(){
		var doc = xhr.response;
		// console.log(doc);

		for(var i in doc){

			ecrire("div","","spoiler","spoiler2",index);
			ecrire("button",i,"spoiler2","but",document.getElementsByClassName("spoiler2").length-1);
			ecrire("div","","spoiler2","combat",document.getElementsByClassName("spoiler2").length-1);

			traitementCombat(doc[i]);
		}
	}
	xhr.send();
}

function traitementCombat(combat){
	var index1=document.getElementsByClassName("combat");
	var combatants=new Array;
	var qqc=new Array;
	for(var i in combat){
		if (i.indexOf("armee")!=-1) {
			combatants.push(i);
			ecrire("h4",i,"combat","txt",index1.length-1);
			ecrire("div","","combat","combatants",index1.length-1);

			var index2=document.getElementsByClassName("combatants");
			ecrire("h4","race:","combatants","txt",index2.length-1);
			ecrire("p",combat[i].race,"combatants","race",index2.length-1);

			ecrire("h4","composition:","combatants","txt",index2.length-1);
			ecrire("p",combat[i].composition,"combatants","initCompo",index2.length-1);
		}
		else{
			qqc.push(combat[i]);
		}
	}
	
	// console.log(qqc);
	var victoire=[0,0];
	for (var i = 0; i < qqc.length; i++) {
		// console.log(qqc[i][combatants[0]]);
		if (qqc[i][combatants[0]].length==0) {victoire[0]+=1}
		else {victoire[1]+=1}
	}

	// console.log(victoire);
	ecrire("h4","totale de victoire: "+victoire[0],"combatants","victoire",index2.length-2);
	ecrire("h4","totale de victoire: "+victoire[1],"combatants","victoire",index2.length-1);

	makeEvent();
}

function makeEvent(){
	for (var i = 0; i < document.getElementsByClassName("spoiler2").length; i++) {
		document.getElementsByClassName("spoiler2")[i].value="0";
		// document.getElementsByClassName("spoiler2")[i].getElementsByTagName("div")[0].style.display="none";
		document.getElementsByClassName("spoiler2")[i].getElementsByTagName("div")[0].style.height="0px";
		document.getElementsByClassName("spoiler2")[i].getElementsByTagName("div")[0].style.opacity="0";
		document.getElementsByClassName("spoiler2")[i].getElementsByTagName("button")[0].addEventListener("click",spoilFunction);
	};
}

function spoilFunction(){
	if(this.parentNode.value=="1"){
		this.parentNode.value = "0";
		// this.parentNode.getElementsByTagName("div")[0].style.display = "none";
		this.parentNode.getElementsByTagName("div")[0].style.height = "0px";
		this.parentNode.getElementsByTagName("div")[0].style.opacity="0";
	}
	else{
		this.parentNode.value = "1";
		// this.parentNode.getElementsByTagName("div")[0].style.display = "block";
		this.parentNode.getElementsByTagName("div")[0].style.height = "580px";
		this.parentNode.getElementsByTagName("div")[0].style.opacity="1";
	}
}