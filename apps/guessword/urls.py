from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.get_word_data, name='guess_word'),  # Vue principale
    path('api/check_translation/', views.check_translation, name='check_translation'),  
]
