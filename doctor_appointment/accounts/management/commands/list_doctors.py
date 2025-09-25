from django.core.management.base import BaseCommand
from accounts.models import DoctorProfile

class Command(BaseCommand):
    help = 'List all doctors with their approval status'

    def add_arguments(self, parser):
        parser.add_argument('--pending-only', action='store_true', help='Show only pending doctors')

    def handle(self, *args, **options):
        pending_only = options['pending_only']
        
        if pending_only:
            doctors = DoctorProfile.objects.filter(is_approved=False)
            self.stdout.write(self.style.WARNING('=== PENDING DOCTORS ==='))
        else:
            doctors = DoctorProfile.objects.all()
            self.stdout.write(self.style.SUCCESS('=== ALL DOCTORS ==='))
        
        if not doctors.exists():
            self.stdout.write(self.style.WARNING('No doctors found.'))
            return
        
        self.stdout.write(f"{'Username':<20} {'Name':<25} {'Specialty':<15} {'Status':<10} {'Email'}")
        self.stdout.write('-' * 80)
        
        for doctor in doctors:
            status = 'APPROVED' if doctor.is_approved else 'PENDING'
            status_style = self.style.SUCCESS if doctor.is_approved else self.style.WARNING
            
            self.stdout.write(
                f"{doctor.user.username:<20} "
                f"{doctor.user.get_full_name():<25} "
                f"{doctor.specialty:<15} "
                f"{status_style(status):<10} "
                f"{doctor.user.email}"
            )
        
        self.stdout.write('\nTo approve a doctor, use:')
        self.stdout.write('python manage.py approve_doctor <username_or_email>')
        self.stdout.write('python manage.py approve_doctor <username_or_email> --send-email')




