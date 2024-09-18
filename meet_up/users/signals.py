

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .models import Profile, User

@receiver(post_save , sender = User)
def createUserProfile(sender , instance , created,*args, **kwargs):
    if created:
        Profile.objects.create(user =instance)
        
        
@receiver(post_save , sender = User)
def create_user_token(sender , instance , created , *args, **kwargs):
    if created:
        Token.objects.create(user=instance)
        