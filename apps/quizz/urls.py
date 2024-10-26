# quizz/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.quizz_list, name='quizz_list'),
    path('<int:quizz_id>/', views.quizz_detail, name='quizz_detail'),
]
