# quizz/urls.py
from django.urls import path
from . import views

urlpatterns = [
    
    ## GESTION FRONT ##
    
    path('api/quizzlist/', views.QuizzListView.as_view(), name='quizz-list'),
    path('api/quizzlist/<int:quizz_id>/', views.QuizzDetailView.as_view(), name='quizz-detail'),
    path('api/quizzlist/add/', views.CreateQuizzView.as_view(), name='create_quizz'),
    path('api/teacher/<int:teacher_id>/quizzes/', views.get_teacher_quizzes, name='get-teacher-quizzes'),
    path('api/quizzlist/like/<int:quizz_id>/', views.LikeQuizzView.as_view(), name='like-quizz'),

    
    ## GESTION BACK ##
    
    path('', views.quizz_list, name='quizz_list'),
    path('<int:quizz_id>/', views.quizz_detail, name='quizz_detail'),
]
