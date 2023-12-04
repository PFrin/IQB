src="https://code.jquery.com/jquery-3.6.4.min.js"
//SCRIPT pour gérer l'ouverture et la fermeture de la fenêtre modale
document.addEventListener("DOMContentLoaded", function () {
  var openModalButton = document.getElementById('openModalButton');
  var closeModalButton = document.getElementById('closeModalButton');
  var modal = document.getElementById('modal');
  var applyStyleButton = document.getElementById('applyStyleButton');

  openModalButton.addEventListener('click', function () {
    modal.style.display = 'block';

    var fileNameCss = formId+".css";
    console.log(fileNameCss);
    applyStyleValues(fileNameCss);

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
      if (xhr.readyState == 4 && xhr.status == 200) {
        var styleContent = xhr.responseText;

        // À ce stade, styleContent contient le contenu du fichier de style.
        // Vous pouvez maintenant extraire les valeurs et les appliquer aux champs correspondants.
        applyStyleValues(styleContent);
      }
    };
    xhr.open('GET', '../../../static/IQB/css/' + fileNameCss, true);
    console.log(fileNameCss);
    console.log(xhr);
    xhr.send();
  });

  closeModalButton.addEventListener('click', function () {
    modal.style.display = 'none';
  });

  applyStyleButton.addEventListener('click', function () {
    var backgroundColor = document.getElementById('backgroundColor').value;
    var fontFamily = document.getElementById('fontFamily').value;
    var textColor = document.getElementById('textColor').value;
    var backgroundFormColor = document.getElementById('backgroundFormColor').value;

    var styleCSS = `
      body {
        background-color: ${backgroundColor};
        font-family: ${fontFamily};
        color: ${textColor};
      }
      .content {
        background-color: ${backgroundFormColor};
      }
    `;


    //récupérer l'image du drag and drop
    
    var profileImageInput = document.getElementById('profileImageInput');
    var fileName = profileImageInput.name;
    var fileInput = profileImageInput.fileInput;

    //url courant
    var url = window.location.href;

      
    var input = $('#profileImageInput')[0];
    var file = input.files[0];

    if (file) {
      console.log("fichier trouvé");
      console.log(file);
      var reader = new FileReader();
      reader.onload = function(e) {
          // Convert the image to base64
          var base64Image = e.target.result;

          // Send the base64-encoded image to the Django view
          uploadBase64Image(base64Image);
          
          console.log("image envoyée"); 
      };
      reader.readAsDataURL(file);
    }
    else{
      console.log("juste le style");
      uploadStyle();
      
    }

    function uploadBase64Image(base64Image) {
      $.ajax({
        url: url,
        type: 'POST',
        data: { 'image': base64Image, 'styleCSS': styleCSS },
        success: function(response) {
          console.log('Image envoyée avec succès !');
          console.log(response);
          console.log(response.media);
          
          
        },
        error: function(error) {
          console.error('Erreur lors de l\'envoi de l\'image : ', error);
        }
      });
    }

    function uploadStyle() {
      $.ajax({
        url: url,
        type: 'POST',
        data: { 'styleCSS': styleCSS },
        success: function(response) {
          console.log('style envoyée avec succès !');
          console.log(response);
        },
        error: function(error) {
          console.error('Erreur lors de l\'envoi de l\'image : ', error);
        }
      });
    }
    // Fermer la fenêtre modale
    modal.style.display = 'none';

  });

  // revoir
  // Fonction pour remplir la liste déroulante avec les fichiers de style disponibles
  function populateStyleFileOptions() {
    // récuperer les fichiers css disponibles dans le dossier static



    var styleFiles = ['default.css', 'StyleDynamique.css']; // Ajoutez d'autres fichiers si nécessaire
    var styleFileSelect = document.getElementById('styleFileSelect');

    for (var i = 0; i < styleFiles.length; i++) {
      var option = document.createElement('option');
      option.value = styleFiles[i];
      option.text = styleFiles[i];
      styleFileSelect.add(option);
    }
  }

  // Appeler la fonction pour remplir la liste déroulante au chargement de la page
  populateStyleFileOptions();

  // Fonction pour charger le fichier CSS de style sélectionné
  document.getElementById('loadStyleButton').addEventListener('click', function () {
    var styleFileSelect = document.getElementById('styleFileSelect');
    var fileName = styleFileSelect.options[styleFileSelect.selectedIndex].value;

    // Charger le fichier de style sélectionné
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
      if (xhr.readyState == 4 && xhr.status == 200) {
        var styleContent = xhr.responseText;

        // À ce stade, styleContent contient le contenu du fichier de style.
        // Vous pouvez maintenant extraire les valeurs et les appliquer aux champs correspondants.
        applyStyleValues(styleContent);
      }
    };
    xhr.open('GET', '../../../static/IQB/css/' + fileName, true);
    console.log(fileName);
    console.log(xhr);
    xhr.send();
  });


  function applyStyleValues(styleContent) {
    // Définir des expressions régulières pour extraire les valeurs de couleur, police, etc.
    var backgroundColorRegex = /background-color:\s*([^;]+);/;
    var fontFamilyRegex = /font-family:\s*([^;]+);/;
    //var textColorRegex = /color:\s*#([a-fA-F\d]{6}|[a-fA-F\d]{3});/; // Couleur hexadécimale
    var textColorRegex = /(?<!-)\bcolor:\s*([^;]+);/
    var backgroundFormColorRegex = /\.content\s*\{\s*background-color:\s*([^;]+);/;

    // Extraire les valeurs avec les expressions régulières
    var backgroundColorMatch = styleContent.match(backgroundColorRegex);
    var fontFamilyMatch = styleContent.match(fontFamilyRegex);
    var textColorMatch = styleContent.match(textColorRegex);
    console.log(textColorMatch);
    var backgroundFormColorMatch = styleContent.match(backgroundFormColorRegex);
    
    // Récupérer les valeurs correspondantes ou une chaîne vide si aucune correspondance
    var backgroundColor = backgroundColorMatch ? backgroundColorMatch[1] : '';
    var fontFamily = fontFamilyMatch ? fontFamilyMatch[1] : '';
    var textColor = textColorMatch ? textColorMatch[1] : '';
    var backgroundFormColor = backgroundFormColorMatch ? backgroundFormColorMatch[1] : '';
  
    // Appliquer les valeurs aux champs correspondants
    document.getElementById('backgroundColor').value = backgroundColor;
    document.getElementById('fontFamily').value = fontFamily;
    document.getElementById('textColor').value = textColor;
    document.getElementById('backgroundFormColor').value = backgroundFormColor;
  }
});



///////////////////
// DRAG and DROP //
///////////////////

// Ajoutez ces scripts à votre fichier JavaScript
document.addEventListener('DOMContentLoaded', function () {
  const dropZone = document.getElementById('dropZone');
  const profileImageInput = document.getElementById('profileImageInput');

  dropZone.addEventListener('dragover', function (e) {
    e.preventDefault();
    dropZone.classList.add('dragover');
  });

  dropZone.addEventListener('dragleave', function () {
    dropZone.classList.remove('dragover');
  });

  dropZone.addEventListener('drop', function (e) {
    e.preventDefault();
    dropZone.classList.remove('dragover');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      const imageFile = files[0];

      // Mettez à jour le label pour afficher le nom du fichier (facultatif)
      dropZone.querySelector('.drop-zone__prompt').innerText = imageFile.name;

      // Mettez à jour l'input de type fichier avec le fichier sélectionné
      profileImageInput.files = files;
    }
  });
});

// Ajoutez le gestionnaire d'événements pour détecter le changement de fichier
document.getElementById('imagePreviewContainer').style.display = 'none';
document.getElementById('profileImageInput').addEventListener('change', function (event) {
  console.log('test');
  // Obtenez l'élément d'aperçu de l'image
  var imagePreview = document.getElementById('imagePreview');

  // Obtenez le fichier sélectionné
  var selectedFile = event.target.files[0];

  // Vérifiez s'il y a un fichier sélectionné
  if (selectedFile) {
    // Créez un objet URL pour le fichier
    var objectUrl = URL.createObjectURL(selectedFile);

    // Mettez à jour l'attribut src de l'aperçu de l'image
    imagePreview.src = objectUrl;

    // Affichez l'aperçu de l'image
    document.getElementById('imagePreviewContainer').style.display = 'block';
    document.getElementById('drop-zone__prompt').style.display = 'none';
  } else {
    // Cachez l'aperçu de l'image s'il n'y a pas de fichier sélectionné
    document.getElementById('imagePreviewContainer').style.display = 'none';
    
  }
});

/*
A FAIRE DANS LA FENETRE MODAL :
*- Ouverture : 
 - Chargement : 
   - Liste déroulante à rempir avec les fichiers css disponibles
   - Remplir les valeurs des champs avec les valeurs du fichier css de la page ou avec les valeurs par défaut
- Interraction : 
* - Template css à appliquer :
*   - Cliquer le bouton "copier le Style"
*   - Remplis les champs en fonction des valeurs du fichier css choisi
  - LOGO :
*    - drag and drop
    - choisir un fichier
*    - afficher l'image
*    - afficher l'image et son nom
  - btn "appliquer le style" :
    -récupérer les valeurs des champs
      -envoyer les valeurs au fichier css de la page
  - btn "Rénitialiser le style" :
    - applique le style du fichier default.css
    - garde le logo de base ou met celui du fichier du form correspondant ?
- Cas particulier :
* - Fermer la fenêtre modale avec la croix garde les paramètre des champs mais ne fais rien d'autre
 - Pouvoir "appliquer le style" sans mettre de logo
*/