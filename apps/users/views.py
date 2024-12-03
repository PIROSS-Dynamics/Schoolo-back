from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status, viewsets
from django.utils import timezone
from datetime import timedelta
from .models import User, Student, Teacher, Parent, Task
from .serializers import (
    UserSerializer, StudentSerializer, TeacherSerializer,
    ParentSerializer, TaskSerializer, SignUpSerializer, LoginSerializer
)
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import localdate
from rest_framework.exceptions import ValidationError
from .serializers import StudentSerializer, TaskSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

@api_view(['GET'])
def student_info(request, student_id):
    """Retrieve student info and tasks."""
    student = get_object_or_404(Student, id=student_id)
    tasks = student.tasks.all()
    student_data = StudentSerializer(student).data
    tasks_data = TaskSerializer(tasks, many=True).data
    return Response({
        "student": student_data,
        "tasks": tasks_data,
    })


@api_view(['PUT'])
def update_student_profile(request, student_id):
    """Update student info."""
    student = get_object_or_404(Student, id=student_id)
    serializer = StudentSerializer(student, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Profile updated successfully! Well done 🎉",
            "redirect_url": f"/student/{student.id}/"
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
def update_task(request, task_id):
    """Update task info."""
    task = get_object_or_404(Task, id=task_id)
    serializer = TaskSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Tache a été mis à jour.",
            "redirect_url": f"/student/{task.student.id}/"
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Require authentication for logout
def logout(request):
    """
    Log the user out by deleting their token and clearing their session.
    """
    Token.objects.filter(user=request.user).delete()  # Delete the user's token
    request.session.flush()  # Optionally clear the session
    return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)


from django.http import Http404

@api_view(['GET'])
def get_user_profile(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        
        # Determine role-specific data
        if hasattr(user, 'student'):
            profile_data = {
                "experience_level": user.student.experience_level,  # Specific to Student
                "tasks": TaskSerializer(user.student.tasks.all(), many=True).data
            }
        elif hasattr(user, 'teacher'):
            profile_data = {
                "subject": user.teacher.subject,  # Example field for Teacher
            }
        elif hasattr(user, 'parent'):
            profile_data = {
                "children_count": user.parent.children.count(),  # Example field for Parent
            }
        else:
            profile_data = {}  # Default if no specific role data

        # General user data
        return Response({
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "profile": profile_data,
        })

    except User.DoesNotExist:
        raise Http404("User not found")
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    
    



def profile_info(request, id):
    user = get_object_or_404(User, id=id)
    data = {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role": user.role,
        "photo": user.photo.url if user.photo else None,
    }
    return JsonResponse(data)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])  # Allow anyone to sign up
def sign_up(request):
    """
    Sign up a new user and return a token upon successful registration.
    """
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "message": "User created successfully.",
            "user": UserSerializer(user).data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])  # Allow anyone to log in
def login(request):
    """
    Login a user by validating credentials and returning a token.
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "message": "Login successful.",
            "user": UserSerializer(user).data,
            "token": token.key
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Require authentication
def task_list(request, user_id):
    """
    List tasks for a specific user within a given week.
    """
    week_start_str = request.query_params.get('week_start')
    week_start = timezone.localdate() if not week_start_str else timezone.datetime.fromisoformat(week_start_str).date()
    week_end = week_start + timedelta(days=6)

    tasks = Task.objects.filter(
        student__id=user_id,
        realization_date__gte=week_start,
        realization_date__lte=week_end
    ).order_by('realization_date')

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])  # Allow anyone to list teachers
def list_teachers(request):
    """
    List all teachers in the database.
    """
    teachers = Teacher.objects.all()
    serializer = TeacherSerializer(teachers, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Require authentication
def calendar_view(request, user_id):
    """
    View a user's calendar with tasks in a specific week.
    """
    week_start_str = request.GET.get('week_start')
    week_start = timezone.localdate() if not week_start_str else timezone.datetime.fromisoformat(week_start_str).date()
    week_end = week_start + timedelta(days=6)

    tasks = Task.objects.filter(
        student_id=user_id,
        realization_date__gte=week_start,
        realization_date__lte=week_end
    ).order_by('realization_date', 'start_hour')

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Require authentication
def student_tasks(request, student_id):
    """
    Retrieve all tasks for a specific student.
    """
    tasks = Task.objects.filter(student_id=student_id).order_by('realization_date', 'start_hour')
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


# ViewSets for CRUD operations
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]


class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [IsAuthenticated]


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Task.objects.filter(student_id=user_id)
        return Task.objects.all()
