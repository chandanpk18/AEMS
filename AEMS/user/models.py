from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta


class users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150)
    password = models.TextField(max_length=20)

    def __str__(self):
        return self.username


class HelpRequest(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Resolved', 'Resolved'),
    ]
    username = models.CharField(max_length=100)
    email = models.EmailField()
    help_text = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='New')

    def __str__(self):
        return self.username

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Equipment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    rate = models.IntegerField()
    number = models.IntegerField()
    
    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=150)
    phone_number = models.BigIntegerField()
    address = models.CharField(max_length=100)
    land = models.IntegerField()
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    date = models.DateTimeField()
    

    def __str__(self):
        return f"{self.name} - {self.date}"


