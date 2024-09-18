
import os
from typing import Any
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.utils.deconstruct import deconstructible

# Create your models here.


class UsersManager(BaseUserManager):
    
    def create_user(self , email , password =None , **extra_fields):
        if not email:
            raise ValueError('the email must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using =self._db)
        return user
    
    def create_superuser(self , email,password = None, **extra_fields):
        extra_fields.setdefault('is_staff' , True)
        extra_fields.setdefault('is_superuser' , True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=250,unique=True)
    email = models.EmailField(unique=True)
    is_banned = models.BooleanField(verbose_name='banned status',default=False)
    is_staff = models.BooleanField(verbose_name='staff status',default=False)
    is_superuser = models.BooleanField(verbose_name='superuser status',default=False)
    last_login = models.DateTimeField(verbose_name='Last Login',blank=True,null=True)
    
    pro_user = models.BooleanField(verbose_name='is_Pro',default=False)
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
    
    def __str__(self) -> str:
        return self.email
    
    

    
@deconstructible
class GenerateProfilePic(object):
    
    def __init__(self) -> None:
        pass
    
    
    def __call__(self, instance , filename) -> Any:
        
        ext = filename.split('.')[-1]
        path = f'media/accounts/{instance.user.id}/images '
        name = f'profile_img.{ext}'
        return os.path.join(path,name)
    
user_profile_img_path = GenerateProfilePic()


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE , related_name='profile')
    first_name = models.CharField(max_length=200 , blank=True)
    last_name = models.CharField(max_length=200 ,blank=True)
    image = models.FileField(upload_to=user_profile_img_path)
    bio = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.user.username}'s profile"
class Skills(models.Model):
    class Skill(models.TextChoices):
        PROGRAMMING = 'programming', 'Programming'
        DATABASE_MANAGEMENT = 'db_management', 'Database Management'
        NETWORKING = 'networking', 'Networking'
        CLOUD_COMPUTING = 'cloud_computing', 'Cloud Computing'
        CYBER_SECURITY = 'cyber_security', 'Cyber Security'
        UI_UX_DESIGN = 'ui_ux_design', 'UI/UX Design'
        GRAPHIC_DESIGN = 'graphic_design', 'Graphic Design'
        WEB_DESIGN = 'web_design', 'Web Design'
        MOTION_GRAPHICS = 'motion_graphics', 'Motion Graphics'
        ILLUSTRATION = 'illustration', 'Illustration'
        MACHINE_LEARNING = 'machine_learning', 'Machine Learning'
        DEEP_LEARNING = 'deep_learning', 'Deep Learning'
        DATA_ANALYSIS = 'data_analysis', 'Data Analysis'
        NATURAL_LANGUAGE_PROCESSING = 'nlp', 'Natural Language Processing'
        COMPUTER_VISION = 'computer_vision', 'Computer Vision'
    
    profile = models.ForeignKey(Profile , on_delete=models.CASCADE ,related_name='skills')
    name = models.CharField(max_length=50 , choices=Skill.choices,null=True , blank=True)
    
    def __str__(self) -> str:
        return f"{self.profile.user.username}'s skills"