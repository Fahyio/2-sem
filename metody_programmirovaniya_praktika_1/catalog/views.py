# -*- coding: utf-8 -*-
from django.shortcuts import render
from .data import COURSES, AUTHORS

def index(request):
    """Главная страница"""
    return render(request, 'index.html')

def courses_list(request):
    """Список всех курсов"""
    return render(request, 'courses.html', {'courses': COURSES})

def course_detail(request, course_id):
    """Страница одного курса"""
    course = next((c for c in COURSES if c['id'] == course_id), None)
    if not course:
        return render(request, 'not_found.html', status=404)
    
    # Находим автора курса
    author = next((a for a in AUTHORS if a['id'] == course['author_id']), None)
    
    # Убедимся что все поля курса существуют
    course_with_defaults = {
        'id': course.get('id', ''),
        'title': course.get('title', 'Без названия'),
        'description': course.get('description', 'Нет описания'),
        'full_description': course.get('full_description', course.get('description', 'Нет подробного описания')),
        'author_id': course.get('author_id', 0),
        'duration': course.get('duration', 'Не указано'),
        'level': course.get('level', 'Не указан'),
        'category': course.get('category', 'Без категории'),
        'lessons': course.get('lessons', 0),
        'projects': course.get('projects', 0),
        'rating': course.get('rating', 0.0),
        'students': course.get('students', 0),
    }
    
    return render(request, 'course_detail.html', {
        'course': course_with_defaults,
        'author': author
    })

def authors_list(request):
    """Список всех авторов"""
    return render(request, 'authors.html', {'authors': AUTHORS})

def author_detail(request, author_id):
    """Страница одного автора"""
    author = next((a for a in AUTHORS if a['id'] == author_id), None)
    if not author:
        return render(request, 'not_found.html', status=404)
    
    # Находим курсы этого автора
    author_courses = [c for c in COURSES if c['author_id'] == author_id]
    return render(request, 'author_details.html', {
        'author': author,
        'courses': author_courses
    })

def info_page(request):
    """Страница информации о сайте"""
    return render(request, 'info.html')

def not_found(request, exception=None):
    """Страница 404 - не найдено"""
    return render(request, 'not_found.html', status=404)