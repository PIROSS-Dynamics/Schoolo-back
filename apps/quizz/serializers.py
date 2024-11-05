from rest_framework import serializers
from .models import Quizz

class QuizzSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)
    
    class Meta:
        model = Quizz
        fields = ['id', 'title', 'subject', 'teacher_name', 'number_of_questions', 'is_public']
