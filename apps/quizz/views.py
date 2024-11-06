
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


class QuizzDetailView(APIView):
    def get(self, request, quizz_id):
        quizz = get_object_or_404(Quizz, id=quizz_id, is_public=True)
        serializer = QuizzSerializer(quizz)
        return Response(serializer.data)

    def post(self, request, quizz_id):
        quizz = get_object_or_404(Quizz, id=quizz_id)
        score = 0
        total_questions = quizz.questions.count()

        # Évaluer chaque question
        for question in quizz.questions.all():
            user_answer = request.data.get(str(question.id))  # Obtient la réponse de l'utilisateur pour cette question

            if question.question_type == 'choice':
                # Récupère le texte du choix sélectionné par l'utilisateur
                selected_choice = get_object_or_404(Choice, id=user_answer)
                if selected_choice.text == question.correct_answer:
                    score += 1
            else:
                # Vérifie la réponse écrite
                if user_answer and user_answer.strip().lower() == question.correct_answer.strip().lower():
                    score += 1

        # Calculer et retourner le score
        return Response({
            "score": score,
            "total": total_questions,
            "result": f"Vous avez {score} bonnes réponses sur {total_questions}."
        }, status=status.HTTP_200_OK)


class CreateQuizzView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        
        # On commence une transaction pour garantir l'intégrité des données en cas d'échec
        with transaction.atomic():
            # Récupérer les informations de base du quiz
            title = data.get('title')
            subject = data.get('subject')
            teacher_id = data.get('teacher')
            is_public = data.get('is_public', False)
            questions_data = data.get('questions', [])
            
            # Créer le quiz
            quiz = Quizz.objects.create(
                title=title,
                subject=subject,
                teacher_id=teacher_id,
                is_public=is_public,
                number_of_questions=len(questions_data)
            )

            # Créer chaque question et ses choix (le cas échéant)
            for question_data in questions_data:
                question_text = question_data.get('text')
                question_type = question_data.get('question_type')
                correct_answer = question_data.get('correct_answer', '')
                
                question = Question.objects.create(
                    quizz=quiz,
                    text=question_text,
                    question_type=question_type,
                    correct_answer=correct_answer
                )
                
                # Créer les choix pour les questions de type "choice"
                if question_type == 'choice':
                    choices_data = question_data.get('choices', [])
                    for choice in choices_data:
                        choice_text = choice['text'] if isinstance(choice, dict) else choice
                        Choice.objects.create(
                            question=question,
                            text=choice_text
                        )

        # Sérialiser le quiz créé pour retour de confirmation
        serializer = QuizzSerializer(quiz)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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

