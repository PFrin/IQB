console.log("createQuestion.js loaded");

function preview(myCustomer,formId){
    console.log("preview");
    console.log("Customer : " + myCustomer);
    //afficher l'utilisateur connecté
    console.log
    console.log("formId : " + formId);
    //var redirectUrl = '/' + myCustomer + '/form/' + formId.toString() + '/?preview=true';
    var redirectUrl = '/' + myCustomer + '/form/' + formId + '/?preview=true';
    console.log(redirectUrl);
    //document.location.href = redirectUrl;
    window.open(redirectUrl, '_blank');
}

function affichagedynamique(parametre) {
    console.log("La fonction affichage dynamique a été appelée.");
    console.log("parametre : " + parametre); 

    //récupéré l'élémeent avec id="lienQuestion" et le mettre dans une variable
    var modal = document.getElementById("lienQuestion");
    //parcourir les questions de la variable et les mettre dans une liste
    var all_question = modal.querySelectorAll('.question-item');
    console.log(all_question);
    //créer un tableau vide
    var elementsToHide = [];
    var elementsSelected = parametre;
    var indexElementsSelected = null;
    //parcourir la liste des question et afficher les id des questions et leur ordre
    Array.from(all_question).forEach(question => {
        question.style.color = " black"; //remetre les checkbox en focntion de la BD
        var idElement = question.getAttribute('data-question-id');
        console.log(idElement);
        console.log(idElement == elementsSelected);
        if (question.getAttribute('data-question-id') == elementsSelected) { //question sélectionnée
            console.log("question sélectionnée");
            console.log(question);
            elementsToHide.push(question);
            //récupérer la place de la question sélectionnée dans la liste
            indexElementsSelected = Array.from(all_question).indexOf(question);
        }
        else if (indexElementsSelected != null ) { //question suivante
            console.log("question suivante");
            console.log(question);
            elementsToHide.push(question);
        }
    }); 
    //parcourir le tableau elementsToHide et mettre les questions dans la fenetre modal en rouge
    //parcourir le tableau elementsToHide et mettre les questions dans la fenetre modal en rouge
    Array.from(elementsToHide).forEach(element => {
        element.style.color = "grey";
        var all_checkbox = element.querySelectorAll('input[type="checkbox"]');
        console.log(all_checkbox);
        Array.from(all_checkbox).forEach(checkbox => {
            checkbox.disabled = true;
        });
    });
}



//////////////////////////////////////////////////////////////////////////
//initialise le Text Area

function MajTextArea() {
    console.log("MajTextArea");
    var textArea = document.getElementById("id_question_text");
    var textAreaValue = textArea.value;
    var textAreaValueMaj = textAreaValue.toUpperCase();
    textArea.value = textAreaValueMaj;
    return textAreaValueMaj;
}

//function qui vérifie si le text area est correctement rempli :
    //nbr parenthese ouvrante = nbr parenthese fermante
    //toutes les réponses cochées sont dans le text area
    //cohérence des calculs, Réponse Opérteur Réponse 

function checkTextArea() {
    console.log("checkTextArea");
    var textArea = document.getElementById("id_question_text");
    var textAreaValue = textArea.value;
    var textAreaValueMaj = textAreaValue.toUpperCase();
    textArea.value = textAreaValueMaj;
    console.log(textAreaValueMaj);

    //vérifier si le text area est vide
    if (textAreaValueMaj == "") {
        console.log("text area vide");
        initTextArea();
        return false;
        
    }else { //vérifier le nombre de parentheses ouvrantes et fermantes
        console.log("text area non vide");
        var nbrParentheseOuvrante = 0;
        var nbrParentheseFermante = 0;
        for (var i = 0; i < textAreaValueMaj.length; i++) {
            if (textAreaValueMaj[i] == "(") {
                nbrParentheseOuvrante += 1;
            }
            if (textAreaValueMaj[i] == ")") {
                nbrParentheseFermante += 1;
            }
        }
        console.log("nbrParentheseOuvrante : " + nbrParentheseOuvrante);
        console.log("nbrParentheseFermante : " + nbrParentheseFermante);
        if (nbrParentheseOuvrante != nbrParentheseFermante) {
            console.log("il y a une erreur dans le text area");
            return false;
        }else {
            console.log("il n'y a pas d'erreur dans le text area");
            nbrParentheseFermante = 0;
            //cohérence des calculs, Réponse Opérteur Réponse
            //toutes les réponses cochées sont dans le text area

            return true;
        }
    }

}