

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch  import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

from .models import  EmailConfirmationToken, Profile, User

@receiver(post_save , sender = User)
def createUserProfile(sender , instance , created,*args, **kwargs):
    if created:
        Profile.objects.create(user =instance)
        
        
@receiver(post_save , sender = User)
def create_user_token(sender , instance , created , *args, **kwargs):
    if created:
        Token.objects.create(user=instance)
        

@receiver(post_save, sender= User)
def create_verify_email_token(sender , instance , created , *args, **kwargs):
    if created:
        token = EmailConfirmationToken(user= instance)
        
        verfication_link = f"http:localhost:8000/api/accounts/user/verify-email/{token.token}/"
        
        send_mail(
            subject='verify Your email address'.capitalize(),
            message=f'click the link to verify your email : {verfication_link}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email]    
        )
        
        