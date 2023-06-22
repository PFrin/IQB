from imaplib import _Authenticator
from django import forms
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import uuid
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

# Create your views here.
from django.http import Http404, HttpResponse
from django.template import loader
from polls.models import Customer
from .models import User
from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
from polls.allForms import CustomerCreationForm, LoginForm, CreateForm, CreateQuestion
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.template import loader
from .models import Customer, Form
from django.http import JsonResponse
from django.core import serializers

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
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
@login_required
def details(request, loginCust):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "newForm":
            myCustomer = get_object_or_404(Customer, loginCust=loginCust)
            
            form = Form(titleForm='new Form', Customer_id=myCustomer.idCustomer)
            form.save(form.idForm)
            print("_____________________")
            print(form.idForm)
            serialized_form = serializers.serialize('json', [form], fields=('titleForm', 'Customer_id'))
            response_data = {
                'success': True,
                'latestFormId': serialized_form
            }
            return JsonResponse(response_data)

    try:
        myCustomer = get_object_or_404(Customer, loginCust=loginCust)
        myOnlineForm = Form.objects.filter(Customer=myCustomer, isOnline=True)
        myFormUnderConstruction = Form.objects.filter(Customer=myCustomer, isOnline=False)

        context = {
            'myCustomer': myCustomer,
            'myOnlineForm': myOnlineForm,
            'myFormUnderConstruction': myFormUnderConstruction
        }
        return render(request, 'polls/details.html', context)
    except Customer.DoesNotExist:
        raise Http404("Customer does not exist")


@csrf_exempt
def QuestionView(request,loginCust,idForm):

  #valeurs par défault
  defaultType = Type.objects.get(typeQuestion='Choix unique')
  if request.method == "POST":
    action = request.POST.get("action")
    if (action == "update"):
      key_question = request.POST.get("key_question")
      key_value = request.POST.get("key_value")
      key_id   = request.POST.get("key_id")
      key_type = request.POST.get("key_type")
      key_page = request.POST.get("key_page")
      key_name = request.POST.get("key_name")
      
      my_model_instance = None

      ##vérification des champs
      #vérif form
      #mise a jour des champs :
      if key_value == "false":
        key_value = False
      if key_value == "true":
        key_value = True

      if key_type == "form":
        my_model_instance = Form.objects.get(idForm=key_id)
        if (key_name == "titleForm"):
          pass 
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
        if (key_name == "title"):
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
        Question = QuestionCourant,
        Answer   = "nouvelle réponse ",
      )
      NewAnswer.save()

    if(action=="removeAnswer"):
      idAnswer = request.POST.get("Answer")
      RmAnswer = Answer.objects.get(idAnswer=idAnswer)
      RmAnswer.delete()

    return JsonResponse({"success": True})
  else:
    template = loader.get_template('polls/createQuestion.html')
    myType = Type.objects.all()
    form = CreateQuestion()
    myForm = Form.objects.get(idForm=idForm)

    info_form = []
    myPages = Page.objects.filter(Form=idForm)
    print(myPages)
    form_data = {
      'form': myForm,
      'pages': []
    }
    for page in myPages:
      myQuestions = Question.objects.filter(page=page)
      page_data = {
        'page': page,
        'questions': []
      }
      for question in myQuestions:
        myAnswers = Answer.objects.filter(Question=question)
        question_data = {
          'question': question,
          'answers': myAnswers
        }
        page_data['questions'].append(question_data)
      
      form_data['pages'].append(page_data)

    info_form.append(form_data)
    customer = myForm.Customer
    CurrentloginCust = customer.loginCust
    context = {
      'myType': myType,
      'form': form,
      'info_form': info_form,
      'CurrentloginCust': CurrentloginCust,
      'myForm':myForm,
    }
    return HttpResponse(template.render(context, request))




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
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, loginCust=username, password=password)
            if user is not None and isinstance(user, Customer):
                login(request, user)
                logger.info('Utilisateur connecté avec succès: %s', user.loginCust)
                #return HttpResponse("Ça fonctionne !")
                return redirect('details',  user.loginCust)
            else:
                error_message = 'Identifiants invalides.'
                logger.warning('Échec de l\'authentification pour l\'utilisateur: %s', username)
                return render(request, 'polls/login.html', {'form': form, 'error': error_message})
    else:
        form = LoginForm()
    return render(request, 'polls/login.html', {'form': form})



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


def logout(request):
  logout(request)
  pass

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
