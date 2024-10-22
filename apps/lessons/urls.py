
from django.urls import path
from . import views

urlpatterns = [
    path('', views.subjects_list, name='subjects_list'), # Liste des sujets sur l'entrée dans l'app
    path('list', views.lessons_list, name='lessons_list'),  # Liste des leçons
    path('<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),  # Détail d'une leçon
]
