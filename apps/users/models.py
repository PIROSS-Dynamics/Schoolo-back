from django.db import models


# -- User
class User(models.Model):
    ROLE_CHOICES = [
        ('student', 'Étudiant'),
        ('teacher', 'Professeur'),
        ('parent', 'Parent'),
        ('admin', 'Administrateur'),  # Ajout d'un rôle administrateur par exemple
    ]
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student') 

    
    def __str__(self):
        return f"User: {self.first_name} {self.last_name} (Email: {self.email})"

# -- Student
class Student(User):
    experience_level = models.IntegerField(default=0)

    def __str__(self):
        return f"Student: {self.first_name} {self.last_name} - Level: {self.experience_level}"

# -- Teacher
class Teacher(User):

    def __str__(self):
        return f"Teacher: {self.first_name} {self.last_name}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

# -- Parent
class Parent(User):
    children = models.ManyToManyField(Student)

    def __str__(self):
        children_list = ", ".join([f"{child.first_name} {child.last_name}" for child in self.children.all()])
        return f"Parent: {self.first_name} {self.last_name} - Children: {children_list or 'None'}"
