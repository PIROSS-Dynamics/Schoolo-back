from django.test import TestCase
from apps.lessons.models import Lesson
from apps.users.models import Teacher
from django.core.exceptions import ValidationError


class LessonModelTest(TestCase):
    def setUp(self):
        """Préparation des données pour les tests."""
        self.teacher = Teacher.objects.create(
            username="teacher1",
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
        )

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
        self.lesson.save()
        self.assertEqual(self.lesson.subject, "Français")




    def test_invalid_subject(self):
        """Test qu'une valeur invalide pour `subject` lève une erreur."""
        self.lesson.subject = "Informatique"
        with self.assertRaises(ValidationError) as context:
            self.lesson.full_clean()

        self.assertIn("n’est pas un choix valide", str(context.exception))


    def test_blank_and_null_description(self):
        """Test que la description peut être vide ou nulle."""
        lesson_without_description = Lesson.objects.create(
            title="Cours sans description",
            subject="Anglais",
            teacher=self.teacher,
            content="Ceci est un cours sans description.",
            is_public=False,
        )
        self.assertIsNone(lesson_without_description.description)

    def test_title_max_length(self):
        """Test que le champ `title` ne dépasse pas la longueur maximale."""
        self.lesson.title = "A" * 256  # Dépasse la limite de 255 caractères
        with self.assertRaises(ValidationError):
            self.lesson.full_clean()

    def test_subject_max_length(self):
        """Test que le champ `subject` ne dépasse pas la longueur maximale."""
        self.lesson.subject = "A" * 51  # Dépasse la limite de 50 caractères
        with self.assertRaises(ValidationError):
            self.lesson.full_clean()

    def test_lesson_teacher_relation(self):
        """Test que la leçon est correctement associée à un enseignant."""
        self.assertEqual(self.lesson.teacher.username, "teacher1")

    def test_teacher_deletion_cascades(self):
        """Test que la suppression d'un enseignant supprime ses leçons."""
        self.teacher.delete()
        with self.assertRaises(Lesson.DoesNotExist):
            Lesson.objects.get(pk=self.lesson.pk)

    def test_is_public_default(self):
        """Test que le champ `is_public` est vrai par défaut."""
        lesson = Lesson.objects.create(
            title="Cours par défaut",
            subject="Anglais",
            teacher=self.teacher,
            content="Contenu par défaut",
        )
        self.assertTrue(lesson.is_public)

    def test_toggle_is_public(self):
        """Test que le champ `is_public` peut être modifié."""
        self.lesson.is_public = False
        self.lesson.save()
        self.assertFalse(self.lesson.is_public)