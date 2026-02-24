from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    path("exam/<int:schedule_id>/start/", views.start_exam, name="start_exam"),
    path("exam/<int:schedule_id>/submit/", views.submit_exam, name="submit_exam"),
    path("save-answer/", views.save_answer, name="save_answer"),


]