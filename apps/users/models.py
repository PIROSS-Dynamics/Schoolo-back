from django.db import models

# -- Task
class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"Task: {self.name} (Start: {self.start_date}, End: {self.end_date})"

# -- Schedule
class Schedule(models.Model):
    tasks = models.ManyToManyField(Task)

    def __str__(self):
        return f"Schedule with {self.tasks.count()} task(s)"

# -- Profile
class Profile(models.Model):
    photo = models.CharField(max_length=200)
    bio = models.TextField()

    def __str__(self):
        return f"Profile (Photo: {self.photo}, Bio: {self.bio[:30]}...)"

# -- User
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=50)
    schedule = models.ForeignKey(Schedule, on_delete=models.SET_NULL, null=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"User: {self.first_name} {self.last_name} (Email: {self.email})"

# -- Student
class Student(User):
    experience_level = models.IntegerField(default=0)

    def __str__(self):
        return f"Student: {self.first_name} {self.last_name} - Level: {self.experience_level}"

# -- Teacher
class Teacher(User):
    lessons = models.ManyToManyField(
        'lessons.Lesson',
        blank=True,
        related_name='teachers'  # Changez le nom ici si nécessaire
    )

    def __str__(self):
        return f"Teacher: {self.first_name} {self.last_name}"

# -- Parent
class Parent(User):
    children = models.ManyToManyField(Student)

    def __str__(self):
        children_list = ", ".join([f"{child.first_name} {child.last_name}" for child in self.children.all()])
        return f"Parent: {self.first_name} {self.last_name} - Children: {children_list or 'None'}"
