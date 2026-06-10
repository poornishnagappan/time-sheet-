from django.db import models
from django.contrib.auth.models import User


class EmployeeTask(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    hours = models.FloatField(default=0)
    date = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name


class Profile(models.Model):

    ROLE_CHOICES = (
        ('employee', 'Employee'),
        ('manager', 'Manager'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')

    def __str__(self):
        return self.user.username
