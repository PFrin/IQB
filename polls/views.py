from imaplib import _Authenticator
import os
from django import forms
import json
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import uuid
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.http import Http404, HttpResponse
from django.template import loader
from IQB import settings
from polls.models import Customer
from .models import *
from .models import Customer, Form, Question, Answer, Participant, ParticipantAnswer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from polls.allForms import CustomerCreationForm, LoginForm, CreateForm, CreateQuestion
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.template import loader
from .models import Customer, Form
from django.http import JsonResponse
from django.core import serializers
import base64
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.contrib.auth import logout
from django.shortcuts import redirect

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views import View
from django.core.serializers.json import DjangoJSONEncoder
import json
User = get_user_model()

def CreateForm(request,loginCust):
  myCustomer = Customer.objects.get(loginCust=loginCust)
  template = loader.get_template('polls/CreateForm.html')
  context = {
    'myClients': myCustomer,
  }
  return HttpResponse(template.render(context, request))

#def answerForm(request):
#  myUser = User.objects.all().values()
#  template = loader.get_template('answerForm.html')
#  context = {
#    'myClients': myUser,
#  }
#  return HttpResponse(template.render(context, request))         


#http://127.0.0.1:8000/details/cust1/
@csrf_exempt
@login_required
def details(request, loginCust):
  context = {}
  if not request.user.is_authenticated:
    return redirect('login')
  if request.method == "POST":
    action = request.POST.get("action")
    if action == "newForm":
      myCustomer = get_object_or_404(Customer, loginCust=loginCust)

      # Use the add_form method to create a new Form with default values
      form = Form()
      form.Customer = myCustomer
      new_form = form.add_form()
      print("ok")
      response_data = {
        'success': True,
        'latestFormId': new_form.idForm
      }
      return JsonResponse(response_data)
    if action == "deleteForm":
      formId = request.POST.get("formId")
      myForm = get_object_or_404(Form, idForm=formId)
      myForm.delete_form()
      
      response_data = {
        'success': myForm.delete_form(),
      }

      return JsonResponse(response_data)

  try:
    myCustomer = get_object_or_404(Customer, loginCust=loginCust)
    print("---------------------------")
    print (myCustomer)
    myOnlineForm = Form.objects.filter(isOnline=True)
    myFormUnderConstruction = Form.objects.filter(isOnline=False)
    print("myFormUnderConstruction : ", myFormUnderConstruction)
    print(type(myFormUnderConstruction))
    context = {
        'myCustomer': myCustomer,
        'myOnlineForm': myOnlineForm,
        'myFormUnderConstruction': myFormUnderConstruction,
        'is_user_authenticated': request.user.is_authenticated,
    }      
    return render(request, 'polls/details.html', context)
  except Customer.DoesNotExist:
    raise Http404("Customer does not exist")
      



@csrf_exempt
@login_required
def QuestionView(request,loginCust,idForm):
  idFormm = idForm
  #traitement des requetes 
  if request.method == "POST":
    action = request.POST.get("action")
    id_Form = request.POST.get('id')

    if action == "update_input":
      id = request.POST.get('id')
      value = request.POST.get('value')
      field = request.POST.get('field')

      # Vérifier le champ spécifié et mettre à jour la valeur correspondante
      if field == 'titleForm':
        object_form = Form.objects.get(idForm=id)
      elif field == 'Answer':
        object_form = Answer.objects.get(idAnswer=id)
      elif field == 'title':
        object_form = Question.objects.get(idQuestion=id)
      elif field == 'concludingText':
        object_form = Form.objects.get(idForm=id)
      elif field == 'introText':
        object_form = Form.objects.get(idForm=id)

      if object_form:
        setattr(object_form, field, value)
        object_form.save()
    
    if action == "questionParameter":
      print("questionParameter")
      id = request.POST.get("id") 
      object_question = Question.objects.get(idQuestion=id)
      type_question = request.POST.get('type_question')
      is_required = request.POST.get('is_required')
      if type_question == object_question.type.__str__():
        print("réponse possible et obligatoire")
        if object_question.isObligatory != is_required :
          object_question.set_isObligatory()
        else:
          pass
          #changer le nombre de réponses possible
      else:
        print("Changement du type de question en cours...")
        print("Ancien type de question : {}".format(object_question.type))
        print("Nouveau type de question : {}".format(type_question))
        #changer le type de question, les autres parametres sont déjà gérer dans la fonction
        print("_________________________")
        object_question.swap_question_type(type_question)

      object_question.save()

      # Nombre de réponse minimum : 1
      # Nombre de réponse maximum : 2
      # Choisir un type question
      # Question est obligatoire

    if action == "question_answer":
      print("question_answer")
      btn = request.POST.get('btn')
      print(btn)
      id_Question = request.POST.get('idQuestion')
      id_Answer = request.POST.get('idAnswer')
      object_Question = Question.objects.get(idQuestion=id_Question)
      if id_Answer is not None:
        object_answer = Answer.objects.get(idAnswer=id_Answer)

        if btn == 'Supprimer':
          print("Supprimer")
          #vérifier si la réponse est lié a une question
          object_answer.delete_answer()
      elif btn == 'Ajouter':
        print("ajouter")
        object_Question.add_answer()

      # Ajouter réponse
      # Suprimer supprimer
      # lier la réponse a des questions
    if action == "question_form":
      # Ajouter question
      # Suprimer Question
      # dupliquer Question
      # Lier des réponses a la question
      # Changer l'ordre des questions

      btn = request.POST.get('btn')
      id_Question = request.POST.get('id_Question')

      
      if id_Question!= '':
        object_Question = Question.objects.get(idQuestion=id_Question)
        print("object_Question : ", object_Question)
      
        if btn == 'supprimer':
          print("supprimer")
          object_Question.delete_question()
        elif btn == 'lier':
          pass
        elif btn == 'dupliquer':
          object_Question.duplicate_question()
        elif btn == 'ajouter':
          object_Question.add_question()
        elif btn == 'haut' or btn == 'bas':
          object_Question.swap_order_with(btn)
      else:
        #erreur pas de question sélectionné
        print("erreur pas de question sélectionné")


    if action == "form_page":
      nbr = request.POST.get('nbr')
      btn = request.POST.get('btn')
      
      object_form = Form.objects.get(idForm=id_Form)
      object_Page = object_form.page_set.get(number=nbr)

      if btn == 'addPage':
        object_Page.ajouter_page()
      elif btn == 'delPage':
        object_Page.supprimer_page()

    if action == "style_form":
      # mettre a jour le style css et sauvegarder les changement quelque part en base de donnée
      # pas encore fais !
      # stockage json ?? =
      pass
    if action =="publier":
      object_form = Form.objects.get(idForm=id_Form)
      object_form.publish()
      # mettre le form en ligne
      # pas encore fais !

    if action =="form_parametre":
      pass
      ##############################################
      #        fonctionalités mis en place        #
      ##############################################

      # aller sur la preview

      ##############################################
      #   fonctionalités pas encore mis en place   #
      ##############################################

      # Changer date de MEP
      # Publier Form
      # Affichage sur un ou plusieurs pages
    
    if action == "lien":
      modal = request.POST.get("Modal")
      idDepedentQuestion = request.POST.get("question")
      answer = request.POST.get("answer")
      info = request.POST.get("info")
      print("modal : ", modal) 
      print("question : ", idDepedentQuestion)
      print("answer : ", answer)
      print("info : ", info)
      print("post : ", request.POST)
      if modal == "lienQuestion":
        # Charger le JSON en tant qu'objet Python
        data = json.loads(info)

        # Accéder aux données
        modal = data["modal"]
        questions_data = data["questionsData"]
        CurrentQuestion = Question.objects.get(idQuestion=idDepedentQuestion)
        
        # Parcourir les données
        for question in questions_data:
          id_element = question["idElement"]
          formule = question["formule"]
          liste_answer = question["listeAnswer"]
          #afficher l'id des answer et si elles sont checked ou non
          CurrentQuestion = Question.objects.get(idQuestion=id_element)
          if( formule != "ancienne formule"):
            CurrentQuestion.dependency_formul = formule
            CurrentQuestion.save()

    return JsonResponse({"success": True})

      ##########################################
      #   info requise pour afficher la page   #
      ##########################################

  else:
    template = loader.get_template('polls/createQuestion.html')
    myType = Type.objects.all()
    form = CreateQuestion()
    myForm = Form.objects.get(idForm=idFormm)

    info_form_json = []
    info_form = []
    myPages = Page.objects.filter(Form=idForm).order_by('number')
    print(myPages)
    form_data = {
      'form': myForm,
      'pages': []
    }
    form_data_json = {
      'formTitle': myForm.titleForm,
      'pages': []
    }
    for page in myPages:
      myQuestions = Question.objects.filter(page=page).order_by('order')
      page_data = {
        'page': page,
        'questions': []
      }
      
      page_data_json = {
        'pageid': str(page.idPage),
        'pagenumber':str(page.number),
        'questions_json': []
      }
      for question in myQuestions:
        myAnswers = Answer.objects.filter(Question=question)
        question_data = {
          'question': question,
          'formumle': question.dependency_formul,
          'answers': myAnswers
        }
        question_data_json = {
          'idQuestion': str(question.idQuestion),
          'title': str(question.title),
          'order': str(question.order),
          'dependency_formul' : str(question.dependency_formul),
          'answers_json' : []
        }
        for answer in myAnswers:
          answer_data_json = {
            'idAnswer': str(answer.idAnswer),
            'answerCode': str(answer.Answer),
            'checked': False
          }
          question_data_json['answers_json'].append(answer_data_json)
        page_data_json['questions_json'].append(question_data_json)
        page_data['questions'].append(question_data)
      
      form_data['pages'].append(page_data)
      form_data_json['pages'].append(page_data_json)

    info_form.append(form_data)
    info_form_json.append(form_data_json)
    
    #info_form_json_str = json.dumps(info_form_json, default=str)
    #print("info_form_json_str : ", info_form_json_str)  # Utilisez info_form_json_str ici
    #info_form_jsons = json.dumps(info_form_json)
    print("ààààààààààààààààààààààààààà")
    print(info_form_json)
    #print(info_form_json_str)
    #print(type(info_form_json_str))
    
    customer = myForm.Customer
    CurrentloginCust = customer.loginCust
    context = {
      'myType': myType,
      'form': form,
      'info_form': info_form,
      'CurrentloginCust': CurrentloginCust,
      'myForm':myForm,
      'info_form_json': info_form_json,
      'is_user_authenticated': request.user.is_authenticated,
    }
    print("contexttttttttttttttttttttttttttttttttttttttttttttttttt")
    return HttpResponse(template.render(context, request))

'''       ANCIEN CODE DE QuestionView 
    if action == "update":
      key_question = request.POST.get("key_question")
      key_value = request.POST.get("key_value")
      key_id   = request.POST.get("key_id")
      key_type = request.POST.get("key_type")
      key_page = request.POST.get("key_page")
      key_name = request.POST.get("key_name")
      
      
      if key_type == "form":
        my_model_instance = Form.objects.get(idForm=key_id)
        if (key_name == "titleForm"):
          my_model_instance.titleForm= key_value
        elif key_name == "introText":
          pass
        elif key_name == "concludingText":
          pass
        elif key_name == "introText":
          pass
        elif key_name == "MEPDate":
          pass
        elif key_name == "isOnline":
          pass
      elif key_type == "page":
        my_model_instance = Page.objects.get(idPage=key_id)
        #number
      elif key_type == "question":
        my_model_instance = Question.objects.get(idQuestion=key_question)
        if (key_name == "titleForm"):
          my_model_instance.title = key_value
        elif key_name == "type":
          myNewType = Type.objects.get(typeQuestion=key_value)
          myAnswers = Answer.objects.filter(Question=my_model_instance)
          my_model_instance.type = myNewType      #mise a jour du type
          if (key_value== "choix multiple"):      #mise a jour des parametre
            my_model_instance.nbrAnswerMin = 1
            my_model_instance.nbrAnswerMax = myAnswers.count()
          elif key_value== "Question à échelle":
            my_model_instance.nbrAnswerMin = 1
            my_model_instance.nbrAnswerMax = 1
          elif key_value== "Choix unique":
            my_model_instance.nbrAnswerMin = 1
            my_model_instance.nbrAnswerMax = 1
          elif key_value== "question ouverte":
            for answer in myAnswers :
              answer.delete()
          
          #mise a jour des questions
          myAnswers = Answer.objects.filter(Question=my_model_instance)
          for answer in myAnswers :
            answer.type = myNewType
            
          
        elif key_name == "page":
          pass
        elif key_name == "isObligatory":
          my_model_instance.isObligatory = key_value
        elif key_name == "nbrAnswerMin":
          pass
        elif key_name == "nbrAnswerMax":
          pass
      elif key_type == "answer":
        answer_id = request.POST.get("answer_id")
        my_model_instance = Answer.objects.get(idAnswer=answer_id)
        my_model_instance.Answer = key_value
      
      if (my_model_instance != None):
        print("save")
        my_model_instance.save()

    if (action == "addQuestion"):
      key_page = request.POST.get("key_page")
      question = Question.objects.create(
        title="Question suivante",
        type_id=defaultType.idType,
        page_id=key_page,
        isObligatory=True,
        nbrAnswerMin=1,
        nbrAnswerMax=2,
      )
      question.save()
    
    if (action== "removeQuestion"):
      question_id = request.POST.get('question_id')
      question = Question.objects.get(idQuestion=question_id)
      question.delete()

    if (action== "duplicateQuestion"):
      question_id = request.POST.get('question_id')
      CpQuestion = Question.objects.get(idQuestion=question_id)
      NewQuestion = Question.objects.create(
        title        = "Copie Question",
        type      = CpQuestion.type,
        page      = CpQuestion.page,
        isObligatory = CpQuestion.isObligatory,
        nbrAnswerMin = CpQuestion.nbrAnswerMin,
        nbrAnswerMax = CpQuestion.nbrAnswerMax,
      )
      NewQuestion.save()

    if(action== "addAnswer"):
      question_id = request.POST.get('question_id')
      QuestionCourant = Question.objects.get(idQuestion=question_id)
      NewAnswer = Answer.objects.create(
        type     = QuestionCourant.type,
        Question = QuestionCourant,CurrentForm
        Answer   = "nouvelle réponse ",
      )
      NewAnswer.save()

    if(action=="removeAnswer"):
      idAnswer = request.POST.get("Answer")
      RmAnswer = Answer.objects.get(idAnswer=idAnswer)
      RmAnswer.delete()

    if(action=="addPage"):
      currentForm = Form.objects.get(idForm=idForm)
      NewPage = Page.objects.create(
        number = 1,
        Form   = currentForm,
      )
      NewPage.save()
      pass
    
    if(action=="publish"):
      pass

    return JsonResponse({"success": True})
    '''




#def nbr(request):
#  form = nbrAnswer()
#  nbrAnswerMin = form.cleaned_data['nbrAnswerMin'],
#  nbrAnswerMax = form.cleaned_data['nbrAnswerMax'],

def redirection(request,loginCust):
  # Trouver le dernier formulaire créé par l'utilisateur
  try:
    myCustomer = Customer.objects.get(loginCust=loginCust)
    latest_form = Form.objects.filter(Customer=myCustomer).latest('CreationDate')
        
  except Form.DoesNotExist:
    # Rediriger vers une autre vue si aucun formulaire n'est trouvé
    return redirect('details', loginCust=myCustomer.loginCust)

  redirect_url = '/'+loginCust+'/form/createQuestion/'+ str(latest_form.idForm)
  return redirect(redirect_url)


def formCreate(request):
  form = CreateForm()
  return render(request, 'polls/Create.html',{'form' : form})

#def questionCreate(request):
#  form = CreateQuestion()
#  return render(request, 'polls/CreateQuestion.html',{'form' : form})


##############################
#  Connexion et déconnexion  #
##############################

def home(request):
    if request.user.is_authenticated and isinstance(request.user, Customer):
      return render(request, 'polls/details.html')
    else:
      return render(request, 'polls/login.html')

import logging

# Création d'un objet logger
logger = logging.getLogger(__name__)

def login_view(request):
    print("login_view")
    context = {}
    if request.method == 'POST':
        print("POST")
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, loginCust=username, password=password)
            if user is not None and isinstance(user, Customer):
                login(request, user)
                logger.info('Utilisateur connecté avec succès: %s', user.loginCust)
                print(f"Utilisateur connecté avec succès: {user.loginCust}")  # Ajout d'un print
                return redirect('details', user.loginCust)
            else:
                error_message = 'Identifiants invalides.'
                logger.warning('Échec de l\'authentification pour l\'utilisateur: %s', username)
                print(f'Échec de l\'authentification pour l\'utilisateur: {username}')  # Ajout d'un print
                context = {
                    'form': form,
                    'error': error_message,
                    'is_user_authenticated': request.user.is_authenticated,
                }
                return render(request, 'polls/login.html', context)
        else:
            print("Formulaire invalide")
            print(form.errors)  # Afficher les erreurs de validation
    else:
        print("autre que POST")
    form = LoginForm()
    context = {
        'is_user_authenticated': request.user.is_authenticated,
        'form': form
    }
    print("Affichage du formulaire de connexion")
    return render(request, 'polls/login.html', context)





def register_view(request):
  if request.method == 'POST':
    form = CustomerCreationForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('login')
    else:
      print("Échec de l'inscription")
  else:
    form = CustomerCreationForm()
  return render(request, 'polls/register.html', {'form': form})


def logout_view(request):
  logout(request)
  return redirect('login')

#def answerFormView(request, formulaire_id,idUSer):
def answerFormView(request):
  myForm  = Form.objects.get(idForm="a0355265-9dc1-4edf-923f-d9c52c63adfa")
  myUser  = User.objects.get(idUSer="5bcff6f7-abc5-4996-86b4-bfa199f8332b")
  myPages = Page.objects.filter(Form=myForm).order_by('number')

  if request.method == 'POST':
    session_data = {}
    for key, value in request.POST.items():
      
      if key.startswith("answer_"):
        session_data[key] = value
        request.session[key] = value

    print("Sessions:")
    print(session_data)
    for key, value in session_data.items():
      print(key + ": " + value)

  else:
    session_data = {}

  context = {
    'myForm' : myForm,
    'myPages': myPages,
    'myUser' : myUser,
    'session_data': session_data
  }
  
  return render(request, 'polls/answerForm.html', context)


def preview_reponse(request, idForm):
  print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Mode aperçu concepteur !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
  return reponse(request, None, idForm)

@csrf_exempt
def reponse(request, username, idForm):
  #del request.session['form_data']
  
  action = request.POST.get("action")
  if action == "theEnd":
    print("theEnd") 
    #answerFormToBDDTheEnddd()
  #si il y a "TheEnd" dans l'URL afficher page de fin
  #if 'theEnd' in request.GET:
  #  return redirect('end')
    
  #clear la session
  #request.session.flush()
  print("------------------------")
  print("|        debug         |")
  print("------------------------")

  preview_doc = None
  #gestion des erreurs 

  try:
    myForm = Form.objects.get(idForm=idForm)
  except Form.DoesNotExist:
    return HttpResponse("Le formulaire n'existe pas")
  '''
  try:
    myParticipant = Participant.objects.get(loginParticipant=username)
  except :
    myParticipant = Participant()
    myParticipant = myParticipant.create_participant(username)
    return redirect('reponse', username=username, idForm=idForm) 
  '''
  condition = {'loginParticipant': username}
  objet_existe = Participant.objects.filter(**condition).exists()

  if objet_existe:
    print("L'objet existe.")
  else:
    print("L'objet n'existe pas.")
    myParticipant = Participant.objects.create(loginParticipant=username)
    print("myParticipant : ", myParticipant)
  
  
  
  
  
  
  request.session['myParticipant'] = username
  #recharger la page
  
  
  
  
  
  myPages = Page.objects.filter(Form=myForm).order_by('number')
  my_dependencies = list(QuestionDependency.objects.filter(dependent_question__page__Form=myForm))
  #print("my_dependencies : ", my_dependencies)
  
  my_dependencies_serialized = json.dumps([str(dep) for dep in my_dependencies])
  print("dependances :")
  print(my_dependencies_serialized)
  
  #vérifier si le formulaire existe
  ###########"
  # nouvel façon de gérer les dépendances"
  
  #faire une liste avec toutes les formules de questions
  depend = {}
  for page in myPages:
    for question in page.question_set.all():
      depend[str(question.idQuestion)] = question.dependency_formul
      
  print("depend : ", depend)
    

  #vérifier preview
  if request.method == 'GET':
    print("GET")
  elif request.method == 'POST':
    print("POST")
    preview_param = request.GET.get('preview', False)
    if preview_param == 'true':
      preview_doc = True
      print("Mode aperçu concepteur !")
      
      if 'styleCSS' in request.POST:
        print("Début traitement STYLE")
        style = request.POST['styleCSS']
        print("Style : ", style)

        # Créer un fichier CSS s'il n'existe pas
        filename = idForm + '.css'
        file_directory = settings.STATIC_POLLS4
        try:
          os.makedirs(file_directory, exist_ok=True)
        except OSError as e:
          print("Erreur lors de la création du dossier CSS :", e)

        print("File directory : ", file_directory)

        # Modifier le contenu du fichier CSS
        file_path = os.path.join(file_directory, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
          f.write(style)

        if 'image' in request.POST:
          print("Début traitement IMAGE")
          base64_image = request.POST['image']

          # Décodez la chaîne base64 en données binaires
          image_data = base64.b64decode(base64_image.split(',')[1])

          # Enregistrez l'image dans un fichier
          logo_path = settings.STATIC_LOGO_PATH + '/' + idForm + '.png'
          print("......................................................")
          print(logo_path)
          with open(logo_path, 'wb') as f:
            f.write(image_data)
            
          myForm.logo_path = logo_path
          myForm.save()

          return JsonResponse({'message': 'Image enregistrée avec succès.', 'logo_path': logo_path})

        return JsonResponse({'message': 'Style enregistré avec succès.'})
    
      
      
    else:
      
      preview_doc = False
      print("Mode normal.")
      #vérifier si le formulaire est en ligne
      if myForm.isOnline:
        print("Formulaire en ligne")
        #vérfier si le user a déjà des réponses avec le formulaire en cours dans la bd
        participant_Answer = ParticipantAnswer.objects.filter(Participant=myParticipant)
        if participant_Answer: #vérifier si il y a des réponses dans la bd
          return HttpResponse("L'utilisateur a déjà répondu")
      #sinon continuer 
      #vérifier si le formulaire est en ligne
      else:
        print("Formulaire hors ligne")
      
   
    def addCurrentFormToSession(form_data):
      print("Fct addCurrentFormToSession")
      newForm = {
        'id': str(myForm.idForm),
        'name': myForm.titleForm,
        'preview': preview_doc,
        'isanswered': False,
        'pages': []
      }
    
      for page in myPages:
        page_data = {
          'id': str(page.idPage),
          'name': str(page.number),
          'isanswered': False,
          'questions': []
        }
        questionPage = Question.objects.filter(page=page)
        questionPageOrder = questionPage.order_by('order')
        for question in questionPageOrder:
          question_data = {
            'id': str(question.idQuestion),
            'name': str(question.title),
            'type': str(question.type),
            'answer': [],
            'dependency_formul': str(question.dependency_formul)
          }
        
          page_data['questions'].append(question_data)

        newForm['pages'].append(page_data)

      form_data['forms'].append(newForm)
      #maj de la session 
      request.session['form_data'] = form_data

        # indentation auto:  Alt + Shift + F
        #enregistrer dans un fichier test.json
      with open('test.json', 'w') as outfile:
        json.dump(form_data, outfile)
      #enregistrer dans la session
      request.session['form_data'] = form_data

    try:
      form_data = request.session['form_data']
    except KeyError: #si form_data n'est pas dans la session
      form_data = {
        'forms': []
      }
    # Vérifiez si le formulaire existe déjà dans la session
    form_exists_in_session = False

    for form in form_data['forms']:
        if form['id'] == str(myForm.idForm):
            form_exists_in_session = True
            break

    # Si le formulaire n'existe pas dans la session, ajoutez-le
    if not form_exists_in_session:
        addCurrentFormToSession(form_data)
        print("Formulaire ajouté dans la session")
    else:
        print("Formulaire trouvé dans la session")


    form_data = request.session['form_data']

    #récupéré la valeur de l'id de chaque formulaire dans la session
    for form in form_data["forms"]:
      form_id = form["id"]
      print(f"ID du f ormulaire : {form_id}")
      if form_id == str(myForm.idForm):
        print("Le formulaire est dans la session ")
        #vérifier si le formulaire est en ligne ou non
        if not myForm.isOnline:
          #remplacer le formulaire dans la session par le formulaire en cours
          #form_data["forms"].remove(form)
          #form_data = addCurrentFormToSession()
          print("#form_data = addCurrentFormToSession()")
      else:
        print("form_data incomplet")
        print("form_data = addCurrentFormToSession()")
        #form_data = addCurrentFormToSession()
    if form_data == None:
      print("form_data vide")
      #form_data = addCurrentFormToSession()
      print("#form_data = addCurrentFormToSession()")

  print("____________________")
  print(request.POST)
  print("____________________")
  
  
  if request.method == 'POST':
    # Parcourir les questions du formulaire en session
    for form in form_data["forms"]:
      if form["id"] == str(myForm.idForm):
        for page in form["pages"]:
          for question in page["questions"]:
            # Récupérer toutes les réponses associées à la question
            question_answers = request.POST.getlist(question['id'])

            if question_answers:
              # Si des réponses sont présentes, les ajouter à la question
              question["answer"] = question_answers
              question["isanswered"] = True
            else:
              # S'il n'y a pas de réponse, marquer la question comme non répondu
              question["isanswered"] = False

    #maj de la session 
    request.session['form_data'] = form_data
    with open('test.json', 'w') as outfile:
      json.dump(form_data, outfile)
      
  #vérifier preview
  if request.method == 'GET':
    print("GETTTT")
    #si thenEnd est dans la requete
    for key in request.GET:
      if key == 'theEnd':
        print("theEndddddddddddd")
        answerFormToBDDTheEnd(request)
        if (answerFormToBDDTheEnd(request)):
          return redirect('end')
        


  print(myPages)
  print(type(myPages))
  all_questions = Question.objects.filter(page__in=myPages).order_by('order')
  print(all_questions)

  #réponses de la session
  user_responses = request.session.get('user_responses', {})

  context = {
    'myForm': myForm,
    'myPages': myPages,
    'all_questions': all_questions,
    'preview': preview_doc,
    'myDependencies': json.dumps(depend),
    'user_responses': user_responses.get(str(myForm.idForm), {})
  }
  
  #reponse(request, username, idForm):
  #return render(request, 'polls/answerForm.html ', context)
  #redirect_url = '/'+username+'/form/'+ idForm
  #return redirect(redirect_url)
  #return render(request, 'polls/answerForm.html', context)
  print("fin de la fonction reponse")
  return render(request, 'polls/answerForm.html', context)

def answerFormToBDDTheEnd(request):
    form_data = request.session.get('form_data')
    if not form_data:
      return redirect('end')  # Rediriger si les données du formulaire ne sont pas présentes en session

    myParticipant = request.session.get('myParticipant')
    if not myParticipant:
      return redirect('end')  # Rediriger si l'utilisateur n'est pas défini en session

    myParticipant = Participant.objects.get(loginParticipant=myParticipant)

    for form_info in form_data['forms']:
        form_obj = Form.objects.get(idForm=form_info['id'])
        for page in form_info['pages']:
            for question_info in page['questions']:
                question_id = question_info['id']
                answer_ids = question_info['answer']
                print("question_info")
                print(question_info)
                print("answer_ids")
                print(answer_ids)
                
                try:
                    question_obj = Question.objects.get(idQuestion=question_id)
                except Question.DoesNotExist:
                    # Gérez les erreurs comme vous le souhaitez (peut-être enregistrer l'erreur)
                    print("Question.DoesNotExist")
                    continue
                for answer_id in answer_ids:
                    if is_valid_uuid(answer_id):
                        try:
                            myAnswer = Answer.objects.get(idAnswer=answer_id)
                        except Answer.DoesNotExist:
                            myAnswer = None  # Définissez myAnswer sur None si l'objet n'existe pas pour gérer les deux cas.

                    if myAnswer is None:
                        # Créez la réponse si elle n'existe pas ou si l'UUID n'est pas valide
                        myAnswer = Answer.objects.create(
                            type=question_obj.type,
                            question=question_obj,
                            text=answer_id
                        )
                        myAnswer.save()
                    
                    answerText = myAnswer.Answer
                    
                    # Enregistrez ParticipantAnswer pour chaque réponse
                    ParticipantAnswer.objects.create(
                        Participant=myParticipant,
                        Form=form_obj,
                        question=question_obj,
                        answer=myAnswer,
                        text=answerText
                    )
                    print("answer")
                    print(myAnswer)
                    print(answerText)

    # Supprimez les données de session après les avoir traitées
    del request.session['form_data']
    print("redirection maintenant")
    # Redirigez l'utilisateur vers la page "end.html"
    return True


def end(request):
  print("end")
  return render(request, 'polls/end.html')

def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=version)
        return True
    except (ValueError, TypeError, AttributeError):
        return False


#def answerFormToDB(request):
  #récupérer les données du formulaire dans la session
  #enregistrer les données dans la base de données
  #redirect vers une page de fin vec le texte de conclusion du formulaire



#def reponse(request, username, idForm):
#vérifier si le user existe dans la base de données
#sinon le créer et l'ajouter dans la base de données
#vérifier si le formulaire existe

#vérifier si on est en preview ou non (paramètre dans l'url)
  #oui
    #pass
  #non
    #vérifier si le form est en ligne ou non
      #oui
        #vérfier si le user a déjà des réponses avec le formulaire en cours dans la bd
          #oui
            #return error form already answered
          #non
            #pass
      #non
        #return error form not online

#vérifier si les données du formulaire sont dans la session
  #non
    #récupérer les données du formulaire dans la base de données
    #initialiser le jsons contenant les données du formulaire
    #enregistrer jsons dans la session
  #oui
    #récupérer les données du formulaire dans la session
    #vérifier si le user a déjà répondu au formulaire courant(ATTETION : vérifier la valeur de preview dans le json)
      #oui
        #valeur des réponses du user dans le json seront préremplies dans le formulaire
      #non
        #initialiser le jsons contenant les données du formulaire courant
        #enregistrer jsons dans la session

#if request.method == 'POST':
  #parcourt les données du POST  ( for key, value in request.POST.items(): )
    #chercher la question correspondante dans le json
    #ajouter la réponse dans le json
    #enregistrer le json dans la session

#context
#return render(request, 'polls/answerForm.html', context)


#bouton Envoyer le Formulaire redirige vers une page de chargement
#dans la page de chargement, on récupère les données du formulaire dans la session
#on enregistre les données dans la base de données
#on supprime les données du formulaire dans la session
#on redirige vers une page de fin vec le texte de conclusion du formulaire
