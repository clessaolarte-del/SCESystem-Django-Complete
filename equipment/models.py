from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Equipment(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    condition = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    available_quantity = models.IntegerField(default=0)
    image_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    STATUS_CHOICES = [
        ("borrowed", "Borrowed"),
        ("returned", "Returned"),
    ]

    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=200)
    location = models.CharField(max_length=150)
    borrowed_at = models.DateTimeField(default=timezone.now)
    due_at = models.DateTimeField(blank=True, null=True)
    returned_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="borrowed")
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.equipment.name}"
