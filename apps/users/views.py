from django.shortcuts import render,redirect
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import RegisterUserForm
from .models import Teacher, CustomUser
from .serializers import TeacherSerializer  # Assurez-vous que ce serializer existe
from rest_framework.decorators import api_view
from django.contrib import messages #c'est pour envoyer un message de succès à la fin d'entregister un nouvel utilisateur


class RegisterUserView(View):
    def get(self,request,*args, **kwargs):
        form = RegisterUserForm()
        return render(request,"users/signup.html", {"form":form})
    
    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            CustomUser.objects.create_user(
                username= data["username"],
                email = data["email"],
                password = data["password"],
            )
            messages.success(request,"Incription effectuée avec succès.","succes") 
            return redirect("home")
        else:
            messages.error(request,"Erreur d'inscription.",'error')
            return redirect(request,"users/signup.html",{'form':form})
    

@api_view(['GET'])
def list_teachers(request):
    teachers = Teacher.objects.all()
    serializer = TeacherSerializer(teachers, many=True)
    return Response(serializer.data)

