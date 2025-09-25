from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Appointment, MedicalRecord, DoctorAvailability
from .forms import (AppointmentForm, DoctorAppointmentForm, MedicalRecordForm, 
                   DoctorSearchForm, DoctorAvailabilityForm)
from accounts.models import DoctorProfile, PatientProfile
from datetime import date, datetime, timedelta
import json

# Create your views here.

def home(request):
    """Home page view"""
    return render(request, 'home.html')
@login_required
def doctor_list(request):
    """Enhanced doctor list with filtering and search capabilities"""
    doctors = DoctorProfile.objects.filter(is_approved=True).order_by('-created_at')
    search_form = DoctorSearchForm(request.GET)
    
    if search_form.is_valid():
        specialty = search_form.cleaned_data.get('specialty')
        location = search_form.cleaned_data.get('location')
        min_experience = search_form.cleaned_data.get('min_experience')
        max_fee = search_form.cleaned_data.get('max_fee')
        
        if specialty:
            doctors = doctors.filter(specialty=specialty)
        if location:
            doctors = doctors.filter(location__icontains=location)
        if min_experience:
            doctors = doctors.filter(experience_years__gte=min_experience)
        if max_fee:
            doctors = doctors.filter(consultation_fee__lte=max_fee)
    
    # Pagination
    paginator = Paginator(doctors, 6)
    page_number = request.GET.get('page')
    doctors = paginator.get_page(page_number)
    
    return render(request, 'appointments/doctor_list.html', {
        'doctors': doctors,
        'search_form': search_form,
        'specialties': DoctorProfile.SPECIALTY_CHOICES
    })


@login_required
def doctor_detail(request, doctor_id):
    """Detailed view of a doctor's profile"""
    doctor = get_object_or_404(DoctorProfile, id=doctor_id, is_approved=True)
    availability = DoctorAvailability.objects.filter(doctor=doctor, is_available=True)
    
    return render(request, 'appointments/doctor_detail.html', {
        'doctor': doctor,
        'availability': availability
    })


@login_required
def book_appointment(request, doctor_id):
    """Enhanced appointment booking with validation"""
    if not request.user.is_patient:
        messages.error(request, 'Only patients can book appointments.')
        return redirect('home')

    doctor = get_object_or_404(DoctorProfile, id=doctor_id, is_approved=True)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            try:
                appt = form.save(commit=False)
                appt.patient = request.user
                appt.doctor = doctor
                appt.status = 'Pending'
                appt.save()

                # Send notification emails
                send_mail(
                    'Appointment Booked',
                    f'Your appointment with Dr. {doctor.user.get_full_name()} on {appt.date} at {appt.time} is booked (Status: {appt.status}).',
                    'admin@example.com',
                    [request.user.email]
                )
                send_mail(
                    'New Appointment Scheduled',
                    f'Patient {request.user.get_full_name()} booked an appointment on {appt.date} at {appt.time}.',
                    'admin@example.com',
                    [doctor.user.email]
                )

                messages.success(request, 'Appointment booked successfully!')
                return redirect('patient_dashboard')
            except IntegrityError:
                messages.error(request, 'This time slot is already booked. Please choose another time.')
    else:
        form = AppointmentForm()

    return render(request, 'appointments/book_appointment.html', {'form': form, 'doctor': doctor})


@login_required
def patient_dashboard(request):
    """Enhanced patient dashboard with filtering and medical history"""
    if not request.user.is_patient:
        return redirect('doctor_dashboard')

    appointments = request.user.appointments.all()
    medical_records = MedicalRecord.objects.filter(patient=request.user)
    
    # Filter appointments by status
    status_filter = request.GET.get('status')
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    # Calculate statistics
    total_appointments = appointments.count()
    pending_appointments = appointments.filter(status='Pending').count()
    confirmed_appointments = appointments.filter(status='Confirmed').count()
    completed_appointments = appointments.filter(status='Completed').count()
    cancelled_appointments = appointments.filter(status='Cancelled').count()
    
    # Pagination
    paginator = Paginator(appointments, 10)
    page_number = request.GET.get('page')
    appointments = paginator.get_page(page_number)
    
    return render(request, 'appointments/patient_dashboard.html', {
        'appointments': appointments,
        'medical_records': medical_records,
        'status_choices': Appointment.STATUS_CHOICES,
        'stats': {
            'total': total_appointments,
            'pending': pending_appointments,
            'confirmed': confirmed_appointments,
            'completed': completed_appointments,
            'cancelled': cancelled_appointments,
        }
    })


@login_required
def doctor_dashboard(request):
    """Enhanced doctor dashboard with appointment management"""
    if not request.user.is_doctor:
        return redirect('patient_dashboard')

    doctor_profile = request.user.doctorprofile
    appointments = Appointment.objects.filter(doctor=doctor_profile)
    
    # Filter appointments by status
    status_filter = request.GET.get('status')
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    # Get doctor's availability
    availability = DoctorAvailability.objects.filter(doctor=doctor_profile, is_available=True)
    
    # Pagination
    paginator = Paginator(appointments, 10)
    page_number = request.GET.get('page')
    appointments = paginator.get_page(page_number)
    
    # Statistics - use the original queryset for accurate counts
    all_appointments = Appointment.objects.filter(doctor=doctor_profile)
    total_appointments = all_appointments.count()
    pending_appointments = all_appointments.filter(status='Pending').count()
    confirmed_appointments = all_appointments.filter(status='Confirmed').count()
    completed_appointments = all_appointments.filter(status='Completed').count()
    cancelled_appointments = all_appointments.filter(status='Cancelled').count()
    
    return render(request, 'appointments/doctor_dashboard.html', {
        'appointments': appointments,
        'doctor_profile': doctor_profile,
        'availability': availability,
        'status_choices': Appointment.STATUS_CHOICES,
        'today': date.today(),
        'stats': {
            'total': total_appointments,
            'pending': pending_appointments,
            'confirmed': confirmed_appointments,
            'completed': completed_appointments,
            'cancelled': cancelled_appointments,
        }
    })


@login_required
def appointment_detail(request, appointment_id):
    """Detailed view of an appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check if user has permission to view this appointment
    if not (request.user == appointment.patient or request.user == appointment.doctor.user):
        messages.error(request, 'You are not authorized to view this appointment.')
        return redirect('home')
    
    medical_records = MedicalRecord.objects.filter(appointment=appointment)
    
    return render(request, 'appointments/appointment_detail.html', {
        'appointment': appointment,
        'medical_records': medical_records
    })


@login_required
def update_appointment(request, appointment_id):
    """Update appointment details (for doctors)"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if not request.user.is_doctor or request.user != appointment.doctor.user:
        messages.error(request, 'You are not authorized to update this appointment.')
        return redirect('home')
    
    if request.method == 'POST':
        form = DoctorAppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment updated successfully.')
            return redirect('appointment_detail', appointment_id=appointment.id)
    else:
        form = DoctorAppointmentForm(instance=appointment)
    
    return render(request, 'appointments/update_appointment.html', {
        'form': form,
        'appointment': appointment
    })


@login_required
def cancel_appointment(request, appointment_id):
    """Cancel an appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Check if user can cancel this appointment
    if request.user == appointment.patient or request.user == appointment.doctor.user:
        if appointment.can_be_cancelled:
            appointment.status = 'Cancelled'
            appointment.save()
            messages.success(request, 'Appointment cancelled successfully.')
        else:
            messages.error(request, 'This appointment cannot be cancelled.')
    else:
        messages.error(request, 'You are not authorized to cancel this appointment.')

    if request.user.is_patient:
        return redirect('patient_dashboard')
    else:
        return redirect('doctor_dashboard')


@login_required
def accept_appointment(request, appointment_id):
    """Accept an appointment (doctor only)"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if not request.user.is_doctor or request.user != appointment.doctor.user:
        messages.error(request, 'You are not authorized to accept this appointment.')
        return redirect('home')
    
    if appointment.status == 'Pending':
        appointment.status = 'Confirmed'
        appointment.save()
        
        # Send notification email to patient
        try:
            send_mail(
                'Appointment Confirmed',
                f'Your appointment with Dr. {appointment.doctor.user.get_full_name()} on {appointment.date} at {appointment.time} has been confirmed.',
                'admin@example.com',
                [appointment.patient.email]
            )
        except Exception as e:
            print(f"Email sending failed: {e}")
        
        messages.success(request, 'Appointment accepted and patient notified.')
    else:
        messages.error(request, 'This appointment cannot be accepted.')
    
    return redirect('doctor_dashboard')


@login_required
def reject_appointment(request, appointment_id):
    """Reject an appointment (doctor only)"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if not request.user.is_doctor or request.user != appointment.doctor.user:
        messages.error(request, 'You are not authorized to reject this appointment.')
        return redirect('home')
    
    if appointment.status == 'Pending':
        appointment.status = 'Cancelled'
        appointment.save()
        
        # Send notification email to patient
        try:
            send_mail(
                'Appointment Rejected',
                f'Your appointment with Dr. {appointment.doctor.user.get_full_name()} on {appointment.date} at {appointment.time} has been rejected. Please book another time slot.',
                'admin@example.com',
                [appointment.patient.email]
            )
        except Exception as e:
            print(f"Email sending failed: {e}")
        
        messages.success(request, 'Appointment rejected and patient notified.')
    else:
        messages.error(request, 'This appointment cannot be rejected.')
    
    return redirect('doctor_dashboard')


@login_required
def create_medical_record(request, appointment_id):
    """Create medical record for an appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if not request.user.is_doctor or request.user != appointment.doctor.user:
        messages.error(request, 'You are not authorized to create medical records for this appointment.')
        return redirect('home')
    
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            medical_record = form.save(commit=False)
            medical_record.patient = appointment.patient
            medical_record.doctor = appointment.doctor
            medical_record.appointment = appointment
            medical_record.save()
            
            # Update appointment status to completed
            appointment.status = 'Completed'
            appointment.save()
            
            messages.success(request, 'Medical record created successfully.')
            return redirect('appointment_detail', appointment_id=appointment.id)
    else:
        form = MedicalRecordForm()
    
    return render(request, 'appointments/create_medical_record.html', {
        'form': form,
        'appointment': appointment
    })


@login_required
def patient_medical_history(request):
    """View patient's complete medical history"""
    if not request.user.is_patient:
        messages.error(request, 'Only patients can view medical history.')
        return redirect('home')
    
    medical_records = MedicalRecord.objects.filter(patient=request.user)
    
    # Pagination
    paginator = Paginator(medical_records, 10)
    page_number = request.GET.get('page')
    medical_records = paginator.get_page(page_number)
    
    return render(request, 'appointments/medical_history.html', {
        'medical_records': medical_records
    })


@login_required
def doctor_availability(request):
    """Manage doctor's availability schedule"""
    if not request.user.is_doctor:
        messages.error(request, 'Only doctors can manage availability.')
        return redirect('home')
    
    doctor_profile = request.user.doctorprofile
    availability = DoctorAvailability.objects.filter(doctor=doctor_profile)
    
    if request.method == 'POST':
        form = DoctorAvailabilityForm(request.POST)
        if form.is_valid():
            availability_obj = form.save(commit=False)
            availability_obj.doctor = doctor_profile
            availability_obj.save()
            messages.success(request, 'Availability updated successfully.')
            return redirect('doctor_availability')
    else:
        form = DoctorAvailabilityForm()
    
    return render(request, 'appointments/doctor_availability.html', {
        'form': form,
        'availability': availability
    })


@login_required
def delete_availability(request, availability_id):
    """Delete doctor availability"""
    availability = get_object_or_404(DoctorAvailability, id=availability_id)
    
    if request.user != availability.doctor.user:
        messages.error(request, 'You are not authorized to delete this availability.')
        return redirect('doctor_availability')
    
    availability.delete()
    messages.success(request, 'Availability deleted successfully.')
    return redirect('doctor_availability')


@login_required
def patient_profile(request):
    """View and edit patient profile"""
    if not request.user.is_patient:
        messages.error(request, 'Only patients can access this page.')
        return redirect('home')
    
    patient_profile, created = PatientProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        from accounts.forms import PatientProfileForm
        form = PatientProfileForm(request.POST, request.FILES, instance=patient_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('patient_profile')
    else:
        from accounts.forms import PatientProfileForm
        form = PatientProfileForm(instance=patient_profile)
    
    return render(request, 'appointments/patient_profile.html', {
        'form': form,
        'patient_profile': patient_profile
    })


@login_required
def doctor_profile(request):
    """View and edit doctor profile"""
    if not request.user.is_doctor:
        messages.error(request, 'Only doctors can access this page.')
        return redirect('home')
    
    doctor_profile = request.user.doctorprofile
    
    if request.method == 'POST':
        from accounts.forms import DoctorProfileForm
        form = DoctorProfileForm(request.POST, request.FILES, instance=doctor_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('doctor_profile')
    else:
        from accounts.forms import DoctorProfileForm
        form = DoctorProfileForm(instance=doctor_profile)
    
    return render(request, 'appointments/doctor_profile.html', {
        'form': form,
        'doctor_profile': doctor_profile
    })
