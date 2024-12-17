from django.test import TestCase
from apps.quizz.models import Quizz, Question, Choice
from apps.users.models import Teacher, Student, Parent, User
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


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name="Test",
            last_name="User",
            email="test.user@example.com",
            password="securepassword",
            role="student",
        )

    def test_user_creation(self):
        """Test de la création d'un utilisateur simple."""
        self.assertEqual(self.user.first_name, "Test")
        self.assertEqual(self.user.last_name, "User")
        self.assertEqual(self.user.email, "test.user@example.com")
        self.assertEqual(self.user.role, "student")

    def test_user_str_representation(self):
        """Test de la méthode __str__ du modèle User."""
        self.assertEqual(str(self.user), "User: Test User (Email: test.user@example.com)")


class TeacherModelTestCase(TestCase):
    def setUp(self):
        self.teacher = Teacher.objects.create(
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@example.com",
            password="securepassword",
        )

    def test_teacher_creation(self):
        """Test de la création d'un professeur."""
        self.assertEqual(self.teacher.first_name, "Jane")
        self.assertEqual(self.teacher.last_name, "Doe")
        self.assertEqual(self.teacher.email, "jane.doe@example.com")
        self.assertEqual(self.teacher.role, "student")  # Inherit default role

    def test_teacher_str_representation(self):
        """Test de la méthode __str__ du modèle Teacher."""
        self.assertEqual(str(self.teacher), "Teacher: Jane Doe")

    def test_teacher_get_full_name(self):
        """Test de la méthode get_full_name."""
        self.assertEqual(self.teacher.get_full_name(), "Jane Doe")


class StudentModelTestCase(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            first_name="John",
            last_name="Smith",
            email="john.smith@example.com",
            password="securepassword",
            experience_level=5,
        )

    def test_student_creation(self):
        """Test de la création d'un étudiant."""
        self.assertEqual(self.student.first_name, "John")
        self.assertEqual(self.student.last_name, "Smith")
        self.assertEqual(self.student.experience_level, 5)

    def test_student_str_representation(self):
        """Test de la méthode __str__ du modèle Student."""
        self.assertEqual(str(self.student), "Student: John Smith - Level: 5")


class ParentModelTestCase(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            first_name="Tom",
            last_name="Brown",
            email="tom.brown@example.com",
            password="securepassword",
        )
        self.parent = Parent.objects.create(
            first_name="Anna",
            last_name="Brown",
            email="anna.brown@example.com",
            password="securepassword",
        )
        self.parent.children.add(self.student)

    def test_parent_creation(self):
        """Test de la création d'un parent et ajout d'enfant."""
        self.assertEqual(self.parent.first_name, "Anna")
        self.assertEqual(self.parent.children.count(), 1)
        self.assertEqual(self.parent.children.first(), self.student)

    def test_parent_str_representation(self):
        """Test de la méthode __str__ du modèle Parent."""
        self.assertEqual(str(self.parent), "Parent: Anna Brown - Children: Tom Brown")
