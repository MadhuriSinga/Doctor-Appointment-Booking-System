from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class Command(BaseCommand):
    help = 'List all users and their activation status'

    def handle(self, *args, **options):
        users = CustomUser.objects.all().order_by('-date_joined')
        
        if not users:
            self.stdout.write(self.style.WARNING('No users found.'))
            return
        
        self.stdout.write(self.style.SUCCESS('User List:'))
        self.stdout.write('=' * 80)
        
        for user in users:
            status = "Active" if user.is_active else "Inactive"
            role = "Patient" if user.is_patient else "Doctor" if user.is_doctor else "Unknown"
            
            self.stdout.write(f"Username: {user.username}")
            self.stdout.write(f"Email: {user.email}")
            self.stdout.write(f"Name: {user.get_full_name()}")
            self.stdout.write(f"Role: {role}")
            self.stdout.write(f"Status: {status}")
            self.stdout.write(f"Joined: {user.date_joined}")
            self.stdout.write('-' * 40)




