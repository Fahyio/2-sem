from django.contrib import admin
from .models import Teacher, TeacherInfo, Course, Student


class TeacherInfoInline(admin.StackedInline):
    model = TeacherInfo
    can_delete = False


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'email', 'phone', 'is_active']
    list_filter = ['is_active', 'hire_date']
    search_fields = ['last_name', 'first_name', 'email']
    inlines = [TeacherInfoInline]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher', 'level', 'start_date', 'max_students', 'current_students_count']
    list_filter = ['level', 'start_date', 'teacher']
    search_fields = ['name', 'description']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'email', 'birth_date', 'is_active', 'courses_count']
    list_filter = ['is_active', 'courses']
    search_fields = ['last_name', 'first_name', 'email']
    filter_horizontal = ['courses']