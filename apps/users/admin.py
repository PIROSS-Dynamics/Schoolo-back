from django.contrib import admin
from .models import User, Student, Teacher, Parent



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')

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
