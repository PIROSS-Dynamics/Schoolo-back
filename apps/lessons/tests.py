from django.test import TestCase
from apps.lessons.models import Lesson
from apps.users.models import Teacher
from django.db.utils import IntegrityError

class LessonModelTestCase(TestCase):
    def setUp(self):
        """Préparer les données pour les tests."""
        self.teacher = Teacher.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="securepassword",
            role="teacher",
        )

        self.lesson = Lesson.objects.create(
            title="Introduction to Maths",
            subject="Maths",
            teacher=self.teacher,
            content="This is the content of the maths lesson.",
            is_public=True,
            description="An introductory lesson to basic maths concepts."
        )


    def test_lesson_creation_without_teacher(self):
        """Test que la création d'une leçon sans professeur échoue."""
        with self.assertRaises(IntegrityError):
            Lesson.objects.create(
                title="Orphan Lesson",
                subject="Maths",
                teacher=None,  # Pas de prof
                content="This lesson should not be created.",
                is_public=True
            )

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
        updated_lesson = Lesson.objects.get(id=self.lesson.id)
        self.assertIsNone(updated_lesson.teacher)  # Vérifie que le champ teacher devient NULL

    def test_change_lesson_visibility(self):
        """Test de la modification de la visibilité de la leçon."""
        self.lesson.is_public = False
        self.lesson.save()
        updated_lesson = Lesson.objects.get(id=self.lesson.id)
        self.assertFalse(updated_lesson.is_public)

    def test_create_lesson_without_teacher(self):
        """Test de la création d'une leçon sans professeur."""
        lesson = Lesson.objects.create(
            title="Self-study Python",
            subject="Informatique",
            teacher=None,  # Aucun professeur assigné
            content="Learn Python by yourself.",
            is_public=True
        )
        self.assertIsNone(lesson.teacher)
        self.assertEqual(lesson.title, "Self-study Python")

    def test_delete_lesson(self):
        """Test de la suppression d'une leçon."""
        lesson_id = self.lesson.id
        self.lesson.delete()
        with self.assertRaises(Lesson.DoesNotExist):
            Lesson.objects.get(id=lesson_id)

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.lessons.models import Lesson
from apps.users.models import Teacher

class LessonViewsTestCase(APITestCase):

    def setUp(self):
        """Préparer les données de test"""
        self.teacher = Teacher.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="securepassword",
            role="teacher"
        )

        self.lesson = Lesson.objects.create(
            title="Introduction to Maths",
            subject="Maths",
            teacher=self.teacher,
            content="This is a basic maths lesson.",
            is_public=True,
            description="A lesson about basic math concepts."
        )

    def test_get_public_lessons(self):
        """Test pour récupérer toutes les leçons publiques"""
        url = reverse('lesson-list')  # ✅ Correspond à `/api/lessonslist/`
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.lesson.title)

    def test_get_lesson_detail(self):
        """Test pour récupérer le détail d’une leçon"""
        url = reverse('lesson-detail', args=[self.lesson.id])  # ✅ `/api/lessonslist/detail/<id>/`
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.lesson.title)

    def test_create_lesson(self):
        """Test pour créer une nouvelle leçon"""
        url = reverse('create-lesson')  # ✅ `/api/lessonslist/add`
        data = {
            "title": "New Maths Lesson",
            "subject": "Maths",
            "teacher": self.teacher.id,
            "content": "This is an advanced maths lesson.",
            "is_public": True,
            "description": "Advanced mathematical concepts."
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_update_lesson(self):
        """Test pour modifier une leçon"""
        url = reverse('lesson-detail', args=[self.lesson.id])  # ✅ `/api/lessonslist/detail/<id>/`
        data = {
            "title": "Updated Maths Lesson",
            "subject": "Maths",
            "content": "Updated content for maths.",
        }
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Maths Lesson")

    def test_delete_lesson(self):
        """Test pour supprimer une leçon"""
        url = reverse('lesson-detail', args=[self.lesson.id])  # ✅ `/api/lessonslist/detail/<id>/`
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_get_teacher_lessons(self):
        """Test pour récupérer les leçons d’un enseignant spécifique"""
        url = reverse('get-teacher-lessons', args=[self.teacher.id])  # ✅ `/api/teacher/<teacher_id>/lessons/`
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.lesson.title)

