from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import DoctorProfile, PatientProfile

CustomUser = get_user_model()


class PatientSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_patient = True
        user.is_active = False  # Deactivate until email confirmed
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Update patient profile with additional data
            if hasattr(user, 'patientprofile'):
                user.patientprofile.phone_number = self.cleaned_data.get('phone_number', '')
                user.patientprofile.date_of_birth = self.cleaned_data.get('date_of_birth')
                user.patientprofile.save()
        return user


class DoctorSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    specialty = forms.ChoiceField(choices=DoctorProfile.SPECIALTY_CHOICES, required=True)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    location = forms.CharField(max_length=200, required=True, help_text="City, State")
    consultation_fee = forms.DecimalField(max_digits=10, decimal_places=2, required=True, min_value=0)
    experience_years = forms.IntegerField(required=True, min_value=0, max_value=50)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'specialty', 'bio', 'location', 'consultation_fee', 'experience_years']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_doctor = True
        user.is_active = False  # Deactivate until email confirmed
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Update doctor profile with additional data
            if hasattr(user, 'doctorprofile'):
                user.doctorprofile.specialty = self.cleaned_data['specialty']
                user.doctorprofile.bio = self.cleaned_data['bio']
                user.doctorprofile.location = self.cleaned_data['location']
                user.doctorprofile.consultation_fee = self.cleaned_data['consultation_fee']
                user.doctorprofile.experience_years = self.cleaned_data['experience_years']
                user.doctorprofile.save()
        return user


class PatientProfileForm(forms.ModelForm):
    """Form for updating patient profile information"""
    class Meta:
        model = PatientProfile
        fields = ['date_of_birth', 'gender', 'blood_type', 'phone_number', 'address', 
                 'emergency_contact', 'emergency_phone', 'medical_history', 
                 'current_medications', 'allergies', 'profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'blood_type': forms.Select(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'medical_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'current_medications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'allergies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }


class DoctorProfileForm(forms.ModelForm):
    """Form for updating doctor profile information"""
    class Meta:
        model = DoctorProfile
        fields = ['specialty', 'bio', 'location', 'consultation_fee', 'experience_years', 'profile_picture']
        widgets = {
            'specialty': forms.Select(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }