from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Teacher(models.Model):
    """Модель преподавателя"""
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    email = models.EmailField('Email', unique=True)
    phone = models.CharField('Телефон', max_length=20, blank=True, null=True)
    hire_date = models.DateField('Дата найма', default=timezone.now)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def get_full_name(self):
        return f"{self.last_name} {self.first_name}"


class TeacherInfo(models.Model):
    """Дополнительная информация о преподавателе"""
    teacher = models.OneToOneField(
        Teacher,
        on_delete=models.CASCADE,
        related_name='info',
        verbose_name='Преподаватель'
    )
    biography = models.TextField('Биография', blank=True)
    education = models.CharField('Образование', max_length=200)
    specialization = models.CharField('Специализация', max_length=200)
    experience_years = models.IntegerField(
        'Опыт работы (лет)',
        validators=[MinValueValidator(0), MaxValueValidator(70)]
    )
    office_number = models.CharField('Номер кабинета', max_length=10, blank=True)
    consultation_hours = models.CharField('Часы консультаций', max_length=200, blank=True)

    class Meta:
        verbose_name = 'Информация о преподавателе'
        verbose_name_plural = 'Информация о преподавателях'

    def __str__(self):
        return f"Информация о {self.teacher.get_full_name()}"


class Course(models.Model):
    """Модель курса"""
    LEVEL_CHOICES = [
        ('beginner', 'Начальный'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    ]

    name = models.CharField('Название курса', max_length=200, unique=True)
    description = models.TextField('Описание', blank=True)
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        related_name='courses',
        verbose_name='Преподаватель',
        null=True,
        blank=True
    )
    level = models.CharField('Уровень', max_length=20, choices=LEVEL_CHOICES, default='beginner')
    duration_weeks = models.IntegerField('Длительность (недель)', validators=[MinValueValidator(1)])
    max_students = models.IntegerField('Максимум студентов', validators=[MinValueValidator(1)])
    start_date = models.DateField('Дата начала')
    price = models.DecimalField('Стоимость', max_digits=10, decimal_places=2)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['start_date', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"

    def current_students_count(self):
        return self.students.count()


class Student(models.Model):
    """Модель студента"""
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    email = models.EmailField('Email', unique=True)
    phone = models.CharField('Телефон', max_length=20)
    birth_date = models.DateField('Дата рождения')
    enrollment_date = models.DateField('Дата поступления', auto_now_add=True)
    is_active = models.BooleanField('Активен', default=True)
    courses = models.ManyToManyField(
        Course,
        related_name='students',
        verbose_name='Курсы',
        blank=True
    )

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        ordering = ['last_name', 'first_name']
        unique_together = ['first_name', 'last_name', 'birth_date']

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def get_full_name(self):
        return f"{self.last_name} {self.first_name}"

    def courses_count(self):
        return self.courses.count()