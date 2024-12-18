from django.test import TestCase
from apps.lessons.models import Lesson
from apps.users.models import Teacher
from django.utils.timezone import now


class LessonModelTestCase(TestCase):
    def setUp(self):
        """Préparer les données pour les tests."""
        # Créer un professeur pour associer aux leçons
        self.teacher = Teacher.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="securepassword",
            role="teacher",
        )

        # Créer une leçon associée au professeur
        self.lesson = Lesson.objects.create(
            title="Introduction to Maths",
            subject="Maths",
            teacher=self.teacher,
            content="This is the content of the maths lesson.",
            is_public=True,
            description="An introductory lesson to basic maths concepts."
        )

    def test_lesson_creation(self):
        """Test de la création d'une leçon."""
        self.assertEqual(self.lesson.title, "Introduction to Maths")
        self.assertEqual(self.lesson.subject, "Maths")
        self.assertEqual(self.lesson.teacher, self.teacher)
        self.assertTrue(self.lesson.is_public)
        self.assertEqual(self.lesson.description, "An introductory lesson to basic maths concepts.")

    def test_lesson_str_representation(self):
        """Test de la méthode __str__ de Lesson."""
        self.assertEqual(str(self.lesson), "Introduction to Maths")

    def test_lesson_teacher_relationship(self):
        """Test de la relation entre Lesson et Teacher."""
        self.assertEqual(self.lesson.teacher.first_name, "John")
        self.assertEqual(self.lesson.teacher.last_name, "Doe")

    def test_update_lesson_content(self):
        """Test de la mise à jour du contenu de la leçon."""
        new_content = "Updated content for the maths lesson."
        self.lesson.content = new_content
        self.lesson.save()
        updated_lesson = Lesson.objects.get(id=self.lesson.id)
        self.assertEqual(updated_lesson.content, new_content)

    def test_delete_teacher(self):
        """Test de la suppression du professeur lié à la leçon."""
        self.teacher.delete()
        with self.assertRaises(Lesson.DoesNotExist):
            Lesson.objects.get(id=self.lesson.id)

    def test_change_lesson_visibility(self):
        """Test de la modification de la visibilité de la leçon."""
        self.lesson.is_public = False
        self.lesson.save()
        updated_lesson = Lesson.objects.get(id=self.lesson.id)
        self.assertFalse(updated_lesson.is_public)
