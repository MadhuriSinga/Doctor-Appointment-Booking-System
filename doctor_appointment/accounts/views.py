from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.contrib import messages
from .forms import PatientSignUpForm, DoctorSignUpForm
from .models import CustomUser

# Create your views here.
def register_patient(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Send activation email
            current_site = get_current_site(request)
            subject = 'Activate Your Patient Account'
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_mail(subject, message, 'admin@example.com', [user.email], html_message=message)
            
            # For development, show activation link in console and message
            activation_url = f"http://127.0.0.1:8000/accounts/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/{default_token_generator.make_token(user)}/"
            print(f"\n=== ACTIVATION LINK FOR {user.username} ===")
            print(f"Email: {user.email}")
            print(f"Activation URL: {activation_url}")
            print("=====================================\n")
            
            messages.success(request, f'Patient account created! Please click this activation link: {activation_url}')
            return redirect('login')
    else:
        form = PatientSignUpForm()
    return render(request, 'accounts/register_patient.html', {'form': form})


def register_doctor(request):
    if request.method == 'POST':
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Send activation email
            current_site = get_current_site(request)
            subject = 'Activate Your Doctor Account'
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_mail(subject, message, 'admin@example.com', [user.email], html_message=message)
            
            # For development, show activation link in console and message
            activation_url = f"http://127.0.0.1:8000/accounts/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/{default_token_generator.make_token(user)}/"
            print(f"\n=== ACTIVATION LINK FOR {user.username} ===")
            print(f"Email: {user.email}")
            print(f"Activation URL: {activation_url}")
            print("=====================================\n")
            
            messages.success(request, f'Doctor account created! Please click this activation link: {activation_url}')
            return redirect('login')
    else:
        form = DoctorSignUpForm()
    return render(request, 'accounts/register_doctor.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated. You can now log in.')
        return redirect('login')
    else:
        return render(request, 'accounts/activation_invalid.html')


def custom_logout(request):
    """Custom logout view that accepts GET requests"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')