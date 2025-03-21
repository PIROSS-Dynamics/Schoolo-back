from django.shortcuts import render, redirect, get_object_or_404
from .forms import LessonForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Lesson, Teacher
from .serializers import LessonSerializer
from rest_framework.decorators import api_view

#to read the pdf
from rest_framework.parsers import MultiPartParser
from PyPDF2 import PdfReader

#### GESTION FRONT ####

class LessonListView(APIView):
    def get(self, request, subject=None):
        if subject:
            # if subject is valid
            if subject.capitalize() in dict(Lesson.SUBJECT_CHOICES).keys():
                lessons = Lesson.objects.filter(is_public=True, subject=subject.capitalize())
            else:
                return Response({"error": "Sujet non valide"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            lessons = Lesson.objects.filter(is_public=True)
        
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LessonDetailView(APIView):

    # for showing lesson detail
    def get(self, request, lesson_id):
        try:
            lesson = Lesson.objects.get(id=lesson_id)
            serializer = LessonSerializer(lesson)  
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Lesson.DoesNotExist:
            return Response({'error': 'Leçon non trouvée.'}, status=status.HTTP_404_NOT_FOUND)     

    # for modifing lesson detail
    def put(self, request, lesson_id):
        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            return Response({'error': 'Leçon non trouvée.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = LessonSerializer(lesson, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, lesson_id):
        try:
            lesson = Lesson.objects.get(id=lesson_id)

            lesson.delete()

            return Response({'message': 'Leçon supprimé avec succès.'}, status=status.HTTP_204_NO_CONTENT)

        except Lesson.DoesNotExist:
            return Response({'error': 'Leçon non trouvé.'}, status=status.HTTP_404_NOT_FOUND)  

class CreateLessonView(APIView):
    
    def post(self, request, *args, **kwargs):

        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExtractPdfTextView(APIView):
    parser_classes = [MultiPartParser]  # to manage muliplePart Files

    def post(self, request, *args, **kwargs):

        pdf_file = request.FILES.get("pdf")
        if pdf_file:
 
            try:

                # read the pdf and transform it to fill the content text zone
                reader = PdfReader(pdf_file)
                extracted_text = ""
                for page in reader.pages:
                    extracted_text += page.extract_text()

                    
                return Response({"content": extracted_text}, status=200)
            except Exception as e:
                return Response({"error": f"Erreur d'extraction : {str(e)}"}, status=400)
        return Response({"error": "Aucun fichier PDF fourni"}, status=400)

@api_view(['GET'])
def get_teacher_lessons(request, teacher_id):
    #Get lessons created by a specific teacher
    lessons = Lesson.objects.filter(teacher_id=teacher_id)
    serializer = LessonSerializer(lessons, many=True)  
    return Response(serializer.data)

class LikeLessonView(APIView):
    def post(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        lesson.likes += 1
        lesson.save()
        return Response({'likes': lesson.likes}, status=status.HTTP_200_OK)

#### GESTION BACK ####

def subjects_list(request):
    subjects = ["Maths", "Français", "Histoire", "Anglais", "Art"]
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