from django.urls import path
from . import views
from .views import student_info, update_student_profile, update_task, get_user_profile

urlpatterns = [
    path('calendar/<int:user_id>/', views.calendar_view, name='calendar_view'),
    
    path('teachers/', views.list_teachers, name='list-teachers'),
    path('tasks/<int:user_id>/', views.task_list, name='task-list'),
    path('tasks/<int:user_id>/', views.task_list, name='task-list'),
    
    path('signup/', views.sign_up, name='signup'),  # Corrected path
    path('login/', views.login, name='login'),      # Ensure login also has /api/
    path('logout/', views.logout, name='logout'),
    
    path('users/', views.UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('students/', views.StudentViewSet.as_view({'get': 'list', 'post': 'create'}), name='student-list'),
    path('teachers/', views.TeacherViewSet.as_view({'get': 'list', 'post': 'create'}), name='teacher-list'),
    path('parents/', views.ParentViewSet.as_view({'get': 'list', 'post': 'create'}), name='parent-list'),
    path('tasks/', views.TaskViewSet.as_view({'get': 'list', 'post': 'create'}), name='task-list'),
    path('student/<int:student_id>/', student_info, name='student-info'),
    path('student/<int:student_id>/edit/', update_student_profile, name='update-student-profile'),
    path('task/<int:task_id>/edit/', update_task, name='update-task'),
    path('profile-info/', get_user_profile, name='profile-info'),
    path('profile-info/<int:id>/', views.profile_info, name='profile_info'),
]
