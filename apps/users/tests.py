from django.test import TestCase
from apps.users.models import User, Student, Teacher, Parent

class UserModelTestCase(TestCase):

    def setUp(self):
        """Préparer les données pour les tests."""
        self.user = User.objects.create(
            first_name="Alice",
            last_name="Durand",
            email="alice.durand@example.com",
            password="password123",
            role="student"
        )

        self.teacher = Teacher.objects.create(
            first_name="Paul",
            last_name="Martin",
            email="paul.martin@example.com",
            password="password123",
            role="teacher"
        )

        self.student1 = Student.objects.create(
            first_name="Leo",
            last_name="Petit",
            email="leo.petit@example.com",
            password="password123",
            role="student",
            experience_level=5
        )

        self.student2 = Student.objects.create(
            first_name="Emma",
            last_name="Blanc",
            email="emma.blanc@example.com",
            password="password123",
            role="student",
            experience_level=3
        )

        self.parent = Parent.objects.create(
            first_name="Sophie",
            last_name="Noir",
            email="sophie.noir@example.com",
            password="password123",
            role="parent"
        )
        self.parent.children.add(self.student1, self.student2)

    def test_user_creation(self):
        """Test de création d'un utilisateur générique."""
        self.assertEqual(self.user.first_name, "Alice")
        self.assertEqual(self.user.role, "student")

    def test_teacher_creation(self):
        """Test de création d'un enseignant."""
        self.assertEqual(str(self.teacher), "Teacher: Paul Martin")
        self.assertEqual(self.teacher.get_full_name(), "Paul Martin")

    def test_student_creation(self):
        """Test de création d'un étudiant."""
        self.assertEqual(self.student1.experience_level, 5)
        self.assertEqual(str(self.student1), "Student: Leo Petit - Level: 5")

    def test_parent_creation(self):
        """Test de la relation Parent <-> Enfants."""
        self.assertEqual(self.parent.children.count(), 2)
        self.assertEqual(
            str(self.parent), 
            "Parent: Sophie Noir - Children: Leo Petit, Emma Blanc"
        )

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.users.models import User, Teacher, Student, Parent

class UserViewsTestCase(APITestCase):

    def setUp(self):
        """Préparer les données de test"""
        self.teacher = Teacher.objects.create(
            first_name="Alice",
            last_name="Dupont",
            email="alice.dupont@example.com",
            password="securepassword",
            role="teacher"
        )

        self.student = Student.objects.create(
            first_name="Bob",
            last_name="Martin",
            email="bob.martin@example.com",
            password="securepassword",
            role="student",
            experience_level=5
        )

        self.parent = Parent.objects.create(
            first_name="Clara",
            last_name="Lemoine",
            email="clara.lemoine@example.com",
            password="securepassword",
            role="parent"
        )

    def test_register_student(self):
        """Test pour enregistrer un étudiant"""
        url = reverse('register')
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "securepassword",
            "role": "student"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 4)  # Un nouvel utilisateur doit être ajouté

    def test_register_teacher(self):
        """Test pour enregistrer un enseignant"""
        url = reverse('register')
        data = {
            "first_name": "Paul",
            "last_name": "Rousseau",
            "email": "paul.rousseau@example.com",
            "password": "securepassword",
            "role": "teacher"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 5)

    def test_register_existing_email(self):
        """Test pour empêcher l'inscription avec un email déjà utilisé"""
        url = reverse('register')
        data = {
            "first_name": "Alice",
            "last_name": "Dupont",
            "email": "alice.dupont@example.com",  # Déjà utilisé
            "password": "securepassword",
            "role": "teacher"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_login_successful(self):
        """Test pour un login réussi"""
        url = reverse('login')
        data = {
            "email": "alice.dupont@example.com",
            "password": "securepassword"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_login_wrong_password(self):
        """Test pour un login avec un mauvais mot de passe"""
        url = reverse('login')
        data = {
            "email": "alice.dupont@example.com",
            "password": "wrongpassword"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_user_not_found(self):
        """Test pour un login avec un email non enregistré"""
        url = reverse('login')
        data = {
            "email": "nonexistent@example.com",
            "password": "securepassword"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_teacher(self):
        """Test pour récupérer un enseignant spécifique"""
        url = reverse('get-teacher', args=[self.teacher.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.teacher.email)

    def test_get_student(self):
        """Test pour récupérer un étudiant spécifique"""
        url = reverse('get-student', args=[self.student.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.student.email)

    def test_get_parent(self):
        """Test pour récupérer un parent spécifique"""
        url = reverse('get-parent', args=[self.parent.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.parent.email)

    def test_list_teachers(self):
        """Test pour récupérer la liste des enseignants"""
        url = reverse('list-teachers')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Un seul enseignant ajouté dans `setUp`
