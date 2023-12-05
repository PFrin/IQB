//variables de pagination

////////////////////////////
// Charger les variables //
///////////////////////////

/////////////////////
// Changer de Page //
/////////////////////

// btn page suivante
function goToNextPage() {
    var currentPage = loadCurrentPage();
    var pageMax = loadPageMax();
    
    if (currentPage < totalPages && currentPage < pageMax) {
      currentPage = currentPage+1;
      pageMax = pageMax+1;
      console.log("currentPage : "+currentPage);
      saveCurrentPage(currentPage);
      savePageMax(pageMax)
  
      showCurrentPage(currentPage);
  
    }
    else{
      console.log("ALEDDDDDDDDD");
    }
  }
// btn Page précédente
function goToPreviousPage() {
    var currentPage = loadCurrentPage();
    if (currentPage > 1) {
  
      currentPage = currentPage-1;
  
      saveCurrentPage(currentPage);
  
      showCurrentPage(currentPage);
    }
  }


//////////////////////////////////
// Autorisation changer de Page //
//////////////////////////////////

// Toutes question obligatoire sont répondues
  function requireAutorisation() {
    const requiredQuestions = form.querySelectorAll('h3.obligatory');

  }


//////////////////////////
// Fonction d'affichage //
//////////////////////////

// Afficher la page actuelle
function showCurrentPage(currentPage) {
    var pages = document.querySelectorAll('.page');
    for (var i = 0; i < pages.length; i++) {
      if (i === currentPage - 1) {
        pages[i].style.display = 'block';
      } else {
        pages[i].style.display = 'none';
      }
    }
    
    // Gérer l'affichage des boutons "Page précédente" et "Page suivante"
    var prevButton = document.getElementById('prevPage');
    var nextButton = document.getElementById('nextPage');
    var submitButton = document.getElementById('submitForm');
  
    console.log("aaaaaaaaaaaaaaaaaaaaaaaaaaa");
    console.log("currentPage : "+currentPage);
    if (currentPage == 1) {
      prevButton.style.display = 'none';
    }
    else{
      prevButton.style.display = 'block';
      prevButton.disabled = false;
    }
  
    if (currentPage === totalPages) {
      nextButton.style.display = 'none';
      submitButton.style.display = 'block';
    } else {
      nextButton.style.display = 'block';
      submitButton.style.display = 'none';
    }
  }

//afficher les questions 


//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
/*
Charger les variables
Sauvegarder les variables

Affuichage : 
    Afficher la page actuelle
        P0   : intro 
        PN   : form
        PN+1 : conclusion
    Afficher les questions de la page actuelle
        Affichage des questions en focntion des dépendances 
    Afficher les boutons de navigation 


Changer de Page
    suivante
        
        btn page suivante
    précédente
        btn page précédente

Autorisation page suivante
    Toutes question obligatoire sont répondues ( Question dépendance obligatoirement obligatoire)
   
*/
