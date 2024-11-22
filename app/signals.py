from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DoctorModel

@receiver(post_save, sender=DoctorModel)
def notify_doctor_created(sender, instance, created, **kwargs):
    if created:
        print(f"A new doctor, Dr. {instance.user.first_name} {instance.user.last_name}, has been added.")
