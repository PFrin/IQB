from datetime import timezone
from datetime import date
from .defaults import *
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, Permission, PermissionsMixin

class Type(models.Model):
    idType = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    typeQuestion = models.TextField(max_length=100)

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
    isOnline         = models.BooleanField(default=False)
    Customer         = models.ForeignKey(Customer, on_delete=models.CASCADE)
    #css_file         = models.FileField(blank=True, null=False, default=STATIC_URL_STYLE + 'default.css')
    logo_path        = models.CharField(max_length=100, blank=True, null=False)
    
    def publish(self):
        self.MEPDate = date.today()
        self.isOnline = True
        self.save()
    
    #fonction pour ajouter un formulaire
    def add_form(self):

        # Récupérer les paramètres de formulaire par défaut
        form_defaults = DEFAULT_FORM_DEFAULTS
        # Créer un nouveau Formulaire avec les paramètres par défaut
        form = Form.objects.create(
            titleForm=form_defaults.get('titleForm'),
            introText=form_defaults.get('introText'),
            concludingText=form_defaults.get('concludingText'),
            Customer=self.Customer
        )
        print("Formulaire créé avec succès")
        # Créer une première page avec la question par défaut
        form.add_init_page()
        return form
    
    def add_init_page(self):
        # Créer une première page avec la question par défaut
        page = Page.objects.create(number=1, Form=self)
        print("page créé avec succès")
        page.add_init_question()
        return page
    
    def delete_form(self):
        form_to_delete = Form.objects.filter(idForm=self.idForm)
        if form_to_delete.exists():
            form_to_delete.delete()
            return True
        else:
            return False


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
        title = question_defaults.get('title')
        is_obligatory = question_defaults.get('isObligatory')
        nbr_answer_min = question_defaults.get('nbrAnswerMin')
        nbr_answer_max = question_defaults.get('nbrAnswerMax')
        print("question créé avec succès")
        # Créer la nouvelle question avec l'ordre spécifié
        question = Question.objects.create(
            title=title,
            type=question_type,
            page=self,
            isObligatory=is_obligatory,
            nbrAnswerMin=nbr_answer_min,
            nbrAnswerMax=nbr_answer_max,
            order=0
        )
        print("question créé avec succès")
        # Ajouter des réponses par défaut à la nouvelle question
        response_defaults = DEFAULT_RESPONSE_DEFAULTS.get(DEFAULT_QUESTION_TYPE, {})
        print("1")
        responses = response_defaults.get('responses', [])
        print("2")
        for response in responses:
            question.add_default_answer(response)
        print("réponses créé avec succès")
        return question


    def supprimer_page(self):
        page_number = self.Form.page_set.count()
        #vérifier si c'est lapage du formulaire 
        if page_number == 1:
            raise ValueError("Impossible de supprimer la dernière question de la page.")
        else :
            # Supprimer la page
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
    dependency_formul = models.TextField(blank=True, null=True) #Q1R1 ET Q1R2, id Q1R1 ET id->Q1R2
                                                                

    def __str__(self):
        return self.title

    def add_question(self):
        print("Ajout d'une question en cours...")
        # Vérifier si le nombre maximal de questions est atteint
        if self.page.question_set.count() >= NUMBER_MAX_QUESTION:
            raise ValueError("Le nombre maximal de questions pour ce formulaire a été atteint.")
        
        # Récupérer le type de question par défaut depuis DEFAULT_QUESTION_TYPE
        question_type = Type.objects.get(typeQuestion=DEFAULT_QUESTION_TYPE)
        
        # Récupérer les paramètres de question par défaut
        question_defaults = DEFAULT_QUESTION_DEFAULTS.get(DEFAULT_QUESTION_TYPE)
        title = question_defaults.get('title')
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
            title=title,
            isObligatory=is_obligatory,
            nbrAnswerMin=nbr_answer_min,
            nbrAnswerMax=nbr_answer_max,
            order=new_question_order
        )

        # Ajouter des réponses par défaut à la nouvelle question
        response_defaults = DEFAULT_RESPONSE_DEFAULTS.get(DEFAULT_QUESTION_TYPE, {})
        responses = response_defaults.get('responses', [])
        print (responses)
        for response in responses:
            question.add_default_answer(response)

        return question

    def add_answer(self):
        text = "Réponse " + str(self.answer_set.count() + 1)
        self.add_default_answer(text)
    
    def add_default_answer(self, text):
        new_answer = Answer.objects.create(
            type=self.type,
            Question=self,
            Answer=text
        )
        return new_answer

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
        myQuestions = Question.objects.filter(page=self.page)
        if direction == 'haut':
            if self.order == 0:
                print("La question est déjà en haut.")
            else:
                # Obtenir la question précédente avec un ordre inférieur dans myQuestions
                other_question = myQuestions.get(order=self.order - 1)
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
                other_question = myQuestions.get(order=self.order + 1)
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
        if self.type.typeQuestion == questionType.typeQuestion:
            print("Le type de question est déjà le même.")
            return
        print("here")
        print(self.type.typeQuestion)
        print(questionType.typeQuestion)
        # Vérifier si l'ancien type ou nouveau est ouvert ou à échelle
        old_type_is_open_likert = self.type.typeQuestion in ['question ouverte', 'Question à échelle']
        new_type_is_open_likert = questionType.typeQuestion in ['question ouverte', 'Question à échelle']
        print("swap")
        print(old_type_is_open_likert)
        print(new_type_is_open_likert)
    

        if self.type == 'question ouverte' or self.type =='Question à échelle' and question_type=='question ouverte' or question_type=='Question à échelle':
            print("here")
            # Supprimer les réponses existantes
            self.answer_set.all().delete()

            # Initialiser les paramètres par défaut du nouveau type
            question_defaults = DEFAULT_QUESTION_DEFAULTS.get(questionType.typeQuestion)
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
        print("Suppression de la réponse en ...")
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
        print("La question est maintenant",  self.isObligatory)

class Answer(models.Model):
    idAnswer   = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    type       = models.ForeignKey(Type    , on_delete=models.CASCADE)
    Question   = models.ForeignKey(Question, on_delete=models.CASCADE)
    Answer     = models.TextField(max_length=100)

    def __str__(self):
        return str(self.idAnswer)
    
    def delete_answer(self):
        print("Suppression de la réponse en cours...")
        self.delete()


class User(models.Model):
    idUSer       = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    mailUser     = models.TextField(max_length=100)
    loginUser    = models.CharField(max_length=100)
    passwordUser = models.TextField(max_length=100)
    replayDate   = models.DateTimeField(auto_now_add=True) # date de la création de l'objet et donc de réponse au Form

    def __str__(self):
        return self.loginUser

class Participant(models.Model):
    idParticipant       = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    loginParticipant    = models.CharField(max_length=100)
    replayDate   = models.DateTimeField(auto_now_add=True) # date de la création de l'objet et donc de réponse au 1er formulaire

    def __str__(self):
        return self.loginParticipant
    
    #créer un Participant
    def create_participant(self, loginParticipant):
        Participant.objects.create(
            loginParticipant=loginParticipant
        )

class ParticipantAnswer(models.Model):
    idParticipantAnswer = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    Participant         = models.ForeignKey(Participant    , on_delete=models.CASCADE)
    Form                = models.ForeignKey(Form           , on_delete=models.CASCADE)
    question     = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer       = models.ForeignKey(Answer  , on_delete=models.CASCADE)
    text         = models.TextField(max_length=100)

    def __str__(self):
        return self.answer.__str__()
    
    def create_participantAnswer(Participant, Form, question, answer, text):
        ParticipantAnswer.objects.create(
            Participant=Participant,
            Form=Form,
            question=question,
            answer=answer,
            text=text
        )

class QuestionDependency(models.Model):
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    dependent_question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='dependency')

    def __str__(self):
        return f"{self.answer} -> {self.dependent_question.idQuestion}"

    @classmethod
    def get_dependent_questions(cls, answer):
        """
        Renvoie la liste des questions dépendantes de la réponse donnée.
        """
        return cls.objects.filter(answer=answer).values_list('dependent_question', flat=True)

    @classmethod
    def get_dependent_answers(cls, question):
        """
        Renvoie la liste des réponses dépendantes de la question donnée.
        """
        return cls.objects.filter(dependent_question=question).values_list('answer', flat=True)

    @classmethod
    def add_dependency(cls, answer, dependent_question):
        cls.objects.create(answer=answer, dependent_question=dependent_question)

    @classmethod
    def remove_dependency(cls, answer, dependent_question):
        cls.objects.filter(answer=answer, dependent_question=dependent_question).delete()