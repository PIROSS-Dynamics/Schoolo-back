from django.contrib import admin
from .models import Lesson


class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'is_public')  

admin.site.register(Lesson, LessonAdmin)
