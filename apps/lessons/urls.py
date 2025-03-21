
from django.urls import path
from . import views

urlpatterns = [
    
    ## GESTION FRONT ##
    
    path('api/lessonslist/', views.LessonListView.as_view(), name='lesson-list'),
    path('api/lessonslist/subject/<str:subject>/', views.LessonListView.as_view(), name='lessons-by-subject'),
    path('api/lessonslist/detail/<int:lesson_id>/', views.LessonDetailView.as_view(), name='lesson-detail'),
    path('api/lessonslist/add', views.CreateLessonView.as_view(), name='create-lesson'),
    path('api/lessonslist/extract-pdf', views.ExtractPdfTextView.as_view(), name='extract_pdf_text'),
    path('api/teacher/<int:teacher_id>/lessons/', views.get_teacher_lessons, name='get-teacher-lessons'),
    path('api/lessonslist/like/<int:lesson_id>/', views.LikeLessonView.as_view(), name='like-lesson'),

    ## GESTION BACK ##
    path('', views.subjects_list, name='subjects_list'), # Liste des sujets sur l'entrée dans l'app
    path('list', views.lessons_list, name='lessons_list'),  # Liste des leçons
    path('<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),  # Détail d'une leçon
    path('add/', views.add_lesson, name='add_lesson'), # ajout d'une leçon
    path('lessons/modify/<int:lesson_id>/', views.modify_lesson, name='modify_lesson'), #modifier une lecon

    

]
