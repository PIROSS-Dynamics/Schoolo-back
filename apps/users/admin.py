from django.contrib import admin
from .models import Task, Schedule, Profile, User, Student, Teacher, Parent

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'start_date', 'end_date')
    search_fields = ('name', 'description')
    list_filter = ('start_date', 'end_date')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_tasks')
    
    def get_tasks(self, obj):
        return ", ".join([task.name for task in obj.tasks.all()])
    get_tasks.short_description = 'Tasks'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'photo', 'bio')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'schedule', 'profile')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('schedule',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'experience_level')
    search_fields = ('first_name', 'last_name')
    list_filter = ('experience_level',)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name')

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'get_children')
    search_fields = ('first_name', 'last_name')
    
    def get_children(self, obj):
        return ", ".join([f"{child.first_name} {child.last_name}" for child in obj.children.all()])
    get_children.short_description = 'Children'
