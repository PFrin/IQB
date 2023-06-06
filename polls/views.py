from imaplib import _Authenticator
from django import forms
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import uuid

# Create your views here.
from django.http import Http404, HttpResponse
from django.template import loader
from polls.models import Customer
from .models import User
from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
from polls.allForms import CustomerCreationForm, LoginForm, CreateForm, CreateQuestion

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
  try:
    myCustomer = Customer.objects.get(loginCust=loginCust)
    myOnlineForm = Form.objects.all().filter(
      Customer = myCustomer,
      isOnline = 'True'
    )
    myFormUnderConstruction = Form.objects.all().filter(
      Customer = myCustomer,
      isOnline = 'False',
    )
    template = loader.get_template('polls/details.html')
    context = {
      'myCustomer': myCustomer,
      'myOnlineForm':myOnlineForm,
      'myFormUnderConstruction':myFormUnderConstruction
    }
  except Customer.DoesNotExist:
    raise Http404("Question does not exist")
  return HttpResponse(template.render(context, request))



@csrf_exempt
def QuestionView(request):
  #valeurs par défault
  defaultType = Type.objects.get(typeQuestion='Choix unique')
  if request.method == "POST":  # Modifier cette ligne
    action = request.POST.get("action")
    if (action == "update"):
      key_question = request.POST.get("key_question")
      key_value = request.POST.get("key_value")
      key_id = request.POST.get("key_id")
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
        print(key_name)
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
      print(question)
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
    myForm = Form.objects.get(idForm="b6c03317-3efb-4eb8-9b72-b6aaa8788dda")

    info_form = []

    myPages = Page.objects.filter(Form=myForm)
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

    context = {
      'myType': myType,
      'form': form,
      'info_form': info_form,
    }
    return HttpResponse(template.render(context, request))




#def nbr(request):
#  form = nbrAnswer()
#  nbrAnswerMin = form.cleaned_data['nbrAnswerMin'],
#  nbrAnswerMax = form.cleaned_data['nbrAnswerMax'],



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
  return render(request, 'polls/index.html')

def loginView(request):
  try:
    form = LoginForm()
    message = ''
    if request.method == 'POST':
      form = LoginForm(request.POST)
      if form.is_valid():
        username=form.cleaned_data['loginCust'],
        password=form.cleaned_data['password'],
        Customer = authenticate(request, username=username, password=password)
        if Customer is not None:
          login(request, Customer)
          #print(Customer.get_username + "user ")
          message = 'Identifiants valide.'
          return redirect("./"+username)
        else:
          message = 'Identifiants invalides.'
    
    template = loader.get_template('polls/login.html')
    context = {
      'form' : form,
      'message': message
    }
  except Customer.DoesNotExist:
    raise Http404("Customers does not exist")
  return HttpResponse(template.render(context, request))

def register(request):
  form = CustomerCreationForm()
  if form.is_valid():
    form.save()
    return 
  return redirect(request, 'polls/register.html')

def logout(request):
  logout(request)
  pass


def answerFormView(request, formulaire_id,idUSer):
  formulaire = Form.objects.get(id=formulaire_id)
  pages = formulaire.page_set.all()

  context = {
   'formulaire': formulaire,
    'pages': pages
  }

  return render(request, 'answerForm.html', context)

