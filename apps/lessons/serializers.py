from rest_framework import serializers
from .models import Lesson

class LessonSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.teacher.get_full_name', read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'teacher_name', 'is_public', 'content']
