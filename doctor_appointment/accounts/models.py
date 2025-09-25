from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.



class CustomUser(AbstractUser):
    """Custom user model with role flags"""
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class DoctorProfile(models.Model):
    """Profile for doctors with additional information"""
    SPECIALTY_CHOICES = [
        ('Cardiology', 'Cardiology'),
        ('Dermatology', 'Dermatology'),
        ('Endocrinology', 'Endocrinology'),
        ('Gastroenterology', 'Gastroenterology'),
        ('General Medicine', 'General Medicine'),
        ('Neurology', 'Neurology'),
        ('Oncology', 'Oncology'),
        ('Orthopedics', 'Orthopedics'),
        ('Pediatrics', 'Pediatrics'),
        ('Psychiatry', 'Psychiatry'),
        ('Radiology', 'Radiology'),
        ('Surgery', 'Surgery'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100, choices=SPECIALTY_CHOICES)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=200, help_text="City, State", default="Not specified")
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    experience_years = models.PositiveIntegerField(default=0)
    is_approved = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='doctor_profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialty}"

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username


class PatientProfile(models.Model):
    """Profile for patients with medical information"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=15, blank=True)
    medical_history = models.TextField(blank=True, help_text="Previous medical conditions, surgeries, etc.")
    current_medications = models.TextField(blank=True, help_text="Current medications and dosages")
    allergies = models.TextField(blank=True, help_text="Known allergies")
    profile_picture = models.ImageField(upload_to='patient_profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - Patient Profile"

    @property
    def age(self):
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None


# Signals to auto-create profiles
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_doctor and not hasattr(instance, 'doctorprofile'):
            DoctorProfile.objects.create(user=instance)
        elif instance.is_patient and not hasattr(instance, 'patientprofile'):
            PatientProfile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_doctor and hasattr(instance, 'doctorprofile'):
        instance.doctorprofile.save()
    elif instance.is_patient and hasattr(instance, 'patientprofile'):
        instance.patientprofile.save()
