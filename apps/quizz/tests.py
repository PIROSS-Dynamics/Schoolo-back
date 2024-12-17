from django.test import TestCase
from apps.quizz.models import Quizz, Question, Choice
from apps.users.models import Teacher
from django.core.exceptions import ValidationError

class QuizzModelTestCase(TestCase):
    def setUp(self):
        # Création d'un enseignant pour associer aux quiz
        self.teacher = Teacher.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="securepassword",
        )
        # Création d'un quiz
        self.quizz = Quizz.objects.create(
            title="Quiz de Mathématiques",
            subject="Maths",
            teacher=self.teacher,
            number_of_questions=10,
            is_public=True
        )

    def test_quizz_creation(self):
        """Test de la création d'un quiz."""
        self.assertEqual(self.quizz.title, "Quiz de Mathématiques")
        self.assertEqual(self.quizz.subject, "Maths")
        self.assertEqual(self.quizz.number_of_questions, 10)
        self.assertTrue(self.quizz.is_public)

    def test_quizz_str_representation(self):
        """Test de la méthode __str__ du quiz."""
        self.assertEqual(str(self.quizz), "Quiz de Mathématiques")

    def test_quizz_invalid_subject(self):
        """Test de validation pour un sujet invalide."""
        self.quizz.subject = "Informatique"  # Sujet invalide
        with self.assertRaises(ValidationError):
            self.quizz.full_clean()


class QuestionModelTestCase(TestCase):
    def setUp(self):
        # Enseignant et quiz associés
        self.teacher = Teacher.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            password="securepassword",
        )
        self.quizz = Quizz.objects.create(
            title="Quiz d'Histoire",
            subject="Histoire",
            teacher=self.teacher,
            number_of_questions=5,
            is_public=True
        )
        # Question associée
        self.question = Question.objects.create(
            quizz=self.quizz,
            text="Quelle est la date de la révolution française ?",
            question_type="text",
            correct_answer="1789"
        )

    def test_question_creation(self):
        """Test de la création d'une question."""
        self.assertEqual(self.question.text, "Quelle est la date de la révolution française ?")
        self.assertEqual(self.question.correct_answer, "1789")
        self.assertEqual(self.question.question_type, "text")
        self.assertEqual(self.question.quizz.title, "Quiz d'Histoire")

    def test_question_str_representation(self):
        """Test de la méthode __str__ de Question."""
        self.assertEqual(str(self.question), "Quelle est la date de la révolution française ?")


class ChoiceModelTestCase(TestCase):
    def setUp(self):
        # Enseignant et quiz associés
        self.teacher = Teacher.objects.create(
            first_name="Alice",
            last_name="Johnson",
            email="alice.johnson@example.com",
            password="securepassword",
        )
        self.quizz = Quizz.objects.create(
            title="Quiz d'Art",
            subject="Art",
            teacher=self.teacher,
            number_of_questions=3,
            is_public=False
        )
        self.question = Question.objects.create(
            quizz=self.quizz,
            text="Qui a peint La Joconde ?",
            question_type="choice",
            correct_answer="Leonard de Vinci"
        )
        # Création des choix
        self.choice1 = Choice.objects.create(question=self.question, text="Leonard de Vinci")
        self.choice2 = Choice.objects.create(question=self.question, text="Picasso")
        self.choice3 = Choice.objects.create(question=self.question, text="Van Gogh")

    def test_choice_creation(self):
        """Test de la création des choix pour une question."""
        self.assertEqual(self.choice1.text, "Leonard de Vinci")
        self.assertEqual(self.choice1.question.text, "Qui a peint La Joconde ?")
        self.assertEqual(self.choice2.text, "Picasso")
        self.assertEqual(self.choice3.text, "Van Gogh")

    def test_choice_str_representation(self):
        """Test de la méthode __str__ de Choice."""
        self.assertEqual(str(self.choice1), "Leonard de Vinci")
