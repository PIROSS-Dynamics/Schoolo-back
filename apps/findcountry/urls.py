from django.urls import path
from .views import GetRandomCountry

urlpatterns = [
    path('api/get_country/', GetRandomCountry.as_view(), name='get_country'),
]