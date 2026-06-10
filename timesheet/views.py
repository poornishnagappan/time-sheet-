from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Sum
from django.contrib import messages

from .models import EmployeeTask, Profile
from .decorators import manager_required


# =========================
# EMPLOYEE LOGIN
# =========================

def employee_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("employee_dashboard")

        return HttpResponse("Invalid login")

    return render(request, "timesheet/employee_login.html")


# =========================
# MANAGER LOGIN
# =========================

def manager_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        print("USERNAME =", username)
        print("PASSWORD =", password)

        user = authenticate(
            request,
            username=username,
            password=password
        )

        print("AUTH RESULT =", user)

        if not user:
            return HttpResponse("Invalid login (auth failed)")

        login(request, user)

        try:
            profile = Profile.objects.get(user=user)
            print("ROLE =", profile.role)

        except Profile.DoesNotExist:
            return HttpResponse("Profile not found")

        if profile.role != "manager":
            return HttpResponse("Access denied: Manager only")

        return redirect("manager_dashboard")

    return render(request, "timesheet/manager_login.html")

# =========================
# EMPLOYEE DASHBOARD
# =========================

@login_required
def employee_dashboard(request):

    tasks = EmployeeTask.objects.filter(user=request.user).order_by("-created_at")

    total_hours = tasks.aggregate(Sum("hours"))["hours__sum"] or 0
    total_tasks = tasks.count()
    pending_tasks = tasks.filter(status="Pending").count()

    return render(request, "timesheet/employee_dashboard.html", {
        "tasks": tasks,
        "total_hours": total_hours,
        "total_tasks": total_tasks,
        "pending_tasks": pending_tasks,
    })


# =========================
# ADD TASK
# =========================

@login_required
def add_task(request):

    if request.method == "POST":

        task_names = request.POST.getlist('task_name')
        descriptions = request.POST.getlist('description')
        hours_list = request.POST.getlist('hours')
        dates = request.POST.getlist('date')

        for i in range(len(task_names)):

            task_name = task_names[i].strip()

            if not task_name:
                continue

            EmployeeTask.objects.create(
                user=request.user,
                task_name=task_name,
                description=descriptions[i] if i < len(descriptions) else "",
                hours=hours_list[i] if i < len(hours_list) else 0,
                date=dates[i] if i < len(dates) else None
            )

        return redirect("employee_dashboard")

    return render(request, "timesheet/add_task.html")


# =========================
# EDIT TASK
# =========================

@login_required
def edit_task(request, task_id):

    task = get_object_or_404(EmployeeTask, id=task_id, user=request.user)

    if request.method == "POST":

        task.task_name = request.POST.get("task")
        task.description = request.POST.get("description")
        task.hours = request.POST.get("hours")

        task.save()

        return redirect("employee_dashboard")

    return render(request, "timesheet/edit_task.html", {"task": task})


# =========================
# DELETE TASK
# =========================

@login_required
def delete_task(request, task_id):

    task = get_object_or_404(EmployeeTask, id=task_id, user=request.user)
    task.delete()

    return redirect("employee_dashboard")


# =========================
# LOGOUT
# =========================

def employee_logout(request):

    logout(request)
    return redirect("employee_login")


# =========================
# MANAGER DASHBOARD
# =========================

@manager_required
def manager_dashboard(request):

    tasks = EmployeeTask.objects.all().order_by("-created_at")

    total_tasks = tasks.count()

    pending = tasks.filter(
        status="Pending"
    ).count()

    approved = tasks.filter(
        status="Approved"
    ).count()

    rejected = tasks.filter(
        status="Rejected"
    ).count()

    return render(
        request,
        "timesheet/manager_dashboard.html",
        {
            "tasks": tasks,
            "total_tasks": total_tasks,
            "pending": pending,
            "approved": approved,
            "rejected": rejected,
        }
    )


# =========================
# APPROVE TASK
# =========================

@manager_required
def approve_task(request, task_id):

    task = get_object_or_404(EmployeeTask, id=task_id)
    task.status = "Approved"
    task.save()

    return redirect("manager_dashboard")


# =========================
# REJECT TASK
# =========================

@manager_required
def reject_task(request, task_id):

    task = get_object_or_404(EmployeeTask, id=task_id)
    task.status = "Rejected"
    task.save()

    return redirect("manager_dashboard")
