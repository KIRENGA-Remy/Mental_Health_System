# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')

    def __str__(self):
        return f"{self.username} ({self.role})"


class Userdata(models.Model):
    firstname= models.CharField(max_length=100, blank=False, null=False)
    lastname= models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(unique=True)
    password= models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.firstname
