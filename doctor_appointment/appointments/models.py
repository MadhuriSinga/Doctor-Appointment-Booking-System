from django.db import models
from django.conf import settings
from accounts.models import DoctorProfile
from django.core.exceptions import ValidationError
from datetime import date, time
# Create your models here.

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    notes = models.TextField(blank=True, help_text="Patient notes for the appointment")
    doctor_notes = models.TextField(blank=True, help_text="Doctor's notes after the appointment")
    prescription = models.TextField(blank=True, help_text="Prescription given by doctor")
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['doctor', 'date', 'time']  # Prevent double booking

    def __str__(self):
        return f"Appointment: {self.patient.username} with Dr. {self.doctor.user.get_full_name()} on {self.date} at {self.time}"

    def clean(self):
        """Validate appointment data"""
        if self.date < date.today():
            raise ValidationError("Appointment date cannot be in the past.")
        
        # Check if appointment is within doctor's working hours (9 AM to 6 PM)
        if self.time < time(9, 0) or self.time > time(18, 0):
            raise ValidationError("Appointments can only be scheduled between 9:00 AM and 6:00 PM.")

    @property
    def is_past_appointment(self):
        """Check if appointment is in the past"""
        return self.date < date.today()

    @property
    def can_be_cancelled(self):
        """Check if appointment can be cancelled (not in past and not completed)"""
        return not self.is_past_appointment and self.status not in ['Completed', 'Cancelled']


class MedicalRecord(models.Model):
    """Medical records for patients"""
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='medical_records'
    )
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name='medical_records'
    )
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name='medical_records',
        blank=True,
        null=True
    )
    diagnosis = models.TextField(help_text="Doctor's diagnosis")
    treatment = models.TextField(help_text="Treatment provided")
    prescription = models.TextField(blank=True, help_text="Prescription details")
    notes = models.TextField(blank=True, help_text="Additional notes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Medical Record: {self.patient.username} - {self.created_at.date()}"


class DoctorAvailability(models.Model):
    """Doctor's availability schedule"""
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='availability')
    day_of_week = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['doctor', 'day_of_week']
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.doctor.user.get_full_name()} - {self.day_of_week} {self.start_time}-{self.end_time}"