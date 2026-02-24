from django import forms
from .models import Teacher, TeacherInfo, Course, Student


class TeacherForm(forms.ModelForm):
    """Форма для создания/обновления преподавателя"""

    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'email', 'phone', 'hire_date', 'is_active']
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
        }


class TeacherInfoForm(forms.ModelForm):
    """Форма для информации о преподавателе"""

    class Meta:
        model = TeacherInfo
        fields = ['biography', 'education', 'specialization', 'experience_years',
                  'office_number', 'consultation_hours']


class CourseForm(forms.ModelForm):
    """Форма для создания/обновления курса"""

    class Meta:
        model = Course
        fields = ['name', 'description', 'teacher', 'level', 'duration_weeks',
                  'max_students', 'start_date', 'price']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].queryset = Teacher.objects.filter(is_active=True)
        self.fields['teacher'].empty_label = "Выберите преподавателя"


class StudentForm(forms.ModelForm):
    """Форма для создания/обновления студента"""

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'phone', 'birth_date', 'is_active']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }