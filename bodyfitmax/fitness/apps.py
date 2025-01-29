from django.apps import AppConfig
from django.db.models.signals import post_migrate

class FitnessConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fitness'

    def ready(self):
        from django.contrib.auth.models import User
        from .models import UserProfile

        def create_user_profiles(sender, **kwargs):
            for user in User.objects.all():
                UserProfile.objects.get_or_create(user=user)

        post_migrate.connect(create_user_profiles, sender=self)