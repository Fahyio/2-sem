from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    # Teacher URLs
    path('teachers/', views.teacher_index, name='teacher_index'),
    path('teachers/<int:pk>/', views.teacher_info, name='teacher_info'),
    path('teachers/create/', views.teacher_create, name='teacher_create'),
    path('teachers/<int:pk>/update/', views.teacher_update, name='teacher_update'),
    path('teachers/<int:pk>/delete/', views.teacher_delete, name='teacher_delete'),

    # Course URLs
    path('courses/', views.course_index, name='course_index'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:pk>/update/', views.course_update, name='course_update'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),

    # Student URLs
    path('students/', views.student_index, name='student_index'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:pk>/update/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('students/<int:pk>/enroll/', views.student_enroll, name='student_enroll'),
    path('students/<int:student_pk>/unenroll/<int:course_pk>/',
         views.student_unenroll, name='student_unenroll'),  # ЭТА СТРОКА ДОЛЖНА БЫТЬ

    # ORM Queries
    path('orm-queries/', views.orm_queries, name='orm_queries'),
]