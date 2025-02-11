# Generated by Django 5.1.2 on 2024-10-30 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('subject', models.CharField(choices=[('Maths', 'Maths'), ('Français', 'Français'), ('Anglais', 'Anglais'), ('Histoire', 'Histoire')], max_length=50)),
                ('content', models.TextField()),
                ('is_public', models.BooleanField(default=True)),
            ],
        ),
    ]
