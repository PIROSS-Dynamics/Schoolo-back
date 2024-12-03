# Generated by Django 5.1.2 on 2024-11-18 11:02

import apps.users.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('users', '0005_remove_task_created_by_task_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='task',
            name='user',
        ),
        migrations.AddField(
            model_name='task',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to='users.student'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='students',
            field=models.ManyToManyField(related_name='teachers', to='users.student'),
        ),
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(default='No bio.', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
        migrations.AddField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, default='user_photos/NoPhoto.jpg', null=True, upload_to=apps.users.models.user_directory_path),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('student', 'Student'), ('parent', 'Parent'), ('teacher', 'Teacher')], default='student', max_length=10),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='parent',
            name='children',
            field=models.ManyToManyField(related_name='parents', to='users.student'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
