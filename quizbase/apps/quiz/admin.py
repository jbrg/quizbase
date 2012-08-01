from django.contrib import admin
from quizbase.apps.quiz.models import *

admin.site.register(Collection)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(CorrectAnswer)
