from django.db.models.signals import post_save
# from django.contrib.auth.models import User
from django.dispatch import receiver

from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # Create a Profile object and associate it with the User
        profile, created = Profile.objects.get_or_create(user=instance)
                
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
        # Save the profile if it exists
    if hasattr(instance, 'profile'):
        instance.profile.save()