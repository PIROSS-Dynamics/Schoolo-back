from django.test import TestCase
from apps.lessons.models import Lesson
from apps.users.models import Teacher
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase, Client
from apps.lessons.models import Lesson
from apps.users.models import Teacher

class LessonModelTest(TestCase):
    def setUp(self):
        """Préparation des données pour les tests."""
        # Création d'un profil pour le Teacher
        self.teacher = Teacher.objects.create(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        password="securepassword",
)


        # Création d'une leçon
        self.lesson = Lesson.objects.create(
            title="Introduction aux fractions",
            subject="Maths",
            teacher=self.teacher,
            content="Ceci est un cours sur les fractions.",
            is_public=True,
            description="Cours introductif pour les élèves de 6ème",
        )

    def test_lesson_creation(self):
        """Test de création d'une leçon."""
        self.assertEqual(self.lesson.title, "Introduction aux fractions")
        self.assertEqual(self.lesson.subject, "Maths")
        self.assertEqual(self.lesson.teacher, self.teacher)
        self.assertTrue(self.lesson.is_public)

    def test_str_representation(self):
        """Test de la représentation en chaîne de caractères."""
        self.assertEqual(str(self.lesson), "Introduction aux fractions")

    def test_subject_choices(self):
        """Test que le choix du sujet est valide."""
        self.lesson.subject = "Français"
        self.lesson.full_clean()  # Valide les choix du modèle
        self.assertEqual(self.lesson.subject, "Français")

    def test_invalid_subject(self):
        """Test qu'une valeur invalide pour `subject` lève une erreur."""
        self.lesson.subject = "Informatique"  # Non présent dans SUBJECT_CHOICES
        with self.assertRaises(ValidationError):
            self.lesson.full_clean()  # Déclenche la validation

    def test_blank_description(self):
        """Test que la description peut être vide."""
        lesson_without_description = Lesson.objects.create(
            title="Cours sans description",
            subject="Anglais",
            teacher=self.teacher,
            content="Contenu sans description.",
            is_public=False,
        )
        self.assertIsNone(lesson_without_description.description)

    def test_title_max_length(self):
        """Test que le champ `title` ne dépasse pas la longueur maximale."""
        self.lesson.title = "A" * 256  # 256 caractères
        with self.assertRaises(ValidationError):
            self.lesson.full_clean()

    def test_teacher_relationship(self):
        """Test de la relation entre une leçon et un enseignant."""
        self.assertEqual(self.lesson.teacher.email, "john.doe@example.com")

    def test_cascade_delete_teacher(self):
        """Test que la suppression d'un enseignant supprime ses leçons."""
        self.teacher.delete()
        with self.assertRaises(Lesson.DoesNotExist):
            Lesson.objects.get(pk=self.lesson.pk)

    def test_is_public_default(self):
        """Test que le champ `is_public` est vrai par défaut."""
        lesson = Lesson.objects.create(
            title="Cours par défaut",
            subject="Art",
            teacher=self.teacher,
            content="Contenu par défaut",
        )
        self.assertTrue(lesson.is_public)

    def test_toggle_is_public(self):
        """Test que le champ `is_public` peut être modifié."""
        self.lesson.is_public = False
        self.lesson.save()
        self.assertFalse(self.lesson.is_public)

class LessonListViewTestCase(APITestCase):
    def setUp(self):
        # Création d'un enseignant pour les relations
        self.teacher = Teacher.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="securepassword",
        )

        # Création de leçons pour les tests
        Lesson.objects.create(title="Leçon 1", subject="Maths", teacher=self.teacher, is_public=True, content="Contenu 1")
        Lesson.objects.create(title="Leçon 2", subject="Français", teacher=self.teacher, is_public=True, content="Contenu 2")
        Lesson.objects.create(title="Leçon 3", subject="Maths", teacher=self.teacher, is_public=False, content="Contenu 3")

    def test_list_all_public_lessons(self):
        """Test que les leçons publiques sont listées."""
        response = self.client.get('/api/lessonslist/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Deux leçons publiques

    def test_list_lessons_by_subject(self):
        """Test que les leçons peuvent être filtrées par sujet."""
        response = self.client.get('/api/lessonslist/subject/Maths/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['subject'], "Maths")

    def test_invalid_subject_returns_error(self):
        """Test qu'un sujet invalide retourne une erreur."""
        response = self.client.get('/api/lessonslist/subject/Informatique/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class LessonDetailViewTestCase(APITestCase):
    def setUp(self):
        self.teacher = Teacher.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            password="securepassword",
        )
        self.lesson = Lesson.objects.create(
            title="Détails de la leçon",
            subject="Histoire",
            teacher=self.teacher,
            is_public=True,
            content="Contenu pour le test de détail",
        )

    def test_lesson_detail_success(self):
        """Test que le détail d'une leçon existante est retourné."""
        response = self.client.get(f'/api/lessonslist/detail/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Détails de la leçon")

    def test_lesson_detail_not_found(self):
        """Test qu'une leçon introuvable retourne une 404."""
        response = self.client.get('/api/lessonslist/detail/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



class LessonCreateViewTestCase(APITestCase):
    def setUp(self):
        self.teacher = Teacher.objects.create(
            first_name="Alice",
            last_name="Johnson",
            email="alice.johnson@example.com",
            password="securepassword",
        )
        self.valid_payload = {
            "title": "Nouvelle leçon",
            "subject": "Art",
            "teacher": self.teacher.id,
            "content": "Contenu de la nouvelle leçon",
            "is_public": True,
        }
        self.invalid_payload = {
            "title": "",
            "subject": "Informatique",  # Sujet invalide
            "content": "",
        }

    def test_create_valid_lesson(self):
        """Test de création d'une nouvelle leçon valide."""
        response = self.client.post('/api/lessonslist/add', data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "Nouvelle leçon")

    def test_create_invalid_lesson(self):
        """Test que la création d'une leçon invalide échoue."""
        response = self.client.post('/api/lessonslist/add', data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('subject', response.data)
