document.addEventListener("DOMContentLoaded", function() {
    // Fonction pour sélectionner une question et désélectionner les autres
    function selectQuestion(question) {
        var questions = document.getElementsByClassName("question-container");
        for (var i = 0; i < questions.length; i++) {
            var currentQuestion = questions[i];
            if (currentQuestion === question) {
                currentQuestion.classList.add("selected");
            } else {
                currentQuestion.classList.remove("selected");
            }
        }
    }

    // Écouteur d'événement pour appeler la fonction selectQuestion lors du clic sur une question
    var questions = document.getElementsByClassName("question-container");
    for (var i = 0; i < questions.length; i++) {
        questions[i].addEventListener("click", function() {
            selectQuestion(this);
        });
    }

    // Sélectionnez toutes les balises avec la classe "editable"
    const editableElements = document.querySelectorAll('[contenteditable="true"]');

    // Ajoutez un écouteur d'événements pour chaque balise
    editableElements.forEach(element => {
        // Stockez la valeur d'origine dans un attribut personnalisé
        element.setAttribute('data-original-value', element.textContent);

        element.addEventListener('blur', () => {
            const id = element.getAttribute('id');
            const value = element.textContent; // Récupérez la valeur modifiée

            // Créez l'objet de données à envoyer dans la requête
            const data = {
              id: id,
              value: value
            };
            console.log(data);
            // Effectuez une requête AJAX avec jQuery
            $.ajax({
              type: 'POST',
              url: '{% url "QuestionView" loginCust='+loginCust+' idForm='+idForm+' %}', // l'URL vue Django
              data: data,
              success: function(response) {
                  // Gérez la réponse du serveur en cas de succès
                  console.log('Mise à jour réussie');
              },
              error: function(error) {
                  // Gérez les erreurs de la requête AJAX
                  console.error('Erreur lors de la mise à jour', error);

                  // Récupérez la valeur d'origine et rétablissez-la
                  const originalValue = element.getAttribute('data-original-value');
                  element.textContent = originalValue;
              }
            });
        });
    });
});


/*
  // Sélectionnez toutes les balises avec la classe "editable"
  const editableElements = document.querySelectorAll('.editable');

  // Ajoutez un écouteur d'événements pour chaque balise
  editableElements.forEach(element => {
    element.addEventListener('input', () => {
      // Obtenez l'ID de l'élément
      const id = element.getAttribute('id');
      
      // Obtenez le nouveau contenu modifié
      const content = element.textContent;
      
      // Données à envoyer dans la requête AJAX
      const data = {
        'action': 'addPage',
        'idForm': id,
        'content': content,
      };

      // Requête AJAX en utilisant jQuery
      $.ajax({
        type: 'POST',
        url: "{% url 'QuestionView' loginCust=CurrentloginCust idForm=myForm.idForm %}",
        data: data,
        success: function(response) {
          if (response.success) {
            console.log("Succès");
            // Supprimer la question dynamiquement ou rafraîchir la page
            location.reload();
          } else {
            console.log("Échec");
          }
        },
        error: function(error) {
          console.log("Erreur lors de la requête AJAX :", error);
        }
      });
    });
  });
*/
  