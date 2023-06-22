from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import Customer

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
    #nbrAnswerMin = forms.IntegerField()
    #nbrAnswerMax = forms.IntegerField()

class nbrAnswer(forms.Form):
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
    username = forms.CharField(label="Nom d'utilisateur")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': True, 'placeholder': "Nom d'utilisateur"})


class CustomerCreationForm(UserCreationForm):
    mailCust = forms.EmailField(label="Adresse e-mail")
    loginCust = forms.CharField(label="Nom d'utilisateur")

    class Meta(UserCreationForm.Meta):
        model = Customer
        fields = ('mailCust', 'loginCust', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['mailCust']
        user.loginCust = self.cleaned_data['loginCust']

        if commit:
            user.save()
        return user






############################################
#              Formulaire user             #
############################################

#class UtilisateurForm(forms.ModelForm):
#    class Meta:
#        model = Form, 
#        fields = ['nom', 'email']


"""""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer

class CustomerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Customer
        fields = ('username', 'email')


from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Customer

class CustomerAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Customer
        fields = '__all__'

"""