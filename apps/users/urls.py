from django.urls import path
from . import views

urlpatterns = [
    path('api/teachers/', views.list_teachers, name='list-teachers'),
    path('api/register/', views.RegisterView.as_view(), name='register'),
    path('api/login/', views.LoginView.as_view(), name='login'),
    path('api/teacher/<int:id>/', views.get_teacher, name='get-teacher'),
    path('api/student/<int:id>/', views.get_student, name='get-student'),
    path('api/parent/<int:id>/', views.get_parent, name='get-parent'),
]

    