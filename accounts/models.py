from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES
    )

    def __str__(self):
        return f"{self.username} ({self.user_type})"


class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    roll_number = models.CharField(max_length=50, blank=True)
    course = models.CharField(max_length=100, blank=True)
    year = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Student Profile - {self.user.username}"


class TeacherProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )

    department = models.CharField(max_length=100, blank=True)
    qualification = models.CharField(max_length=100, blank=True)
    experience = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Teacher Profile - {self.user.username}"
