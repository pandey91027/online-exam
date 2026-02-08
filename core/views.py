from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def student_dashboard(request):
    return render(request, 'accounts//student_dashboard.html')

@login_required
def teacher_dashboard(request):
    return render(request, 'accounts\\teacher_dashboard.html')

# def logout_view(request):
#     logout(request)
#     return redirect('landingpage')

def landingpage(request):
    return render(request, 'landingpage.html')
