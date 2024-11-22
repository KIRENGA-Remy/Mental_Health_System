from django.db import models
from django.conf import settings
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
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']  

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

class PatientModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    symptoms = models.TextField(blank=True, null=True) 

    def __str__(self):
        return f"Patient: {self.user.first_name} {self.user.last_name}"

class DoctorModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    specialization = models.CharField(max_length=100, choices=[
        ('eyes', 'Eyes Specialist'),
        ('headache', 'Headache Specialist'),
        ('injury', 'Injury Specialist'),
    ])
    available = models.BooleanField(default=True)
    location = models.CharField(max_length=50)
    working_hours = models.CharField(max_length=100, blank=True, null=True) 

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} - {self.specialization}"

class PatientRecord(models.Model):
    patient = models.ForeignKey(PatientModel, on_delete=models.CASCADE, related_name="records")
    doctor = models.ForeignKey(DoctorModel, on_delete=models.CASCADE, related_name="patients")
    notes = models.TextField()
    prescription = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Record for {self.patient.user.first_name} by {self.doctor.user.last_name}"
    
class Appointment(models.Model):
    patient = models.ForeignKey(PatientModel, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(DoctorModel, on_delete=models.CASCADE, related_name="appointments")
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )
    notes = models.TextField(blank=True, null=True)  # Optional field for additional details

    def __str__(self):
        return f"Appointment on {self.date} with Dr. {self.doctor.user.last_name} and {self.patient.user.last_name}"


class HealthRecord(models.Model):
    patient = models.ForeignKey(PatientModel, on_delete=models.CASCADE, related_name="health_records")
    doctor = models.ForeignKey(DoctorModel, on_delete=models.CASCADE)
    notes = models.TextField()
    prescription = models.TextField()

    def __str__(self):
        return f"Health Record for {self.patient.user.first_name} {self.patient.user.last_name} by Dr. {self.doctor.user.last_name}"

class Advice(models.Model):
    patient = models.ForeignKey(PatientModel, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorModel, on_delete=models.CASCADE)
    advice_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class MedicineRecommendation(models.Model):
    patient = models.ForeignKey(PatientModel, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorModel, on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)
    recommended_at = models.DateTimeField(auto_now_add=True)
