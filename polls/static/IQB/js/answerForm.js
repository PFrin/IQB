//variables de pagination
var curentPage = loadCurrentPage();
var pageMax = loadPageMax();

//charger la page actuelle à partir de la session
function loadCurrentPage() {
    var currentPage = sessionStorage.getItem(`${formId}_currentPage`);
    console.log("currentPage : "+currentPage);
    if (currentPage) {
      return parseInt(currentPage);
    }
    saveCurrentPage(1);
    return 1; // Valeur par défaut pour la première page
  }

//Charger la page max à partir de la session
function loadPageMax() {
    var pageMax = sessionStorage.getItem(`${formId}_pageMax`);
    console.log("pageMax : "+pageMax);
    if (pageMax) {
      if (pageMax > totalPages) {
        pageMax = totalPages;
      }
      return parseInt(pageMax);
    }
    savePageMax(2);
    return 2; // Valeur par défaut pour la première page
  }