from django.core.management.base import BaseCommand
from accounts.models import DoctorProfile
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Approve a doctor by username or email'

    def add_arguments(self, parser):
        parser.add_argument('identifier', type=str, help='Username or email of the doctor to approve')
        parser.add_argument('--send-email', action='store_true', help='Send approval email to doctor')

    def handle(self, *args, **options):
        identifier = options['identifier']
        send_email = options['send_email']
        
        try:
            # Try to find doctor by username or email
            if '@' in identifier:
                # Search by email
                doctor = DoctorProfile.objects.get(user__email=identifier)
            else:
                # Search by username
                doctor = DoctorProfile.objects.get(user__username=identifier)
            
            if doctor.is_approved:
                self.stdout.write(
                    self.style.WARNING(f'Doctor {doctor.user.username} is already approved.')
                )
                return
            
            # Approve the doctor
            doctor.is_approved = True
            doctor.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully approved doctor: {doctor.user.get_full_name()} ({doctor.user.username})')
            )
            
            # Send approval email if requested
            if send_email:
                try:
                    send_mail(
                        'Doctor Profile Approved',
                        f'Hello Dr. {doctor.user.get_full_name()},\n\nYour doctor profile has been approved! You can now log in and start accepting appointments.\n\nBest regards,\nDocBook Team',
                        settings.DEFAULT_FROM_EMAIL,
                        [doctor.user.email],
                        fail_silently=False,
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f'Approval email sent to {doctor.user.email}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Failed to send email: {e}')
                    )
                    
        except DoctorProfile.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Doctor with identifier "{identifier}" not found.')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {e}')
            )




