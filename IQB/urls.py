"""
URL configuration for IQB project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
""" from django import views
from django.contrib import admin
from django.urls import path
import IQB.polls.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name='main'),
    path('Client/<int:id>', views.CreateForm(), name='client'),
    path('user', views.answerForm(), name='user'),
] """

from django.contrib import admin
from django.urls import include, path
from polls import views
import uuid

urlpatterns = [
    #path("polls/", include("polls.urls"t)),
    path("", views.login_view, name="home"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/',views.register_view, name='register'),
    path("admin/", admin.site.urls),
    
    #test et debug
    
    #path('form/', views.answerFormView, name='answerFormView'),
    #path('<str:loginCust>/createQuestion/<str:idForm>/', views.QuestionView, name='QuestionView'),
    
    path('<str:username>/form/<str:idForm>/', views.reponse, name='preview'),
    path('form/<str:idForm>/', views.reponse, name='reponse'),
    #path("Customer/<str:login>", views.CreateForm, login='login'),
    
    #test et debug
    #path('details/<str:loginCust>/', views.details, name='details'),        #http://127.0.0.1:8000/details/cust1/
    #Vu Client 
    path('<str:loginCust>/', views.details, name='details'),
    path('<str:loginCust>/form/', include([
        path('redirection', views.redirection, name='redirection'),
        path('CreateForm/', views.CreateForm, name='createForm'),
        path('createQuestion/<str:idForm>/', views.QuestionView, name='QuestionView'),
    ])),

]

"""
url :
""                                      --> si pas connecté direction login sinon vers login/details
login
register
<str:loginCust>
<str:loginCust>/createQuestion
<str:loginCust>/createQuestion/test     --> voir le formulaire en mode vue user pour test
form/idUSer                             --> user qui répond au form

admin
"""