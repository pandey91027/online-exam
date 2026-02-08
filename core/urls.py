from django.urls import path
from core import views 

app_name='core'

urlpatterns = [
    path('', views.landingpage, name='landingpage'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
] 


