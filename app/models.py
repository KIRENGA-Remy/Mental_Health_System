from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]
    
    username = None  
    email = models.EmailField(unique=True)  
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role', username]  

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"


class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    symptoms = models.TextField(blank=True, null=True)  # Optional field for patient symptoms

    def __str__(self):
        return f"Patient: {self.user.first_name} {self.user.last_name}"


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

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    specialization = models.CharField(max_length=100, choices=SPECIALIZATION_CHOICES)
    experience = models.PositiveIntegerField(help_text="Experience in years")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    image = models.ImageField(upload_to='doctor_images/', blank=True, null=True)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} - {self.specialization}"


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed')],
        default='Pending'
    )
    notes = models.TextField(blank=True, null=True)  # Optional field for additional details

    def __str__(self):
        return f"Appointment on {self.date} with Dr. {self.doctor.user.last_name} and {self.patient.user.last_name}"
