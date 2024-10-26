
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Quizz, Question, Choice

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
