from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('student/login/', views.student_login, name='student_login'),
    path('student/register/', views.student_register, name='student_register'),
    path('teacher/login/', views.teacher_login, name='teacher_login'),
    path('teacher/register/', views.teacher_register, name='teacher_register'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
]
