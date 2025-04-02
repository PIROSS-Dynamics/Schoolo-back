from django.urls import path
from . import views

urlpatterns = [
    path('api/quizzresults/<int:quizz_id>/', views.QuizzResultsView.as_view(), name='quizz_results'),
    path('api/userQuizResults/<int:user_id>/', views.UserQuizzResultsView.as_view(), name='user_quizz_results'),
    path('api/guesswordresult/', views.GuessWordResultView.as_view(), name='guess_word_result'),
    path('api/findcountryresult/', views.FindCountryResultView.as_view(), name='find_country_result'),
    path('api/userchallengeresults/', views.UserChallengeResultsView.as_view(), name='user_challenge_results'),
]
 