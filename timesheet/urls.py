from django.urls import path
from . import views

urlpatterns = [

    # ======================
    # EMPLOYEE URLs
    # ======================
    path(
        "login/",
        views.employee_login,
        name="employee_login"
    ),

    path(
        "dashboard/",
        views.employee_dashboard,
        name="employee_dashboard"
    ),

    path(
        "add-task/",
        views.add_task,
        name="add_task"
    ),

    path(
        "logout/",
        views.employee_logout,
        name="employee_logout"
    ),

    # ======================
    # MANAGER URLs
    # ======================

    path(
        "manager-login/",
        views.manager_login,
        name="manager_login"
    ),

    path(
        "manager-dashboard/",
        views.manager_dashboard,
        name="manager_dashboard"
    ),

    path(
        "approve-task/<int:task_id>/",
        views.approve_task,
        name="approve_task"
    ),

    path(
        "reject-task/<int:task_id>/",
        views.reject_task,
        name="reject_task"
    ),

]
