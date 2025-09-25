from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, DoctorProfile, PatientProfile
from django.core.mail import send_mail
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_patient', 'is_doctor', 'is_staff', 'is_active', 'date_joined')
    list_filter = UserAdmin.list_filter + ('is_patient', 'is_doctor')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'location', 'consultation_fee', 'experience_years', 'is_approved', 'created_at')
    list_filter = ('specialty', 'is_approved', 'location', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'specialty', 'location')
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        # Send email notification when doctor is approved
        if change and obj.is_approved and not form.initial.get('is_approved', False):
            send_mail(
                'Doctor Profile Approved',
                f'Hello Dr. {obj.user.get_full_name()}, your profile has been approved. You can now log in.',
                'admin@example.com',
                [obj.user.email]
            )
        super().save_model(request, obj, form, change)


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'gender', 'blood_type', 'phone_number', 'created_at')
    list_filter = ('gender', 'blood_type', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone_number')
    ordering = ('-created_at',)
