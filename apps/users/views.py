from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User, Student, Teacher, Parent
from .serializers import TeacherSerializer, StudentSerializer, ParentSerializer
from rest_framework.decorators import api_view
import jwt # for token
from datetime import datetime, timedelta
from django.conf import settings
# from django.contrib.auth.hashers import check_password, make_password



class RegisterView(APIView):
    def post(self, request):

        data = request.data
        role = data.get('role', 'student')
        
        if User.objects.filter(email=data['email']).exists():
            return Response({'error': 'Un utilisateur existe déjà avec cet email'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a user in dependance of the role choosed
        try:
            if role == 'student':   
                user = Student.objects.create(
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    password=data['password'],  
                    experience_level=0,
                    role=role
                )
            elif role == 'teacher':
                user = Teacher.objects.create(
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    password=data['password'],
                    role=role
                )
            elif role == 'parent':
                user = Parent.objects.create(
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    password=data['password'],
                    role=role
                )
            else:
                return Response({'error': 'Ce rôle est invalide'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'Utilisateur crée avec succès'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)

            if (password == user.password):
                # Generate a token
                token = jwt.encode(
                    {
                        'id': user.id,
                        'email': user.email,
                        'exp': datetime.utcnow() + timedelta(hours=24)
                    },
                    settings.SECRET_KEY,
                    algorithm='HS256'
                )

                return Response({
                    'access': token,
                    'first_name': user.first_name,
                    'role': user.role,
                    'id': user.id
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Le mot de passe ne correspond pas'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'error': "Il n'y a aucun utilisateur existant avec cet email"}, status=status.HTTP_404_NOT_FOUND)




@api_view(['GET'])
def list_teachers(request):
    teachers = Teacher.objects.all()
    serializer = TeacherSerializer(teachers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_teacher(request, id):
    try:
        teacher = Teacher.objects.get(id=id)
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)
    except Teacher.DoesNotExist:
        return Response({'error': 'Teacher not found'}, status=404)
    
    
@api_view(['GET'])
def get_parent(request, id):
    try:
        parent = Parent.objects.get(id=id)
        serializer = ParentSerializer(parent)
        return Response(serializer.data)
    except Parent.DoesNotExist:
        return Response({'error': 'Parent not found'}, status=404)
    
    
@api_view(['GET'])
def get_student(request, id):
    try:
        student = Student.objects.get(id=id)
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=404)

