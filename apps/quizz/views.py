
from django.shortcuts import render, get_object_or_404
from .models import Quizz, Question, Choice
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuizzSerializer, QuestionSerializer, ChoiceSerializer
from rest_framework.decorators import api_view

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
        corrections = []  # Nouvelle liste pour stocker les corrections

        # Évaluer chaque question
        for question in quizz.questions.all():
            user_answer = request.data.get(str(question.id))  # Obtient la réponse de l'utilisateur pour cette question
            is_correct = False  # Par défaut, la réponse est incorrecte

            if question.question_type == 'choice':
                # Récupère le choix sélectionné par l'utilisateur
                selected_choice = get_object_or_404(Choice, id=user_answer)
                if selected_choice.text == question.correct_answer:
                    score += 1
                    is_correct = True
                correct_answer = question.correct_answer  # Bonne réponse

            else:
                # Vérifie la réponse écrite
                if user_answer and user_answer.strip().lower() == question.correct_answer.strip().lower():
                    score += 1
                    is_correct = True
                correct_answer = question.correct_answer  # Bonne réponse

            # Ajout des détails de correction pour chaque question
            corrections.append({
                "question_text": question.text,
                "correct_answer": correct_answer,
                "is_correct": is_correct
            })

        # Calculer et retourner le score ainsi que les corrections
        return Response({
            "score": score,
            "total": total_questions,
            "result": f"Vous avez {score} bonnes réponses sur {total_questions}.",
            "corrections": corrections  # Ajout des corrections dans la réponse
        }, status=status.HTTP_200_OK)
        
    def put(self, request, quizz_id):
        quizz = Quizz.objects.get(id=quizz_id)
        
        # Sérialiseur pour le quiz
        quizz_serializer = QuizzSerializer(quizz, data=request.data, partial=True)
        
        if quizz_serializer.is_valid():
            quizz_serializer.save()

            # Mise à jour des questions et des choix
            for question_data in request.data.get('questions', []):
                question = Question.objects.get(id=question_data['id'], quizz=quizz)
                question_serializer = QuestionSerializer(question, data=question_data, partial=True)
                if question_serializer.is_valid():
                    question_serializer.save()

                    # Mise à jour des choix
                    for choice_data in question_data.get('choices', []):
                        choice = Choice.objects.get(id=choice_data['id'], question=question)
                        choice_serializer = ChoiceSerializer(choice, data=choice_data, partial=True)
                        if choice_serializer.is_valid():
                            choice_serializer.save()

            return Response({'message': 'Quiz mis à jour avec succès'}, status=status.HTTP_200_OK)
        else:
            return Response(quizz_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, quizz_id):
        
        try:
            quizz = Quizz.objects.get(id=quizz_id)

            quizz.delete()

            return Response({'message': 'Quiz supprimé avec succès.'}, status=status.HTTP_204_NO_CONTENT)

        except Quizz.DoesNotExist:
            return Response({'error': 'Quiz non trouvé.'}, status=status.HTTP_404_NOT_FOUND)    




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


@api_view(['GET'])
def get_teacher_quizzes(request, teacher_id):
    #Get Quizz created by a specific teacher
    quizzes = Quizz.objects.filter(teacher_id=teacher_id)
    serializer = QuizzSerializer(quizzes, many=True)  
    return Response(serializer.data)

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

