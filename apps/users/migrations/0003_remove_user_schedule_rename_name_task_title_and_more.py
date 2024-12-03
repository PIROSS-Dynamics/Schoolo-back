# Generated by Django 5.1.2 on 2024-11-05 20:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_teacher_lessons'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='schedule',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='name',
            new_name='title',
        ),
        migrations.AddField(
            model_name='task',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.user'),
        ),
        migrations.AddField(
            model_name='task',
            name='subject',
            field=models.CharField(choices=[('Maths', 'Maths'), ('Français', 'Français'), ('Anglais', 'Anglais'), ('Histoire', 'Histoire')], max_length=50, null=True),
        ),
        migrations.DeleteModel(
            name='Schedule',
        ),
    ]