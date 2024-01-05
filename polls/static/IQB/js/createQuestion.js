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

function affichagedynamique(parametre,form_data_json) {
    console.log("La fonction affichage dynamique a été appelée.");
    console.log("parametre : " + parametre); 
    console.log("~~~~")

    //récupéré l'élémeent avec id="lienQuestion" et le mettre dans une variable
    var modal = document.getElementById("lienQuestion");
    //parcourir les questions de la variable et les mettre dans une liste
    var all_question = modal.querySelectorAll('.question-item');
    console.log("all_question");
    console.log(all_question);
    console.log("~~~~")
    //créer un tableau vide
    var elementsToHide = [];
    var elementsSelected = parametre;
    var indexElementsSelected = null;
    //initialise a vide
    var all_checkbox = modal.querySelectorAll("input[type='checkbox']");
    console.log('all_checkbox');
    console.log(all_checkbox);
    all_checkbox.forEach(checkbox => {
        checkbox.checked = false;
        console.log(checkbox);
    });


    //var form_data_json = "{{ info_form_json|safe }}";  

    //var form_data_json = document.getElementById('info_form_json').textContent;
    console.log('---> form_data_json <---');
    json = JSON.parse(form_data_json);
    console.log(json);
    var formule = document.getElementById("conditions");
    //formule.value = form_data_json[elementsSelected]['formule'];
    console.log("=====================================");
    //const formula = getFormulaById(parametre, json);
    //console.log(formula);
    formule.value = getFormulaById(parametre, json);
    //initCheckbox(formule.value);
    console.log("=====================================");




    //parcourir la liste des question et afficher les id des questions et leur ordre
    Array.from(all_question).forEach(question => {
        question.style.color = " black"; //remetre les checkbox en fonction de la BD
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
    initCheckbox(formule.value);
}

function getFormulaById(questionId, jsonData) {
    for (let i = 0; i < jsonData.length; i++) {
        const pages = jsonData[i].pages;
        for (let j = 0; j < pages.length; j++) {
            const questions = pages[j].questions_json;
            for (let k = 0; k < questions.length; k++) {
                if (questions[k].idQuestion === questionId) {
                    return questions[k].dependency_formul;
                }
            }
        }
    }
    // Retourne null si l'id de question n'est pas trouvé
    return null;
}

function initCheckbox(formule) {
    //renvoi les checkbox à leur état initial selon la formule
    console.log("initCheckbox");
    console.log(formule);
    lstAnswer = lstAnswerDepends(formule);
    console.log(lstAnswer);
    console.log("###########################################")
    //parcourir toutes les checkbox de la fenetre modal et les coher en fonction de la formule
    var modal = document.getElementById("lienQuestion");
    var all_checkbox = modal.querySelectorAll("input[type='checkbox']");
    console.log(all_checkbox);
    //check les checkbox qui sont dans la lstAnswer
    Array.from(all_checkbox).forEach(checkbox => {
        if (lstAnswer.includes(checkbox.value)) {
            checkbox.checked = true;
        }
    });

}

function lstAnswerDepends(formule){ 
    //servira a mettre des linerter qur ces réponses
    console.log("lstAnswerDepends");
    //tableau de toutes les réponses
    var lstCode = [];
  
    formule.replace(/Q[0-9]+R[0-9]+/g, function(match) {
      console.log("match : "+match);  
      lstCode.push(match);
    });
    console.log("lstCode : "+lstCode);
    console.log("###########################################")
    lstID = codeAnswerToID(lstCode);
    console.log("lstID : "+lstID);
    return lstCode;
  }

  function codeAnswerToID(codeAnswer) {
    var lstID = [];

    for (var i = 0; i < codeAnswer.length; i++) {
        var currentCode = codeAnswer[i];

        // Extract the answer number (after "R")
        var numberAnswer = currentCode.split("R")[1];

        // Extract the question number (after "Q")
        var numberQuestion = currentCode.split("Q")[1].split("R")[0];

        var id = "";

        // Get all question items
        var modal = document.getElementById("lienQuestion");
        var questionItems = modal.querySelectorAll(".question-item");
        console.log(questionItems);

        //aller a la numberQuestion question
        var questionItem = questionItems[numberQuestion - 1];
        console.log(questionItem);
        //aller a la l'input type checkbox numero numberAnswer
        var allChheckbox = questionItem.querySelectorAll("input[type='checkbox']");
        console.log(allChheckbox);
        var checkbox = allChheckbox[numberAnswer - 1];
        checkbox.checked = true;
    }

    return lstID;
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


