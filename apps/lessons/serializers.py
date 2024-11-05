from rest_framework import serializers
from .models import Lesson

class LessonSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.teacher.get_full_name', read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'title', 'teacher_name', 'teacher', 'is_public', 'content','description']
        extra_kwargs = {
            'teacher': {'required': True}  # S'assurer que le champ teacher est requis
        }

