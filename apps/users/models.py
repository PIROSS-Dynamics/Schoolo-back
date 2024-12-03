#-------------------------------------------------------------------------
#                               IMPORTS
#-------------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
import os


#-------------------------------------------------------------------------
#                               User Manager
#-------------------------------------------------------------------------
class UserManager(BaseUserManager):
    """ 
    Gère la création des utilisateurs et des super utilisateurs.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Le champ email doit être renseigné.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')  # Force the role to be admin for superusers

        if not extra_fields.get('is_staff'):
            raise ValueError("Le super utilisateur doit avoir is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Le super utilisateur doit avoir is_superuser=True.")
        if extra_fields.get('role') != 'admin':
            raise ValueError("Le super utilisateur doit avoir le rôle 'admin'.")

        return self.create_user(email, password, **extra_fields)





#-------------------------------------------------------------------------
#                               Methods
#-------------------------------------------------------------------------
def user_directory_path(instance, filename): 
    """
        Retourne le chemin du dossier où enregistrer les images des utilisateurs.
    """
    return f'user_photos/user_{instance.id}/{filename}'


def generate_unique_username():
    """ 
    Ca genere un username automatique au cas ou un utilisateur arrive à ne pas saisir ses infos
    """
    from uuid import uuid4
    return f"user_{uuid4().hex[:8]}"  # Generates a unique username like 'user_ab12cd34'

#-------------------------------------------------------------------------
#                               MODELS
#-------------------------------------------------------------------------

# ---- USER
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('parent', 'Parent'),
        ('teacher', 'Teacher'),
    ]
    photo = models.ImageField(
        upload_to=user_directory_path,
        null=True,
        default="media/user_photos/NoPhoto.jpg",
        blank=True
    )
    bio = models.TextField(null=True, default="No bio.")
    username = models.CharField(null=True, max_length=20, unique=True)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=254, null=False, unique=True)
    password = models.CharField(max_length=50, null=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=False, default="student")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']  # Removed 'role' from REQUIRED_FIELDS

    objects = UserManager()

    def save(self, *args, **kwargs):
        if self.role == 'admin' and not self.is_superuser:
            raise ValidationError("The role 'admin' cannot be assigned to a regular user.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"




# ---- STUDENT
class Student(User):
    experience_level = models.IntegerField(default=0)

    def __str__(self):
        return f"Student: {self.first_name} {self.last_name} - Level: {self.experience_level}"

    def get_tasks(self):
        return self.tasks.all()


# ---- TEACHER
class Teacher(User):
    students = models.ManyToManyField('Student', related_name='teachers')
    lessons = models.ManyToManyField(
        'lessons.Lesson',
        blank=True,
        related_name='teachers'
    )

    def __str__(self):
        return f"Teacher: {self.first_name} {self.last_name}"


# ---- PARENT
class Parent(User):
    children = models.ManyToManyField(Student, related_name="parents")

    def __str__(self):
        children_list = ", ".join([f"{child.first_name} {child.last_name}" for child in self.children.all()])
        return f"Parent: {self.first_name} {self.last_name} - Children: {children_list or 'None'}"


# ---- TASK
class Task(models.Model):
    SUBJECT_CHOICES = [
        ('Maths', 'Maths'),
        ('Français', 'Français'),
        ('Anglais', 'Anglais'),
        ('Histoire', 'Histoire'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES, null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, related_name='tasks')
    start_hour = models.TimeField(null=True)
    end_hour = models.TimeField(null=True)
    realization_date = models.DateField(null=True)

    def __str__(self):
        return f"Task: {self.title}, for {self.student} on {self.realization_date}"
