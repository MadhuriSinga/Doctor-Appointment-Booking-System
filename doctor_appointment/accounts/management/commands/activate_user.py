from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class Command(BaseCommand):
    help = 'Activate a user account for testing'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to activate')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = CustomUser.objects.get(username=username)
            user.is_active = True
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'User {username} has been activated successfully!')
            )
        except CustomUser.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User {username} does not exist!')
            )




