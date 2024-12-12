# serializers.py
from rest_framework import serializers
from .models import Teacher,Student, Parent

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'email', 'role'] 
        
 
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'email', 'role'] 
        
        
class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ['id', 'first_name', 'last_name', 'email', 'role'] 