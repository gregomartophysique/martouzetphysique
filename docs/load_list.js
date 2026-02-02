data = [
		{
			"name": "De Fresnel à Fraunhofer",
			"img": "Fresnel_Fraun.jpg",
			"codePy": "De_Fresnel_a_Fraun.py",
			"keyword": ["Onde", "Optique"],
			"type": "py",
			"description": "Calcul de la figure de diffraction par intégration de Huygens-Fresnel. Possibilité de modifier certains paramètres (longueur d'onde, largeur de la fente, ...). Le nombre de Fresnel F est affiché en direct. L'éclairement 2D, tel qu'on le voit sur un écran et éclairement en fonction de la position"
		},
		{
			"name": "Critère de Rayleigh",
			"img": "Rayleigh.jpg",
			"codePy": "Critere_Rayleigh.py",
			"keyword": ["Onde", "Optique"],
			"type": "py",
			"description": "Illustration du critère de Rayleigh. Possibilité de modifier certains paramètres (longueur d'onde, largeur de la fente, ...). L'éclairement 2D, tel qu'on le voit sur un écran et éclairement en fonction de la position"
		},
		{
			"name": "Diffraction périodique",
			"img": "diffraction_periodique.jpg",
			"codePy": "Diffraction_periodique.py",
			"keyword": ["Onde", "Optique"],
			"type": "py",
			"description": ""
		},
		{
			"name": "Trajectoire",
			"img": "trajectoire.jpg",
			"codePy": "Trajectoire.py",
			"keyword": ["Mécanique"],
			"type": "py",
			"description": "Trajectoire d'un point autour d'un centre et affichage de la zone d'énergie potentielle accessible."
		},

		{
			"name": "Marée",
			"img": "maree.jpg",
			"codePy": "Maree.py",
			"keyword": ["Mécanique"],
			"type": "py",
			"description": ""
		},
		{
			"name": "Equation auto-cohérente",
			"img": "Equ_autocoherente.jpg",
			"codePy": "Equ_autocoherente.py",
			"keyword": ["Thermodynamique"],
			"type": "py",
			"description": "Résolution de l'équation auto-cohérente en champ moyen pour différentes températures et différents champs magnétiques."
		},
		{
			"name": "Energie libre de Landau",
			"img": "Energie_libre_Landau.jpg",
			"codePy": "Energie_libre_Landau.py",
			"keyword": [ "Thermodynamique"],
			"type": "py",
			"description": "Affichage de l'énergie libre dans le cas du model de Landau (pour différentes températures)."
		},
		{
			"name": "Loi de Planck",
			"img": "loi_planck.jpg",
			"codePy": "loi_planck.py",
			"type": "py",
			"keyword": ["Thermodynamique"],
			"description": "Calcul du spectre d'un corps à partir de la loi de Planck. Donne également des éléments tel que le maximum, la constante de Stefan, etc."
		},
		{
			"name": "Cristallographie",
			"img": "Cristallographie.jpg",
			"code": "",
			"type": "pa",
			"keyword": ["Chimie"],
			"description": "Visualisation 3D de mailles."
		},
		{
			"name": "Filtre en traitement du signal",
			"img": "traitement_signal.jpg",
			"codePy": "Traitement_Signal.py",
			"codeJS": "app_filtrage.html",
			"type": "py",
			"keyword": ["Filtrage", "Electricité", "Signaux"],
			"description": "Visualisation de l'influence de filtre sur un signal, représentation temporelle et spectrale"
		}

	]


window.onload = function () {


	var liste = document.getElementById("liste");

	var possible_keywords = [];

	for (let j = 0; j < data.length; j++) {
		var element = document.createElement("div");
		element.className = "element";

		var thumbnail = document.createElement("div");
		thumbnail.className = "thumbnail";
		var right_side = document.createElement("div");
		right_side.className = "right_side";

		element.appendChild(thumbnail);
		element.appendChild(right_side);

		var titre = document.createElement("div");
		titre.className = "title";
		titre.innerHTML = data[j].name;

		var description = document.createElement("div");
		description.className = "description";
		description.innerHTML = data[j].description;

		var logo = document.createElement("IMG");
		logo.className = "thumbnail-image";

		logo.src = "./codes_python/"+data[j].img;
		logo.alt = "./codes_python/" + data[j].img;
		logo.title = data[j].name;

		thumbnail.appendChild(logo);

		

		// Mots clefs
		var keywords = document.createElement("div");
		keywords.className = "keywords";
		for (let k = 0; k < data[j].keyword.length; k++) {
			key = document.createElement("div");
			key.className = "keyword";
			key.innerHTML = data[j].keyword[k];
			if (!possible_keywords.some(e => e === data[j].keyword[k])) {
				possible_keywords.push(data[j].keyword[k]);
			}
			keywords.appendChild(key);
		}

		// Bouton pour les codes (ou liens)
		var liste_btnCode = document.createElement("div");

		btnCodeLink = document.createElement("A");
		btnCode = document.createElement("BUTTON");
		btnCodeLink.href = "./application_info.html?code_name=" + data[j].codePy;
		btnCode.innerHTML = "En savoir plus";
		btnCodeLink.appendChild(btnCode);
		liste_btnCode.appendChild(btnCodeLink);


		if (typeof data[j].codePy !== "undefined") {
			btnCodeLink = document.createElement("A");
			btnCode = document.createElement("BUTTON");
			btnCodeLink.href = "./codes_python/" + data[j].codePy;
			btnCode.setAttribute('download', "./codes_python/" + data[j].codePy);
			btnCode.innerHTML = "Code Python";
			btnCodeLink.appendChild(btnCode);
			liste_btnCode.appendChild(btnCodeLink);
		}
		if (typeof data[j].codeJS !== "undefined") {
			btnCodeLink = document.createElement("A");
			btnCode = document.createElement("BUTTON");
			btnCodeLink.href = './AppJS/' + data[j].codeJS;
			btnCode.innerHTML = "JavaScript";
			btnCodeLink.appendChild(btnCode);
			liste_btnCode.appendChild(btnCodeLink);
		}


		right_side.appendChild(titre);
		right_side.appendChild(keywords);
		right_side.appendChild(description);
		right_side.appendChild(liste_btnCode);

		liste.appendChild(element);
	}

	var choose_keyword = document.getElementById("listCategorie"); 
	for (let k = 0; k < possible_keywords.length; k++) {
		key = document.createElement("LI");
		input = document.createElement("INPUT");
		input.setAttribute('type', "checkbox");
		input.setAttribute('value', possible_keywords[k]);
		input.setAttribute('id', "checkitem_categorie_" + k);

		input_label = document.createElement("LABEL");
		input_label.setAttribute('for', "checkitem_categorie_" + k);
		input_label.innerHTML = possible_keywords[k];
		key.appendChild(input);
		key.appendChild(input_label);
		choose_keyword.appendChild(key);
	}

};