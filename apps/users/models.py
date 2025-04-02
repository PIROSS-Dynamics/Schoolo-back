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
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student') 
    is_hashed = models.BooleanField(default=False)
    
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
    

    def __str__(self):
        children_list = ", ".join([f"{child.first_name} {child.last_name}" for child in self.children.all()])
        return f"Parent: {self.first_name} {self.last_name} - Children: {children_list or 'None'}"

class Relation(models.Model):
    RELATION_TYPE_CHOICES = [
        ('parent', 'Parent'),
        ('school', 'school'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_relations')
    relation_type = models.CharField(max_length=10, choices=RELATION_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.first_name} {self.sender.last_name} - {self.student.first_name} {self.student.last_name} ({self.relation_type})"
