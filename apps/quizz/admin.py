# quizz/admin.py
from django.contrib import admin
from .models import Quizz, Question, Choice

class quizzQuestion(admin.ModelAdmin):
    list_display = ('title', 'subject', 'number_of_questions', 'is_public')

admin.site.register(Quizz, quizzQuestion)


class questionAdmin(admin.ModelAdmin):
    list_display = ('quizz', 'question_type', 'correct_answer')  

admin.site.register(Question, questionAdmin)


class choiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct')  

admin.site.register(Choice, choiceAdmin)

