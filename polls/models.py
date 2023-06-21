import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class Type(models.Model):
    idType = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True) 
    typeQuestion  = models.TextField(max_length=100)

    def __str__(self):
        return self.typeQuestion

class CustomerManager(BaseUserManager):
    def create_customer(self, mailCust, loginCust, password=None, **extra_fields):
        if not mailCust:
            raise ValueError("L'email est obligatoire.")
        if not loginCust:
            raise ValueError("Le nom d'utilisateur est obligatoire.")

        mailCust = self.normalize_email(mailCust)
        loginCust = self.model.normalize_username(loginCust)

        # Vérifier si un utilisateur avec la même adresse e-mail existe déjà
        if self.model.objects.filter(mailCust=mailCust).exists():
            raise ValueError("Un utilisateur avec cette adresse e-mail existe déjà.")

        customer = self.model(mailCust=mailCust, loginCust=loginCust, **extra_fields)
        customer.set_password(password)
        customer.save(using=self._db)
        return customer
    
    def create_superuser(self, mailCust, loginCust, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superutilisateur doit avoir is_superuser=True.')

        return self.create_customer(mailCust, loginCust, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(mailCust=username)


class Customer(AbstractBaseUser, PermissionsMixin):
    idCustomer = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    mailCust = models.EmailField(max_length=100, unique=True)
    loginCust = models.CharField(max_length=100, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomerManager()

    EMAIL_FIELD = 'mailCust'
    USERNAME_FIELD = 'mailCust'
    REQUIRED_FIELDS = ['loginCust']

    groups = models.ManyToManyField(Group, related_name='customer_users')
    user_permissions = models.ManyToManyField(Permission, related_name='customer_users')

    def save(self, *args, **kwargs):
        print(self.idCustomer)  #idCustomer lors de la création d'un nouvel utilisateur
        super().save(*args, **kwargs)

    def __str__(self):
        return self.loginCust

    def get_full_name(self):
        return self.loginCust

    def get_short_name(self):
        return self.loginCust
   

class Form(models.Model):
    idForm           = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    titleForm        = models.TextField(max_length=100)
    introText        = models.TextField(max_length=100, default="Binevenue sur notre formulaire.")
    concludingText   = models.TextField(max_length=100, default="Merci d\'avoir rempli notre formulaire.")
    CreationDate     = models.DateTimeField(auto_now_add=True)  # date de la création de l'objet
    MEPDate          = models.DateTimeField(blank=True, null=True)
    lastModifiedDate = models.DateTimeField(auto_now=True)      # date de la derniere modification de l'objet
    isOnline         = models.BooleanField (default="False")
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

    def __str__(self):
        return self.title

class Answer(models.Model):
    idAnswer   = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    type       = models.ForeignKey(Type    , on_delete=models.CASCADE)
    Question   = models.ForeignKey(Question, on_delete=models.CASCADE)
    Answer     = models.TextField(max_length=100)

    def __str__(self):
        return str(self.idAnswer)

class User(models.Model):
    idUSer       = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    mailUser     = models.TextField(max_length=100)
    loginUser    = models.CharField(max_length=100)
    passwordUser = models.TextField(max_length=100)
    replayDate   = models.DateTimeField(auto_now_add=True) # date de la création de l'objet et donc de réponse au Form

    def __str__(self):
        return self.loginUser

class UserAnswer(models.Model):
    idUserAnswer = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    user         = models.ForeignKey(User    , on_delete=models.CASCADE)
    question     = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer       = models.ForeignKey(Answer  , on_delete=models.CASCADE)
    text         = models.TextField(max_length=100)

    def __str__(self):
        return self.text