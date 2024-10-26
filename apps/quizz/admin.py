# quizz/admin.py
from django.contrib import admin
from .models import Quizz, Question, Choice

admin.site.register(Quizz)
admin.site.register(Question)
admin.site.register(Choice)
