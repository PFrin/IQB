import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class Type(models.Model):
    idType = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True) 
    typeQuestion  = models.TextField(max_length=100)

class Customer(AbstractBaseUser):
    idCustomer     = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    mailCust       = models.TextField(max_length=100)
    loginCust      = models.CharField(max_length=100)

    USERNAME_FIELD = 'loginCust'
    EMAIL_FIELD    = 'mailCust'

class Form(models.Model):
    idForm           = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    title            = models.TextField(max_length=100)
    introText        = models.TextField(max_length=100, default="Binevenue sur notre formulaire.")
    concludingText   = models.TextField(max_length=100, default="Merci d\'avoir rempli notre formulaire.")
    CreationDate     = models.DateTimeField(auto_now_add=True)  # date de la création de l'objet
    MEPDate          = models.DateTimeField()
    lastModifiedDate = models.DateTimeField(auto_now=True)      # date de la derniere modification de l'objet
    isOnline         = models.BooleanField (default="false")
    Customer         = models.ForeignKey(Customer, on_delete=models.CASCADE)

class Page(models.Model):
    idPage = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    number = models.IntegerField()
    Form   = models.ForeignKey(Form, on_delete=models.CASCADE)

class Question(models.Model):
    idQuestion = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    title = models.TextField(max_length=100)
    type  = models.ForeignKey(Type, on_delete=models.CASCADE)
    page  = models.ForeignKey(Page, on_delete=models.CASCADE)
    isObligatory = models.BooleanField()
    nbrAnswerMin = models.IntegerField()
    nbrAnswerMax = models.IntegerField()

class Answer(models.Model):
    idQuestion = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    type       = models.ForeignKey(Type    , on_delete=models.CASCADE)
    Question   = models.ForeignKey(Question, on_delete=models.CASCADE)
    Answer     = models.TextField(max_length=100)

class User(models.Model):
    idUSer       = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    mailUser     = models.TextField(max_length=100)
    loginUser    = models.CharField(max_length=100)
    passwordUser = models.TextField(max_length=100)
    replayDate   = models.DateTimeField(auto_now_add=True) # date de la création de l'objet et donc de réponse au Form

class UserAnswer(models.Model):
    idUserAnswer = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    user         = models.ForeignKey(User    , on_delete=models.CASCADE)
    question     = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer       = models.ForeignKey(Answer  , on_delete=models.CASCADE)
    text         = models.TextField(max_length=100)
