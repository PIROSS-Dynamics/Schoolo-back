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


from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.quizz.models import Quizz, Question, Choice
from apps.users.models import Teacher
from apps.quizz.serializers import QuizzSerializer

class QuizzViewsTestCase(APITestCase):

    def setUp(self):
        """Préparer les données de test"""
        self.teacher = Teacher.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="securepassword",
            role="teacher"
        )

        self.quizz = Quizz.objects.create(
            title="Test Quizz",
            subject="Maths",
            teacher=self.teacher,
            number_of_questions=2,
            is_public=True
        )

        self.question1 = Question.objects.create(
            quizz=self.quizz,
            text="What is 2 + 2?",
            question_type="text",
            correct_answer="4"
        )

        self.question2 = Question.objects.create(
            quizz=self.quizz,
            text="What is the capital of France?",
            question_type="text",
            correct_answer="Paris"
        )

        self.choice1 = Choice.objects.create(
            question=self.question2,
            text="Paris"
        )

    def test_get_public_quizzes(self):
        """Test pour récupérer tous les quizz publics"""
        url = reverse('quizz-list')  # Assure-toi que cette URL est définie dans `urls.py`
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.quizz.title)

    def test_get_quizz_detail(self):
        """Test pour récupérer le détail d’un quizz"""
        url = reverse('quizz-detail', args=[self.quizz.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.quizz.title)

    def test_create_quizz(self):
        """Test pour créer un nouveau quizz"""
        url = reverse('create_quizz')
        data = {
            "title": "New Quizz",
            "subject": "Science",
            "teacher": self.teacher.id,
            "is_public": True,
            "questions": [
                {
                    "text": "What is H2O?",
                    "question_type": "text",
                    "correct_answer": "Water",
                    "choices": []
                },
                {
                    "text": "Which planet is known as the Red Planet?",
                    "question_type": "choice",
                    "correct_answer": "Mars",
                    "choices": [
                        {"text": "Mars"},
                        {"text": "Venus"},
                        {"text": "Jupiter"}
                    ]
                }
            ]
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quizz.objects.count(), 2)

    def test_update_quizz(self):
        """Test pour mettre à jour un quizz"""
        url = reverse('quizz-detail', args=[self.quizz.id])
        data = {
            "title": "Updated Quizz",
            "subject": "Maths"  # Remplace "Physics" par un choix valide
        }
        response = self.client.put(url, data, format="json")

        print("Response status:", response.status_code)
        print("Response data:", response.data)  # Vérifie si d'autres erreurs persistent

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.quizz.refresh_from_db()
        self.assertEqual(self.quizz.title, "Updated Quizz")
        self.assertEqual(self.quizz.subject, "Maths")  # Vérifie la mise à jour



# def test_delete_quizz(self):
#     """Test pour supprimer un quizz"""
#     url = reverse('quizz-detail', args=[self.quizz.id])
#     response = self.client.delete(url)
#     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#     self.assertEqual(Quizz.objects.count(), 0)


    def test_get_teacher_quizzes(self):
        """Test pour récupérer les quizz d’un enseignant spécifique"""
        url = reverse('get-teacher-quizzes', args=[self.teacher.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.quizz.title)

from apps.quizz.forms import QuizzForm, QuestionForm, ChoiceForm

class QuizzFormsTestCase(TestCase):

    def setUp(self):
        """Préparer les données de test"""
        self.teacher = Teacher.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="securepassword",
            role="teacher"
        )

    def test_valid_quizz_form(self):
        """Test qu'un formulaire de quiz valide est bien accepté"""
        form_data = {
            "title": "Science Quiz",
            "subject": "Maths",  # Doit être une valeur valide de SUBJECT_CHOICES
            "teacher": self.teacher.id,
            "number_of_questions": 5,
            "is_public": True
        }
        form = QuizzForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_quizz_form(self):
        """Test qu'un formulaire de quiz invalide est rejeté"""
        form_data = {
            "title": "",  # Titre vide (invalide)
            "subject": "Informatique",  # Sujet non valide
            "teacher": self.teacher.id,
            "number_of_questions": -1,  # Nombre négatif (invalide)
            "is_public": True
        }
        form = QuizzForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)
        self.assertIn("subject", form.errors)
        self.assertIn("number_of_questions", form.errors)

    def test_valid_question_form(self):
        """Test qu'un formulaire de question valide est bien accepté"""
        form_data = {
            "text": "What is 2 + 2?",
            "question_type": "text",
            "correct_answer": "4"
        }
        form = QuestionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_question_form(self):
        """Test qu'un formulaire de question invalide est rejeté"""
        form_data = {
            "text": "",  # Texte vide (invalide)
            "question_type": "text",
            "correct_answer": ""
        }
        form = QuestionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("text", form.errors)

    def test_valid_choice_form(self):
        """Test qu'un formulaire de choix valide est bien accepté"""
        form_data = {"text": "Paris"}
        form = ChoiceForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_choice_form(self):
        """Test qu'un formulaire de choix invalide est rejeté"""
        form_data = {"text": ""}  # Texte vide (invalide)
        form = ChoiceForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("text", form.errors)
