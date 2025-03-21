from rest_framework import serializers
from .models import Lesson

class LessonSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'title', 'teacher_name', 'teacher', 'is_public', 'content', 'description','grade']
        extra_kwargs = {
            'teacher': {'required': False}  # teacher field not requird for being able to not put it on update
        }

    def update(self, instance, validated_data):
        validated_data.pop('teacher', None)  # dont show teacher field on modity lesson
        return super().update(instance, validated_data)
