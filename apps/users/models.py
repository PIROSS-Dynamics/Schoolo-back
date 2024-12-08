from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

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
    

    def __str__(self):
        return f"Profile (Photo: {self.photo}, Bio: {self.bio[:30]}...)"




# -------------------------------------------------------------------------------- 
# -- CustomUserManager - un user manager costomisé afin de mieux gérer la création de chaque user
# -------------------------------------------------------------------------------- 

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username,first_name="", last_name="",password=None):
        if not username:
            raise ValueError("username n'est pas donné.")
    
        if not email:
            raise ValueError("email n'est pas donné.")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using= self._db)

        return user

    # -------------------------------------     
    def create_superuser(self,email,username,first_name,last_name, password=None ):
        user = self.create_user(
            email,username,first_name,last_name,password
        )
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using= self._db)
        
        return user






# -------------------------------------------------------------------------------- 
# -- User - un user customisé afin de mieux gérer les fonctonnalités
# -------------------------------------------------------------------------------- 
class CustomUser(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(max_length=50,blank=True)
    last_name = models.CharField(max_length=50,blank=True)
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=50)
    register_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)
    bio = models.TextField(default="")
    
    USERNAME_FIELD ='username'
    REQUIRED_FIELDS=["first_name","last_name","email"]
    
    objects = CustomUserManager()
    
    def __str__(self):
        return f"User: {self.first_name} {self.last_name} (Email: {self.email})"

    
    @property
    def is_staff(self):    # c'est un admin cet utilisateur? (is_staff au lieu de is_admin car cela posait des problème)
        return self.is_admin




# -------------------------------------------------------------------------------- 
# -- Student 
# -------------------------------------------------------------------------------- 
class Student(CustomUser):
    experience_level = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        
    def __str__(self):
        return f"Student: {self.first_name} {self.last_name} - Level: {self.experience_level}"






# -------------------------------------------------------------------------------- 
# -- Teacher 
# -------------------------------------------------------------------------------- 
class Teacher(CustomUser):
    lessons = models.ManyToManyField(
        'lessons.Lesson',
        blank=True,
        related_name='teachers'  # Changez le nom ici si nécessaire
    )

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
        
    def __str__(self):
        return f"Teacher: {self.first_name} {self.last_name}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"






# -------------------------------------------------------------------------------- 
# -- Parent
# -------------------------------------------------------------------------------- 
class Parent(CustomUser):
    children = models.ManyToManyField(Student, related_name='parents')

    class Meta:
        verbose_name = "Parent"
        verbose_name_plural = "Parents"
        
    def __str__(self):
        children_list = ", ".join([f"{child.first_name} {child.last_name}" for child in self.children.all()])
        return f"Parent: {self.first_name} {self.last_name} - Children: {children_list or 'None'}"
