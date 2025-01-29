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
