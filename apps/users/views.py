from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Teacher
from .serializers import TeacherSerializer  # Assurez-vous que ce serializer existe
from rest_framework.decorators import api_view

@api_view(['GET'])
def list_teachers(request):
    teachers = Teacher.objects.all()
    serializer = TeacherSerializer(teachers, many=True)
    return Response(serializer.data)

