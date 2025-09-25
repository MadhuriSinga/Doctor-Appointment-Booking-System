"""
URL configuration for doctor_appointment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctor/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('appointment/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('appointment/<int:appointment_id>/update/', views.update_appointment, name='update_appointment'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('accept/<int:appointment_id>/', views.accept_appointment, name='accept_appointment'),
    path('reject/<int:appointment_id>/', views.reject_appointment, name='reject_appointment'),
    path('medical-record/<int:appointment_id>/create/', views.create_medical_record, name='create_medical_record'),
    path('medical-history/', views.patient_medical_history, name='medical_history'),
    path('doctor/availability/', views.doctor_availability, name='doctor_availability'),
    path('doctor/availability/<int:availability_id>/delete/', views.delete_availability, name='delete_availability'),
    path('patient/profile/', views.patient_profile, name='patient_profile'),
    path('doctor/profile/', views.doctor_profile, name='doctor_profile'),
]