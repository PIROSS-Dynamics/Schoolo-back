from django.test import TestCase
from apps.quizz.models import Quizz, Question, Choice
from apps.users.models import Teacher

class QuizzModelTestCase(TestCase):
    def setUp(self):
        """Préparer les données pour les tests."""
        self.teacher = Teacher.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            password="securepassword",
            role="teacher",
        )

        self.quizz = Quizz.objects.create(
            title="General Knowledge",
            subject="Maths",
            teacher=self.teacher,
            number_of_questions=10,
            is_public=True
        )

        self.question = Question.objects.create(
            quizz=self.quizz,
            text="What is 2 + 2?",
            question_type="text",
            correct_answer="4"
        )

        self.choice = Choice.objects.create(
            question=self.question,
            text="4"
        )

    def test_quizz_creation(self):
        """Test de la création d'un quiz."""
        self.assertEqual(self.quizz.title, "General Knowledge")
        self.assertEqual(self.quizz.subject, "Maths")
        self.assertEqual(self.quizz.teacher, self.teacher)
        self.assertEqual(self.quizz.number_of_questions, 10)
        self.assertTrue(self.quizz.is_public)

    def test_quizz_str_representation(self):
        """Test de la méthode __str__ de Quizz."""
        self.assertEqual(str(self.quizz), "General Knowledge")

    def test_question_creation(self):
        """Test de la création d'une question."""
        self.assertEqual(self.question.text, "What is 2 + 2?")
        self.assertEqual(self.question.question_type, "text")
        self.assertEqual(self.question.correct_answer, "4")
        self.assertEqual(self.question.quizz, self.quizz)

    def test_question_str_representation(self):
        """Test de la méthode __str__ de Question."""
        self.assertEqual(str(self.question), "What is 2 + 2?")

    def test_choice_creation(self):
        """Test de la création d'un choix."""
        self.assertEqual(self.choice.text, "4")
        self.assertEqual(self.choice.question, self.question)

    def test_choice_str_representation(self):
        """Test de la méthode __str__ de Choice."""
        self.assertEqual(str(self.choice), "4")

    def test_question_quizz_relationship(self):
        """Test de la relation entre Question et Quizz."""
        self.assertEqual(self.question.quizz.title, "General Knowledge")

    def test_choice_question_relationship(self):
        """Test de la relation entre Choice et Question."""
        self.assertEqual(self.choice.question.text, "What is 2 + 2?")
