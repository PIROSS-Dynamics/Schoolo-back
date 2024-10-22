
from django.shortcuts import render, get_object_or_404
from .models import Lesson

def lessons_list(request):
    lessons = Lesson.objects.filter(is_public=True)
    return render(request, 'lessons/lessons_list.html', {'lessons': lessons})

def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    return render(request, 'lessons/lesson_detail.html', {'lesson': lesson})
