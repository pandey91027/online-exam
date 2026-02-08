from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import StudentRegisterForm, TeacherRegisterForm
from django.contrib.auth.decorators import login_required
from .forms import (
    UserUpdateForm,
    StudentProfileForm,
    TeacherProfileForm
)

# ---------- STUDENT REGISTER ----------
def student_register(request):
    form = StudentRegisterForm()

    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student account created successfully')
            return redirect('accounts:student_login')

    return render(request, 'accounts/student_register.html', {'form': form})


# ---------- TEACHER REGISTER ----------
def teacher_register(request):
    form = TeacherRegisterForm()

    if request.method == 'POST':
        form = TeacherRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher account created successfully')
            return redirect('accounts:teacher_login')

    return render(request, 'accounts/teacher_register.html', {'form': form})


# ---------- STUDENT LOGIN ----------
def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user and user.user_type == 'student':
            login(request, user)
            return redirect('core:student_dashboard')
        else:
            messages.error(request, 'Invalid student credentials')

    return render(request, 'accounts/student_login.html')


# ---------- TEACHER LOGIN ----------
def teacher_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user and user.user_type == 'teacher':
            login(request, user)
            return redirect('core:teacher_dashboard')
        else:
            messages.error(request, 'Invalid teacher credentials')

    return render(request, 'accounts/teacher_login.html')

def logout_view(request):
    logout(request)
    return redirect('core:landingpage')

@login_required
def profile_view(request):
    user = request.user

    user_form = UserUpdateForm(instance=user)
    profile_form = None

    if user.user_type == 'student':
        profile = user.student_profile
        profile_form = StudentProfileForm(instance=profile)

    elif user.user_type == 'teacher':
        profile = user.teacher_profile
        profile_form = TeacherProfileForm(instance=profile)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)

        if user.user_type == 'student':
            profile_form = StudentProfileForm(
                request.POST,
                instance=user.student_profile
            )

        elif user.user_type == 'teacher':
            profile_form = TeacherProfileForm(
                request.POST,
                instance=user.teacher_profile
            )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('accounts:profile')

    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_type': user.user_type
    })
