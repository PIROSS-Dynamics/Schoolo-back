from django.urls import path
from .views import GetWordDataView

urlpatterns = [
    path('api/get_word/', GetWordDataView.as_view(), name='get_word_data'),
]
