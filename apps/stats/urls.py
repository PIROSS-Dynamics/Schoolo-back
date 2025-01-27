from django.urls import path
from . import views

urlpatterns = [
    path('api/quizzresults/<int:quizz_id>/', views.QuizzResultsView.as_view(), name='quizz_results'),
    path('api/userQuizResults/<int:user_id>/', views.UserQuizzResultsView.as_view(), name='user_quizz_results'),
]
