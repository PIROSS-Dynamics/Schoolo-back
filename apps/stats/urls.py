from django.urls import path
from . import views

urlpatterns = [
    path('api/quizzresults/<int:quizz_id>/', views.QuizzResultsView.as_view(), name='quizz_results'),
]
