from django.urls import path
from . import views
from .views import RegisterView, LoginView

urlpatterns = [
    path('api/teachers/', views.list_teachers, name='list-teachers'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
]