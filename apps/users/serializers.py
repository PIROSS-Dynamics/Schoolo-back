# serializers.py
from rest_framework import serializers
from .models import Teacher

from rest_framework import serializers
from .models import User, Parent, Student, Teacher

from rest_framework import serializers
from .models import User, Profile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(write_only=True)  # Pass role during registration

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'role']

    def create(self, validated_data):
        # Remove 'role' from validated data
        role = validated_data.pop('role')
        password = validated_data.pop('password')

        # Create a Profile instance for the user
        profile = Profile.objects.create(photo='', bio='')  # Empty defaults for profile fields

        # Create the user and link the profile
        user = User.objects.create(profile=profile, **validated_data)
        user.set_password(password)  # Hash the password
        user.save()

        # Assign the role-specific model
        if role == 'parent':
            Parent.objects.create(user_ptr=user)
        elif role == 'student':
            Student.objects.create(user_ptr=user)
        elif role == 'teacher':
            Teacher.objects.create(user_ptr=user)

        return user



class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name']  # Incluez tous les champs nécessaires
