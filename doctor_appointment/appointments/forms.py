from django import forms
from .models import Appointment, MedicalRecord, DoctorAvailability
from accounts.models import DoctorProfile
from django.core.exceptions import ValidationError
from datetime import date, time
import datetime


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any specific concerns or symptoms you\'d like to discuss...'}),
        }

    def clean_date(self):
        appointment_date = self.cleaned_data['date']
        if appointment_date < date.today():
            raise ValidationError("Appointment date cannot be in the past.")
        return appointment_date

    def clean_time(self):
        appointment_time = self.cleaned_data['time']
        if appointment_time < time(9, 0) or appointment_time > time(18, 0):
            raise ValidationError("Appointments can only be scheduled between 9:00 AM and 6:00 PM.")
        return appointment_time


class DoctorAppointmentForm(forms.ModelForm):
    """Form for doctors to update appointment details"""
    class Meta:
        model = Appointment
        fields = ['status', 'doctor_notes', 'prescription', 'follow_up_required', 'follow_up_date']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'doctor_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Doctor\'s notes and observations...'}),
            'prescription': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Prescription details...'}),
            'follow_up_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'follow_up_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean_follow_up_date(self):
        follow_up_date = self.cleaned_data.get('follow_up_date')
        follow_up_required = self.cleaned_data.get('follow_up_required', False)
        
        if follow_up_required and not follow_up_date:
            raise ValidationError("Follow-up date is required when follow-up is needed.")
        
        if follow_up_date and follow_up_date <= date.today():
            raise ValidationError("Follow-up date must be in the future.")
        
        return follow_up_date


class MedicalRecordForm(forms.ModelForm):
    """Form for creating medical records"""
    class Meta:
        model = MedicalRecord
        fields = ['diagnosis', 'treatment', 'prescription', 'notes']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter diagnosis...'}),
            'treatment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Treatment provided...'}),
            'prescription': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Prescription details...'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional notes...'}),
        }


class DoctorSearchForm(forms.Form):
    """Form for filtering doctors"""
    specialty = forms.ChoiceField(
        choices=[('', 'All Specialties')] + DoctorProfile.SPECIALTY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    location = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city or state...'})
    )
    min_experience = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min years of experience'})
    )
    max_fee = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max consultation fee', 'step': '0.01'})
    )


class DoctorAvailabilityForm(forms.ModelForm):
    """Form for setting doctor availability"""
    class Meta:
        model = DoctorAvailability
        fields = ['day_of_week', 'start_time', 'end_time', 'is_available']
        widgets = {
            'day_of_week': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time and start_time >= end_time:
            raise ValidationError("End time must be after start time.")
        
        return cleaned_data
