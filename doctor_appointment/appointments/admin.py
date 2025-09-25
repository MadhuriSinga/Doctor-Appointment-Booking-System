from django.contrib import admin
from .models import Appointment, MedicalRecord, DoctorAvailability

# Register your models here.
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'status', 'follow_up_required', 'created_at')
    list_filter = ('status', 'date', 'doctor__specialty', 'follow_up_required')
    search_fields = ('patient__username', 'doctor__user__username', 'notes')
    date_hierarchy = 'date'
    readonly_fields = ('created_at', 'updated_at')

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment', 'diagnosis', 'created_at')
    list_filter = ('created_at', 'doctor__specialty')
    search_fields = ('patient__username', 'doctor__user__username', 'diagnosis')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)

@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'day_of_week', 'start_time', 'end_time', 'is_available')
    list_filter = ('day_of_week', 'is_available', 'doctor__specialty')
    search_fields = ('doctor__user__username', 'doctor__specialty')
    ordering = ('doctor', 'day_of_week', 'start_time')
