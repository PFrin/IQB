from .defaults import *
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, Permission, PermissionsMixin

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
        return self.get(loginCust=username)


class Customer(AbstractBaseUser, PermissionsMixin):
    idCustomer = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    mailCust = models.EmailField(max_length=100, unique=True)
    loginCust = models.CharField(max_length=100, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomerManager()

    EMAIL_FIELD = 'mailCust'
    USERNAME_FIELD = 'loginCust'
    REQUIRED_FIELDS = ['loginCust']
    REQUIRED_FIELDS = ['mailCust']

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

    def publier(self):
        self.isOnline = True
        self.save()


class Page(models.Model):
    idPage = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    number = models.IntegerField()
    Form   = models.ForeignKey(Form, on_delete=models.CASCADE)

    def ajouter_page(self):
        current_page_number = self.number
        new_page_number = current_page_number + 1

        # Décaler les pages suivantes de +1
        pages_to_update = self.Form.page_set.filter(number__gte=new_page_number)
        for page in pages_to_update:
            page.number += 1
            page.save()

        # Créer nouvelle page avec le bon numéro
        new_page = Page(number=new_page_number, Form=self.Form)
        new_page.save()

        #ajouter une question à la page
        new_page.add_init_question()
        new_page.save()

        return new_page
    
    def add_init_question(self):

        # Récupérer le type de question par défaut depuis DEFAULT_QUESTION_TYPE
        question_type = Type.objects.get(typeQuestion=DEFAULT_QUESTION_TYPE)
        
        # Récupérer les paramètres de question par défaut
        question_defaults = DEFAULT_QUESTION_DEFAULTS.get(DEFAULT_QUESTION_TYPE)
        is_obligatory = question_defaults.get('isObligatory')
        nbr_answer_min = question_defaults.get('nbrAnswerMin')
        nbr_answer_max = question_defaults.get('nbrAnswerMax')

        # Créer la nouvelle question avec l'ordre spécifié
        question = Question.objects.create(
            type=question_type,
            page=self,
            isObligatory=is_obligatory,
            nbrAnswerMin=nbr_answer_min,
            nbrAnswerMax=nbr_answer_max,
            order=0
        )

        # Ajouter des réponses par défaut à la nouvelle question
        response_defaults = DEFAULT_RESPONSE_DEFAULTS.get(DEFAULT_QUESTION_TYPE, {})
        responses = response_defaults.get('responses', [])
        for response in responses:
            question.add_answer(response)

        return question


    def supprimer_page(self):
        page_number = self.number
        self.delete()

        # Décaler les numéros de page des pages suivantes de -1
        pages_to_update = self.Form.page_set.filter(number__gt=page_number)
        for page in pages_to_update:
            page.number -= 1
            page.save()


class Question(models.Model):
    idQuestion = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    title = models.TextField(max_length=100)
    type  = models.ForeignKey(Type, on_delete=models.CASCADE)
    page  = models.ForeignKey(Page, on_delete=models.CASCADE)
    isObligatory = models.BooleanField()
    nbrAnswerMin = models.IntegerField()
    nbrAnswerMax = models.IntegerField()
    order = models.IntegerField()

    def __str__(self):
        return self.title

    def add_question(self):
        # Vérifier si le nombre maximal de questions est atteint
        if self.page.question_set.count() >= NUMBER_MAX_QUESTION:
            raise ValueError("Le nombre maximal de questions pour ce formulaire a été atteint.")
        
        # Récupérer le type de question par défaut depuis DEFAULT_QUESTION_TYPE
        question_type = Type.objects.get(typeQuestion=DEFAULT_QUESTION_TYPE)
        
        # Récupérer les paramètres de question par défaut
        question_defaults = DEFAULT_QUESTION_DEFAULTS.get(DEFAULT_QUESTION_TYPE)
        is_obligatory = question_defaults.get('isObligatory')
        nbr_answer_min = question_defaults.get('nbrAnswerMin')
        nbr_answer_max = question_defaults.get('nbrAnswerMax')

        # Récupérer l'ordre de la nouvelle question
        current_question_order = self.order
        new_question_order = current_question_order + 1

        # Décaler les questions suivantes de +1
        questions_to_update = self.page.question_set.filter(order__gt=new_question_order)
        for q in questions_to_update:
            q.order += 1
            q.save()

        # Créer la nouvelle question avec l'ordre spécifié
        question = Question.objects.create(
            type=question_type,
            page=self.page,
            isObligatory=is_obligatory,
            nbrAnswerMin=nbr_answer_min,
            nbrAnswerMax=nbr_answer_max,
            order=new_question_order
        )

        # Ajouter des réponses par défaut à la nouvelle question
        response_defaults = DEFAULT_RESPONSE_DEFAULTS.get(DEFAULT_QUESTION_TYPE, {})
        responses = response_defaults.get('responses', [])
        for response in responses:
            question.add_answer(response)

        return question
    
    def add_answer(self,text):
        new_answer = Answer.objects.create(
            type = self.type,
            Question= self,
            Answer = text
        )
        return new_answer
    
    def add_answer(self):
        text = "Réponse " + str(self.answer_set.count() + 1)
        self.add_answer(self, text)
    

    

    def delete_question(self):
        #vérifier si c'est la derniere question de la page 
        if self.page.question_set.count() == 1:
            raise ValueError("Impossible de supprimer la dernière question de la page.")
        else :
            self.delete()


        # Décaler les ordres des questions suivantes de -1
        questions_to_update = self.page.question_set.filter(order__gt=self.order)
        for q in questions_to_update:
            q.order -= 1
            q.save()

    def swap_order_with(self, direction):
        if direction == 'haut':
            if self.order == 0:
                print("La question est déjà en haut.")
                return
            else:
                # Obtenir la question précédente avec un ordre inférieur
                try:
                    other_question = self.page.question_set.get(order=self.order - 1)
                except Question.DoesNotExist:
                    print("La question précédente n'existe pas.")
                    return

                other_question.order += 1
                other_question.save()

                self.order -= 1
                self.save()
                print("La question a été déplacée vers le haut.")

        elif direction == 'bas':
            # Vérifier si une question suivante existe
            if not self.page.question_set.filter(order__gt=self.order).exists():
                print("La question est déjà en bas.")
                return
            else:
                # Obtenir la question suivante avec un ordre supérieur
                try:
                    other_question = self.page.question_set.get(order=self.order + 1)
                except Question.DoesNotExist:
                    print("La question suivante n'existe pas.")
                    return

                other_question.order -= 1
                other_question.save()

                self.order += 1
                self.save()
                print("La question a été déplacée vers le bas.")

        else:
            print("Direction invalide. Utilisez 'haut' ou 'bas'.")



    
    def swap_question_type(self, question_type):
        print("Changement du type de question en cours...")
        print("Ancien type de question : {}".format(self.type))
        print("Nouveau type de question : {}".format(question_type))
        questionType = Type.objects.get(typeQuestion=question_type)
        # Vérifier si le type de question est déjà le même
        if self.type.typeQuestion == questionType:
            print("Le type de question est déjà le même.")
            return

        # Vérifier si l'ancien type ou nouveau est ouvert ou à échelle
        old_type_is_open_likert = self.type in ['ouvert', 'échelle']
        new_type_is_open_likert = questionType in ['ouvert', 'échelle']

        if old_type_is_open_likert or new_type_is_open_likert:
            # Supprimer les réponses existantes
            self.answer_set.all().delete()

            # Initialiser les paramètres par défaut du nouveau type
            question_defaults = DEFAULT_QUESTION_DEFAULTS.get(questionType)
            is_obligatory = question_defaults.get('isObligatory')
            nbr_answer_min = question_defaults.get('nbrAnswerMin')
            nbr_answer_max = question_defaults.get('nbrAnswerMax')

            # Changer le type de question et les paramètres
            self.type = Type.objects.get(typeQuestion=questionType)
            self.isObligatory = is_obligatory
            self.nbrAnswerMin = nbr_answer_min
            self.nbrAnswerMax = nbr_answer_max

        else:
            # Changer seulement le type de question
            self.type = Type.objects.get(typeQuestion=questionType)

             # Calculer le nombre de réponses total existantes
            nbr_answer_total = self.answer_set.count()
            
            # Modifier le nombre de réponses minimum et maximum
            if questionType == 'choix_multiple':
                self.nbrAnswerMin = DEFAULT_QUESTION_DEFAULTS['choix_multiple']['nbrAnswerMin']
                self.nbrAnswerMax = nbr_answer_total
            elif questionType == 'choix_unique':
                self.nbrAnswerMin = DEFAULT_QUESTION_DEFAULTS['choix_unique']['nbrAnswerMin']
                self.nbrAnswerMax = DEFAULT_QUESTION_DEFAULTS['choix_unique']['nbrAnswerMax']

        self.save()

    def delete_answer(self, answer_id):
        Answer.objects.filter(idAnswer=answer_id, Question=self).delete()

    def duplicate_question(self):
        new_question = Question.objects.create(
            title=self.title,
            type=self.type,
            page=self.page,
            isObligatory=self.isObligatory,
            nbrAnswerMin=self.nbrAnswerMin,
            nbrAnswerMax=self.nbrAnswerMax,
            order=self.order + 1
        )

        for answer in self.answer_set.all():
            Answer.objects.create(
                type=answer.type,
                Question=new_question,
                Answer=answer.Answer
            )

        return new_question

    def set_nbr_Answer_Min(self, nbr):
        total_answers = self.answer_set.count()

        if nbr <= 0:
            raise ValueError(self.ERROR_MIN_ANSWER_INVALID)
        elif nbr > total_answers:
            raise ValueError(self.ERROR_MIN_ANSWER_EXCEEDED_TOTAL)
        elif nbr > self.nbrAnswerMax:
            raise ValueError(self.ERROR_MAX_ANSWER_INVALID)

        self.nbrAnswerMin = nbr
        self.save()

    def set_nbr_Answer_Max(self, nbr):
        total_answers = self.answer_set.count()

        if nbr < self.nbrAnswerMin:
            raise ValueError(self.ERROR_MAX_ANSWER_INVALID)
        elif nbr > total_answers:
            raise ValueError(self.ERROR_MAX_ANSWER_EXCEEDED_TOTAL)

        self.nbrAnswerMax = nbr
        self.save()

    def set_isObligatory(self):
        self.isObligatory = not self.isObligatory
        self.save(update_fields=['isObligatory'])

class Answer(models.Model):
    idAnswer   = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    type       = models.ForeignKey(Type    , on_delete=models.CASCADE)
    Question   = models.ForeignKey(Question, on_delete=models.CASCADE)
    Answer     = models.TextField(max_length=100)

    def __str__(self):
        return str(self.idAnswer)
    
    def delete_answer(self):
        self.delete()


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

class QuestionDependency(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    dependent_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='dependency')

    def __str__(self):
        return f"{self.answer} -> {self.dependent_question}"

    def get_dependent_questions(cls, answer):
        """
        Renvoie la liste des questions dépendantes de la réponse donnée.
        """
        return [dependency.dependent_question for dependency in cls.objects.filter(answer=answer)]

    def get_dependent_answers(cls, question):
        """
        Renvoie la liste des réponses dépendantes de la question donnée.
        """
        return [dependency.answer for dependency in cls.objects.filter(dependent_question=question)]

    def add_dependency(cls, answer, dependent_question):
        cls.objects.create(answer=answer, dependent_question=dependent_question)

    def remove_dependency(cls, answer, dependent_question):
        cls.objects.filter(answer=answer, dependent_question=dependent_question).delete()
