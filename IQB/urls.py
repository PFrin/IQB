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

urlpatterns = [
    #path("polls/", include("polls.urls"t)),
    path("", views.home, name="home"),
    path('login', views.login, name='login'),
    path('register',views.register, name='register'),
    path("admin/", admin.site.urls),
    
    #test et debug
    path('createQuestion/', views.Question, name='Question'),
    
    

    #test et debug
    path('details/<str:loginCust>/', views.details, name='details'),        #http://127.0.0.1:8000/details/cust1/
    #Vu Client 
    path('<str:loginCust>/', views.details, name='details'), #http://127.0.0.1:8000/cust1/
    path('<str:loginCust>/', include([
        path('CreateForm/', views.CreateForm, name='createForm'),
        #path('answerForm/', views.AnswerForm, name='AnswerForm'),
    ])),
]