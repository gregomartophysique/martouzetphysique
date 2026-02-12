window.onload = function () {

	var possible_keywords = [];

	for (let j = 0; j < data_application.length; j++) {
		// Mots clefs
		var keywords = document.createElement("div");
		keywords.className = "keywords";
		for (let k = 0; k < data_application[j].Keywords.length; k++) {
			if (!possible_keywords.some(e => e === data_application[j].Keywords[k])) {
				possible_keywords.push(data_application[j].Keywords[k]);
			}
		}
	}



	var choose_keyword = document.getElementById("listCategorie");
	for (let k = 0; k < possible_keywords.length; k++) {
		key = document.createElement("LI");
		input = document.createElement("INPUT");
		input.setAttribute('type', "checkbox");
		input.setAttribute('value', possible_keywords[k]);
		input.setAttribute('id', "checkitem_categorie_" + k);
		input.setAttribute('checked', "");
		input.setAttribute('name', possible_keywords[k]);

		input_label = document.createElement("LABEL");
		input_label.setAttribute('for', "checkitem_categorie_" + k);
		input_label.innerHTML = possible_keywords[k];
		key.appendChild(input);
		key.appendChild(input_label);
		choose_keyword.appendChild(key);
	}

	const fieldset = document.getElementById("keywords_field");
	fieldset.addEventListener('change', load);
	const fieldset_code = document.getElementById("code_type");
	fieldset_code.addEventListener('change', load);

	load();

};

function getCheckboxStates(fieldset) {
	const states = {};
	fieldset.querySelectorAll('input[type="checkbox"]').forEach(cb => {
		states[cb.name] = cb.checked;
	});
	return states;
}

function load() {
	const div = document.getElementById('liste');
	while (div.firstChild) {
		div.removeChild(div.firstChild);
	}

	const filtre = getCheckboxStates(document.getElementById("keywords_field"));
	const filtre_code_type = getCheckboxStates(document.getElementById("code_type"))
	for (let j = 0; j < data_application.length; j++) {

		var affiche = false;
		for (let k = 0; k < data_application[j].Keywords.length; k++) {
			affiche = affiche || filtre[data_application[j].Keywords[k]];
		}

		var bool_code = false;
		if (typeof data_application[j].CodePY !== "undefined") { // Si de type python, il faut vérifier que python est cliqué
			bool_code = filtre_code_type["Python"];
		}
		if (typeof data_application[j].CodeJS !== "undefined") { // Si de type python, il faut vérifier que python est cliqué
			bool_code = bool_code ||filtre_code_type["JS"];
		}
		//affiche = affiche || (filtre_code_type["Python"] && (typeof data[j].codePy !== "undefined"));
		//affiche = affiche || (filtre_code_type["JS"] && (typeof data[j].codeJS !== "undefined"));
		//affiche = affiche && (filtre_code_type["Python"] && (typeof data[j].codePy !== "undefined"));

		affiche = affiche && bool_code;

		if (!affiche) {
			continue;
		}

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
		titre.innerHTML = data_application[j].Nom;

		var description = document.createElement("div");
		description.className = "description";
		description.innerHTML = data_application[j].Descrip;

		var logo = document.createElement("IMG");
		logo.className = "thumbnail-image";

		logo.src = "./codes_python/" + data_application[j].Img;
		logo.alt = "./codes_python/" + data_application[j].Img;
		logo.title = data_application[j].Nom;

		thumbnail.appendChild(logo);



		// Mots clefs
		var keywords = document.createElement("div");
		keywords.className = "keywords";
		for (let k = 0; k < data_application[j].Keywords.length; k++) {
			key = document.createElement("div");
			key.className = "keyword";
			key.innerHTML = data_application[j].Keywords[k];
			keywords.appendChild(key);
		}

		// Bouton pour les codes (ou liens)
		var liste_btnCode = document.createElement("div");

		btnCodeLink = document.createElement("A");
		btnCode = document.createElement("BUTTON");
		btnCodeLink.href = "./application_info.html?ID=" + data_application[j].id;
		btnCode.innerHTML = "En savoir plus";
		btnCodeLink.appendChild(btnCode);
		liste_btnCode.appendChild(btnCodeLink);


		if (typeof data_application[j].CodePY !== "undefined") {
			btnCodeLink = document.createElement("A");
			btnCode = document.createElement("BUTTON");
			btnCodeLink.href = "./codes_python/" + data_application[j].CodePY;
			btnCode.setAttribute('download', "./codes_python/" + data_application[j].CodePY);
			btnCode.innerHTML = "Code Python";
			btnCodeLink.appendChild(btnCode);
			liste_btnCode.appendChild(btnCodeLink);
		}
		if (typeof data_application[j].CodeJS !== "undefined") {
			btnCodeLink = document.createElement("A");
			btnCode = document.createElement("BUTTON");
			btnCodeLink.href = './AppJS/' + data_application[j].codeJS;
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

}