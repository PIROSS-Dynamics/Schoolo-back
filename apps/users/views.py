from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import RegisterUserForm
from .models import Teacher
from .serializers import TeacherSerializer  # Assurez-vous que ce serializer existe
from rest_framework.decorators import api_view


class RegisterUserView(View):
    def get(self,request,*args, **kwargs):
        form = RegisterUserForm()
        return render(request,"")
        
    

@api_view(['GET'])
def list_teachers(request):
    teachers = Teacher.objects.all()
    serializer = TeacherSerializer(teachers, many=True)
    return Response(serializer.data)

