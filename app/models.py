from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')


class Userdata(models.Model):
    firstname= models.CharField(max_length=100, blank=False, null=False)
    lastname= models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(unique=True)
    password= models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.firstname
    
class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    symptoms = models.TextField()  # How the patient is feeling


class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        ('eyes', 'Eyes Specialist'),
        ('headache', 'Headache Specialist'),
        ('injury', 'Injury Specialist'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100) 
    specialization = models.CharField(max_length=100, choices=SPECIALIZATION_CHOICES)
    experience = models.PositiveIntegerField(help_text="Experience in years")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    image = models.ImageField(upload_to='doctor_images/', blank=True, null=True)  

    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed')], default='Pending')
    notes = models.TextField(null=True, blank=True)  # Medicine details
