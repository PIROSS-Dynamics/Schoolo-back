
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Quizz, Question, Choice
from .forms import QuizzForm, QuestionForm, ChoiceForm
from django.forms import formset_factory
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuizzSerializer

#### GESTION FRONT ####

class QuizzListView(APIView):
    def get(self, request):
        quizz = Quizz.objects.filter(is_public=True)  # Filtre pour les quizz publics uniquement
        serializer = QuizzSerializer(quizz, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#### GESTION BACK ####

def quizz_list(request):
    quizzs = Quizz.objects.filter(is_public=True)
    return render(request, 'quizz/quizz_list.html', {'quizzs': quizzs})

def quizz_detail(request, quizz_id):
    quizz = get_object_or_404(Quizz, id=quizz_id)
    return render(request, 'quizz/quizz_detail.html', {'quizz': quizz})


def quizz_detail(request, quizz_id):
    quizz = get_object_or_404(Quizz, id=quizz_id)

    if request.method == 'POST':
        score = 0
        total_questions = quizz.questions.count()

        for question in quizz.questions.all():
            user_answer = request.POST.get(f'question_{question.id}')

            if question.question_type == 'choice':
                # Vérifie si la réponse choisie est correcte
                if user_answer:
                    choice = get_object_or_404(Choice, id=user_answer)
                    if choice.is_correct:
                        score += 1
            else:
                # Pour les questions à réponse écrite, vérifiez si la réponse est correcte
                if user_answer.strip().lower() == question.correct_answer.strip().lower():
                    score += 1

        return render(request, 'quizz/result.html', {'score': score, 'total': total_questions})

    return render(request, 'quizz/quizz_detail.html', {'quizz': quizz})

def add_quizz(request):
    if request.method == 'POST':
        quizz_form = QuizzForm(request.POST)
        if quizz_form.is_valid():
            quizz = quizz_form.save()
            
            # Parcourir les questions
            for key in request.POST:
                if key.startswith('question_') and '_text' in key:
                    question_index = key.split('_')[1]
                    question_text = request.POST.get(f'question_{question_index}_text')
                    question_type = request.POST.get(f'question_{question_index}_type')

                    # Créer l'objet Question
                    question = Question.objects.create(
                        quizz=quizz,
                        text=question_text,
                        question_type=question_type
                    )

                    # Si c'est une question à réponse écrite
                    if question_type == 'text':
                        question.correct_answer = request.POST.get(f'question_{question_index}_correct_answer')
                        question.save()

                    # Si c'est une question à choix multiple
                    elif question_type == 'choice':
                        choices = [v for k, v in request.POST.items() if k.startswith(f'choices_{question_index}_')]
                        correct_choice_key = request.POST.get(f'correct_choice_{question_index}')

                        # Créer les choix
                        for i, choice_text in enumerate(choices):
                            choice_key = f'choices_{question_index}_{i+1}'
                            is_correct = (choice_key == correct_choice_key)

                            # Création du choix avec le bon état de `is_correct`
                            choice = Choice.objects.create(
                                question=question,
                                text=choice_text,
                                is_correct=is_correct
                            )

                            # Si le choix est correct, on met à jour `correct_answer`
                            if is_correct:
                                question.correct_answer = choice.text
                                question.save()  # Sauvegarde pour `correct_answer`
            
            return redirect('quizz_list')

    else:
        quizz_form = QuizzForm()
    
    return render(request, 'quizz/add_quizz.html', {'quizz_form': quizz_form})

