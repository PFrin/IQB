from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm

############################################
#           Concepteur de Formulaire       #
############################################

class CreateForm(forms.Form):
    title            = forms.CharField()
    introText        = forms.CharField()
    concludingText   = forms.CharField()
    MEPDate          = forms.DateTimeField()
    isOnline         = forms.BooleanField ()

class CreateQuestion(forms.Form):
    title = forms.CharField()
    #type  = models.ForeignKey(Type, on_delete=models.CASCADE)
    #page  = models.ForeignKey(Page, on_delete=models.CASCADE)
    isObligatory = forms.BooleanField()
    nbrAnswerMin = forms.IntegerField()
    nbrAnswerMax = forms.IntegerField()


#class QuestionForm(forms.ModelForm):
#    class Meta:
#        model = Page,Question,Answer
#        fields = ['title', 'type','page','isObligatory','nbrAnswerMin','nbrAnswerMax']

#class ConclusionForm():
#    class Meta:
#        model = Form
#        fields = ['concludingText'] 
############################################
#   Formulaire d'inscription, connexion    #
############################################

class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField()

class CustomerCreationForm(forms.ModelForm):
    mailCust       = models.TextField(max_length=100)
    loginCust      = models.CharField(max_length=100)
    


############################################
#              Formulaire user             #
############################################

#class UtilisateurForm(forms.ModelForm):
#    class Meta:
#        model = Form, 
#        fields = ['nom', 'email']