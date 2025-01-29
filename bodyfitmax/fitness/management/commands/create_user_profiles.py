from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fitness.models import UserProfile

class Command(BaseCommand):
    help = 'Creates UserProfiles for existing users that do not have one'

    def handle(self, *args, **options):
        users_without_profile = User.objects.filter(userprofile__isnull=True)
        for user in users_without_profile:
            UserProfile.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Created UserProfile for {user.username}'))

        self.stdout.write(self.style.SUCCESS('UserProfile creation complete'))