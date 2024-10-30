from django.shortcuts import render, redirect, get_object_or_404
from .models import Lesson
from .forms import LessonForm
from apps.users.models import Teacher



def subjects_list(request):
    subjects = ["Maths", "Français", "Histoire", "Anglais"]
    return render(request, 'lessons/subjects_list.html', {'subjects': subjects})

def lessons_list(request):
    subject = request.GET.get('subject')  # Récupérer le sujet sélectionné dans la requête
    if subject:
        lessons = Lesson.objects.filter(subject=subject, is_public=True)  # Filtrer par sujet
    else:
        lessons = Lesson.objects.filter(is_public=True)  # Afficher toutes les leçons si aucun sujet n'est sélectionné
    return render(request, 'lessons/lessons_list.html', {'lessons': lessons, 'subject': subject})

def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    return render(request, 'lessons/lesson_detail.html', {'lesson': lesson})


def add_lesson(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lessons_list')  # Rediriger vers la liste des leçons après l'ajout
    else:
        form = LessonForm()
    
    teachers = Teacher.objects.all()  # Récupérer tous les enseignants
    return render(request, 'lessons/add_lesson.html', {'form': form, 'teachers': teachers})