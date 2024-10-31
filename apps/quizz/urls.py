# quizz/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.quizz_list, name='quizz_list'),
    path('<int:quizz_id>/', views.quizz_detail, name='quizz_detail'),
    path('add/', views.add_quizz, name='add_quizz'),
]
