from rest_framework import serializers
from .models import Quizz, Question, Choice


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'correct_answer', 'choices']
        extra_kwargs = {
            'correct_answer': {'write_only': True}  # Cache la réponse correcte dans l'affichage
        }


class QuizzSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)
    teacher_id = serializers.IntegerField(source='teacher.id', read_only=True)  
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quizz
        fields = ['id', 'title', 'subject', 'teacher_name', 'teacher_id', 'number_of_questions', 'questions']
