from imaplib import _Authenticator
from django import forms
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate

# Create your views here.
from django.http import Http404, HttpResponse
from django.template import loader
from polls.models import Customer
from .models import User
from django.shortcuts import render
from .models import Customer
from .models import Form
from django.contrib.auth.decorators import login_required
from polls.allForms import LoginForm, CreateForm, CreateQuestion

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

def home(request):
  return HttpResponse('bonjour à tous')

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


#def details(request, loginCust):
#  myCustomer = Customer.objects.get(loginCust=loginCust)
#  template = loader.get_template('polls/details.html')
#  context = {
#    'myCustomer': myCustomer,
#  }
#  return HttpResponse(template.render(context, request))




def formCreate(request):
  form = CreateForm()
  return render(request, 'polls/Create.html',{'form' : form})

def questionCreate(request):
  form = CreateQuestion()
  return render(request, 'polls/CreateQuestion.html',{'form' : form})


##############################
#  Connexion et déconnexion  #
##############################

def home(request):
  return render(request, 'polls/index.html')

def login(request):
  try:
    form = LoginForm()
    message = ''
    if request.method == 'POST':
      form = LoginForm(request.POST)
      if form.is_valid():
        Customer = authenticate(
          username=form.cleaned_data['loginCust'],
          password=form.cleaned_data['password'],
        )
        if Customer is not None:
          login(request, Customer)
          print(Customer.get_username + "user ")
          message = 'Identifiants valide.'
          return redirect("./"+Customer.get_username)
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



