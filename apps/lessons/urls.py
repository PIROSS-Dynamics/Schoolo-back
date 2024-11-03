
from django.urls import path
from . import views

urlpatterns = [
    
    ## GESTION FRONT ##
    path('api/lessonslist/', views.LessonListView.as_view(), name='lesson-list'),
    path('api/lessonslist/<int:lesson_id>/', views.LessonDetailView.as_view(), name='lesson-detail'), 
    
    ## GESTION BACK ##
    path('', views.subjects_list, name='subjects_list'), # Liste des sujets sur l'entrée dans l'app
    path('list', views.lessons_list, name='lessons_list'),  # Liste des leçons
    path('<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),  # Détail d'une leçon
    path('add/', views.add_lesson, name='add_lesson'), # ajout d'une leçon
    path('lessons/modify/<int:lesson_id>/', views.modify_lesson, name='modify_lesson'), #modifier une lecon
]
