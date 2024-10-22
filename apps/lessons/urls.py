
from django.urls import path
from .views import lessons_list, lesson_detail

urlpatterns = [
    path('', lessons_list, name='lessons_list'),  # Point d'entrée vers la liste des leçons
    path('lesson/<int:lesson_id>/', lesson_detail, name='lesson_detail'),  # Détail d'une leçon
]
