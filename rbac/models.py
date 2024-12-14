from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    ROLE_CHOICES = [
        ('staff', 'Staff'),
        ('supervisor', 'Supervisor'),
        ('admin', 'Admin'),
    ]
    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
    users = models.ManyToManyField(User, related_name='roles')

    def __str__(self):
        return self.name

class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    resource = models.CharField(max_length=100)
    action = models.CharField(max_length=50)
    roles = models.ManyToManyField(Role, related_name='permissions')

    def __str__(self):
        return f"{self.name} ({self.resource}:{self.action})"

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    resource = models.CharField(max_length=100)
    outcome = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
