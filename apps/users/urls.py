from django.urls import path
from . import views

urlpatterns = [
    path('api/teachers/', views.list_teachers, name='list-teachers'),
]