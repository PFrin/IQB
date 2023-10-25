from django.contrib import admin

from .models import Type, Question, Customer, Form, Page, Answer,User, Participant, ParticipantAnswer, QuestionDependency

admin.site.register(Type)
admin.site.register(Customer)
admin.site.register(Form)
admin.site.register(Page)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(User)
admin.site.register(Participant)
admin.site.register(ParticipantAnswer)
admin.site.register(QuestionDependency)
