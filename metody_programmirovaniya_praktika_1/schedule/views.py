from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from .models import Teacher, TeacherInfo, Course, Student
from .forms import TeacherForm, TeacherInfoForm, CourseForm, StudentForm


# ============= TEACHER VIEWS =============

def teacher_index(request):
    """Список всех преподавателей"""
    teachers = Teacher.objects.all()
    return render(request, 'schedule/teacher/index.html', {'teachers': teachers})


def teacher_info(request, pk):
    """Подробная информация о преподавателе"""
    teacher = get_object_or_404(Teacher.objects.prefetch_related('courses'), pk=pk)
    return render(request, 'schedule/teacher/info.html', {'teacher': teacher})


def teacher_create(request):
    """Создание нового преподавателя"""
    if request.method == 'POST':
        teacher_form = TeacherForm(request.POST)
        info_form = TeacherInfoForm(request.POST)

        if teacher_form.is_valid() and info_form.is_valid():
            teacher = teacher_form.save()
            teacher_info = info_form.save(commit=False)
            teacher_info.teacher = teacher
            teacher_info.save()
            messages.success(request, 'Преподаватель успешно создан')
            return redirect('schedule:teacher_info', pk=teacher.pk)
    else:
        teacher_form = TeacherForm()
        info_form = TeacherInfoForm()

    return render(request, 'schedule/teacher/create.html', {
        'teacher_form': teacher_form,
        'info_form': info_form
    })


def teacher_update(request, pk):
    """Обновление информации о преподавателе"""
    teacher = get_object_or_404(Teacher, pk=pk)
    teacher_info, created = TeacherInfo.objects.get_or_create(teacher=teacher)

    if request.method == 'POST':
        teacher_form = TeacherForm(request.POST, instance=teacher)
        info_form = TeacherInfoForm(request.POST, instance=teacher_info)

        if teacher_form.is_valid() and info_form.is_valid():
            teacher_form.save()
            info_form.save()
            messages.success(request, 'Информация о преподавателе обновлена')
            return redirect('schedule:teacher_info', pk=teacher.pk)
    else:
        teacher_form = TeacherForm(instance=teacher)
        info_form = TeacherInfoForm(instance=teacher_info)

    return render(request, 'schedule/teacher/update.html', {
        'teacher_form': teacher_form,
        'info_form': info_form,
        'teacher': teacher
    })


def teacher_delete(request, pk):
    """Удаление преподавателя"""
    teacher = get_object_or_404(Teacher, pk=pk)

    if request.method == 'POST':
        teacher.delete()
        messages.success(request, 'Преподаватель удален')
        return redirect('schedule:teacher_index')

    return render(request, 'schedule/teacher/delete.html', {'teacher': teacher})


# ============= COURSE VIEWS =============

def course_index(request):
    """Список курсов с фильтрацией по преподавателю"""
    teacher_id = request.GET.get('teacher')
    courses = Course.objects.select_related('teacher').annotate(
        students_count=Count('students')
    )

    if teacher_id:
        courses = courses.filter(teacher_id=teacher_id)

    teachers = Teacher.objects.filter(is_active=True)

    return render(request, 'schedule/course/index.html', {
        'courses': courses,
        'teachers': teachers,
        'selected_teacher': teacher_id
    })


def course_create(request):
    """Создание нового курса с выбором преподавателя"""
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, 'Курс успешно создан')
            return redirect('schedule:course_index')
    else:
        form = CourseForm()

    return render(request, 'schedule/course/create.html', {'form': form})


def course_update(request, pk):
    """Обновление курса"""
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Курс обновлен')
            return redirect('schedule:course_index')
    else:
        form = CourseForm(instance=course)

    return render(request, 'schedule/course/update.html', {'form': form, 'course': course})


def course_delete(request, pk):
    """Удаление курса"""
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Курс удален')
        return redirect('schedule:course_index')

    return render(request, 'schedule/course/delete.html', {'course': course})


# ============= STUDENT VIEWS =============

def student_index(request):
    """Список всех студентов"""
    students = Student.objects.annotate(courses_count=Count('courses'))
    return render(request, 'schedule/student/index.html', {'students': students})


def student_create(request):
    """Создание нового студента"""
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, 'Студент успешно создан')
            return redirect('schedule:student_index')
    else:
        form = StudentForm()

    return render(request, 'schedule/student/create.html', {'form': form})


def student_update(request, pk):
    """Обновление информации о студенте"""
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Информация о студенте обновлена')
            return redirect('schedule:student_index')
    else:
        form = StudentForm(instance=student)

    return render(request, 'schedule/student/update.html', {'form': form, 'student': student})


def student_delete(request, pk):
    """Удаление студента"""
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Студент удален')
        return redirect('schedule:student_index')

    return render(request, 'schedule/student/delete.html', {'student': student})


def student_enroll(request, pk):
    """Запись студента на курс"""
    student = get_object_or_404(Student, pk=pk)
    courses = Course.objects.filter(
        start_date__gte=timezone.now().date()
    ).exclude(students=student)

    if request.method == 'POST':
        course_id = request.POST.get('course')
        if course_id:
            course = get_object_or_404(Course, pk=course_id)
            if course.students.count() < course.max_students:
                student.courses.add(course)
                messages.success(request, f'Студент записан на курс "{course.name}"')
            else:
                messages.error(request, 'На курсе нет свободных мест')
        return redirect('schedule:student_enroll', pk=student.pk)

    return render(request, 'schedule/student/enroll.html', {
        'student': student,
        'courses': courses
    })


def student_enroll(request, pk):
    """Запись студента на курс"""
    student = get_object_or_404(Student, pk=pk)
    # Фильтруем курсы, которые еще не начались или уже идут
    courses = Course.objects.filter(
        start_date__gte=timezone.now().date()
    ).exclude(students=student)

    if request.method == 'POST':
        course_id = request.POST.get('course')
        if course_id:
            course = get_object_or_404(Course, pk=course_id)
            # Проверяем, есть ли места на курсе
            if course.students.count() < course.max_students:
                student.courses.add(course)
                messages.success(request, f'Студент {student.get_full_name()} записан на курс "{course.name}"')
            else:
                messages.error(request, 'На курсе нет свободных мест')
        return redirect('schedule:student_enroll', pk=student.pk)

    return render(request, 'schedule/student/enroll.html', {
        'student': student,
        'courses': courses
    })
# ============= ORM QUERIES VIEW =============

def orm_queries(request):
    """Демонстрация ORM-запросов"""

    # 1. Все студенты курса (для примера берем первый курс)
    first_course = Course.objects.first()
    course_students = first_course.students.all() if first_course else []

    # 2. Все преподаватели, у которых больше 1 курса
    teachers_with_multiple_courses = Teacher.objects.annotate(
        course_count=Count('courses')
    ).filter(course_count__gt=1)

    # 3. Студенты без курсов
    students_without_courses = Student.objects.annotate(
        course_count=Count('courses')
    ).filter(course_count=0)

    # 4. Преподаватели без профиля (TeacherInfo)
    teachers_without_profile = Teacher.objects.filter(
        info__isnull=True
    ).select_related('info')

    return render(request, 'schedule/orm_queries.html', {
        'course_students': course_students,
        'first_course': first_course,
        'teachers_with_multiple_courses': teachers_with_multiple_courses,
        'students_without_courses': students_without_courses,
        'teachers_without_profile': teachers_without_profile,
    })


def student_unenroll(request, student_pk, course_pk):
    """Отписка студента от курса"""
    student = get_object_or_404(Student, pk=student_pk)
    course = get_object_or_404(Course, pk=course_pk)

    if request.method == 'POST':
        student.courses.remove(course)
        messages.success(request, f'Студент {student.get_full_name()} отписан от курса "{course.name}"')

    return redirect('schedule:student_index')