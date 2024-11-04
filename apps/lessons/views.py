from django.shortcuts import render, redirect, get_object_or_404
from .models import Lesson
from .forms import LessonForm
from apps.users.models import Teacher
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Lesson
from .serializers import LessonSerializer

#### GESTION FRONT ####

class LessonListView(APIView):
    def get(self, request, subject=None):
        if subject:
            # Vérifie que le sujet est valide
            if subject.capitalize() in dict(Lesson.SUBJECT_CHOICES).keys():
                lessons = Lesson.objects.filter(is_public=True, subject=subject.capitalize())
            else:
                return Response({"error": "Sujet non valide"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            lessons = Lesson.objects.filter(is_public=True)
        
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LessonDetailView(APIView):
    def get(self, request, lesson_id):
        try:
            lesson = Lesson.objects.get(id=lesson_id)
            serializer = LessonSerializer(lesson)  
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Lesson.DoesNotExist:
            return Response({'error': 'Leçon non trouvée.'}, status=status.HTTP_404_NOT_FOUND)

#### GESTION BACK ####

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

def modify_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('lesson_detail', lesson_id=lesson.id)  # Rediriger vers la page de détail de la leçon
    else:
        form = LessonForm(instance=lesson)

    return render(request, 'lessons/modify_lesson.html', {'form': form, 'lesson': lesson})