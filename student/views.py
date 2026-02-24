from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.utils import timezone
from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404, redirect
from exam.models import ExamSchedule, ExamAttempt


def student_dashboard(request):
    user = request.user
    now = timezone.localtime()

    schedules = ExamSchedule.objects.filter(
        group__students=user,
        is_cancelled=False
    ).select_related("exam", "group")

    exam_list = []

    for schedule in schedules:
        exam_datetime_start = datetime.combine(schedule.date, schedule.start_time)
        exam_datetime_end = datetime.combine(schedule.date, schedule.end_time)

        exam_datetime_start = timezone.make_aware(exam_datetime_start)
        exam_datetime_end = timezone.make_aware(exam_datetime_end)

        status = "Upcoming"

        if now.date() == schedule.date:
            if now < exam_datetime_start - timedelta(minutes=10):
                status = "Upcoming"
            elif exam_datetime_start - timedelta(minutes=10) <= now < exam_datetime_start:
                status = "Instructions"
            elif exam_datetime_start <= now <= exam_datetime_end:
                status = "Live"
            else:
                status = "Expired"
        elif now > exam_datetime_end:
            status = "Expired"

        attempt = ExamAttempt.objects.filter(
            student=user,
            schedule=schedule,
            is_submitted=True
        ).exists()

        if attempt:
            status = "Completed"

        exam_list.append({
            "schedule": schedule,
            "status": status
        })

    # Notices (for now simple upcoming today)
    today_exams = [
        exam for exam in exam_list
        if exam["schedule"].date == now.date()
        and exam["status"] in ["Upcoming", "Instructions", "Live"]
    ]

    context = {
        "exam_list": exam_list,
        "today_exams": today_exams,
    }

    return render(request, "student//student_dashboard.html", context)




def start_exam(request, schedule_id):
    schedule = get_object_or_404(
        ExamSchedule,
        id=schedule_id,
        group__students=request.user,
        is_cancelled=False
    )

    now = timezone.localtime()

    start_datetime = timezone.make_aware(
        datetime.combine(schedule.date, schedule.start_time)
    )
    end_datetime = timezone.make_aware(
        datetime.combine(schedule.date, schedule.end_time)
    )

    # 🚨 Security Check
    if now < start_datetime - timedelta(minutes=10):
        return redirect("core:student_dashboard")

    if now > end_datetime:
        return redirect("core:student_dashboard")

    attempt, created = ExamAttempt.objects.get_or_create(
        student=request.user,
        schedule=schedule
    )

    if attempt.is_submitted:
        return redirect("core:student_dashboard")

    remaining_seconds = int((end_datetime - now).total_seconds())

    questions = schedule.exam.questions.all()

    return render(request, "student/exam_page.html", {
        "schedule": schedule,
        "remaining_seconds": remaining_seconds,
        "questions": questions
    })

from django.utils import timezone


def submit_exam(request, schedule_id):
    schedule = get_object_or_404(ExamSchedule, id=schedule_id)

    attempt = get_object_or_404(
        ExamAttempt,
        student=request.user,
        schedule=schedule
    )

    if not attempt.is_submitted:
        attempt.is_submitted = True
        attempt.submitted_at = timezone.now()
        attempt.save()

    return redirect("core:student_dashboard")

from django.http import JsonResponse
from exam.models import StudentAnswer, ExamAttempt, ExamSchedule, Question


def save_answer(request):
    if request.method == "POST":
        question_id = request.POST.get("question_id")
        selected_option = request.POST.get("selected_option")
        schedule_id = request.POST.get("schedule_id")

        schedule = ExamSchedule.objects.get(id=schedule_id)

        attempt = ExamAttempt.objects.get(
            student=request.user,
            schedule=schedule,
            is_submitted=False
        )

        question = Question.objects.get(id=question_id)

        StudentAnswer.objects.update_or_create(
            attempt=attempt,
            question=question,
            defaults={"selected_option": selected_option}
        )

        return JsonResponse({"status": "saved"})


from exam.models import StudentAnswer


def submit_exam(request, schedule_id):
    schedule = get_object_or_404(ExamSchedule, id=schedule_id)

    attempt = get_object_or_404(
        ExamAttempt,
        student=request.user,
        schedule=schedule,
        is_submitted=False
    )

    answers = StudentAnswer.objects.filter(attempt=attempt)

    total_score = 0

    for answer in answers:
        if answer.selected_option == answer.question.correct_option:
            total_score += answer.question.marks

    attempt.is_submitted = True
    attempt.submitted_at = timezone.now()
    attempt.save()

    return redirect("core:student_dashboard")