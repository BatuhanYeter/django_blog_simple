from django.db.models.signals import post_save 
# this is a signal that fires after an object is saved. We wanna get a post saved signal when a user is created
from django.contrib.auth.models import User
# o yüzden User modelini de yükleriz. User model here is going to be the sender. We need a receiver that gets
# a signal and performs some tasks
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# when a user is saved then send this signal

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


