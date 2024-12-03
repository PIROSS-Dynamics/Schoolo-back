from rest_framework import serializers
from .models import User, Student, Teacher, Parent, Task
from rest_framework.authtoken.models import Token

# --- Base User Serializer ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'photo', 'bio', 'username', 'first_name', 'last_name', 'email', 'role']


# --- Sign Up Serializer ---
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'first_name', 'last_name', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    # Custom validation for username
    def validate_username(self, value):
        role = self.initial_data.get('role', 'student')
        if User.objects.filter(username=value, role=role).exists():
            raise serializers.ValidationError(f"The username '{value}' already exists for the role '{role}'.")
        return value

    # Custom validation for email
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        # Create user using User model
        user = User.objects.create_user(**validated_data)
        role = validated_data.get('role', 'student')

        # Create role-specific instance
        if role == 'student':
            Student.objects.create(
                user_ptr=user,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                role='student',
                password=user.password
            )
        elif role == 'teacher':
            Teacher.objects.create(
                user_ptr=user,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                role='teacher',
                password=user.password
            )
        elif role == 'parent':
            Parent.objects.create(
                user_ptr=user,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                role='parent',
                password=user.password
            )

        # Generate token for the user
        Token.objects.create(user=user)
        return user



# --- Login Serializer ---
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        from django.contrib.auth import authenticate
        user = authenticate(email=data.get('email'), password=data.get('password'))
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return user


# --- Student Serializer ---
class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Embed User fields

    class Meta:
        model = Student
        fields = ['id', 'user', 'experience_level']


# --- Teacher Serializer ---
class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Embed User fields
    students = StudentSerializer(many=True)  # Show related students

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'students', 'lessons']


# --- Parent Serializer ---
class ParentSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Embed User fields
    children = StudentSerializer(many=True)  # Show related children

    class Meta:
        model = Parent
        fields = ['id', 'user', 'children']


# --- Task Serializer ---
class TaskSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)  # Show student data
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(),
        source='student',  # Maps to the student ForeignKey
        write_only=True
    )

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'subject',
            'student', 'student_id', 'start_hour', 'end_hour', 'realization_date'
        ]
