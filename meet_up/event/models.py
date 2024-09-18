
from ast import mod
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import module_loading

from users.models import User
# Create your models here.

class PlaceGovernrate(models.TextChoices):
    CAIRO = 'cairo', 'Cairo'
    ALEXANDRIA = 'alexandria', 'Alexandria'
    GIZA = 'giza', 'Giza'
    SUEZ = 'suez', 'Suez'
    DAKAHLIA = 'dakahlia', 'Dakahlia'
    DAMIETTA = 'damietta', 'Damietta'
    FAIYUM = 'faiyum', 'Faiyum'
    GHARBIA = 'gharbia', 'Gharbia'
    ISMAILIA = 'ismailia', 'Ismailia'
    KAFR_EL_SHEIKH = 'kafr_el_sheikh', 'Kafr El Sheikh'
    MINYA = 'minya', 'Minya'
    MONUFIA = 'monufia', 'Monufia'
    QALYUBIA = 'qalyubia', 'Qalyubia'
    QENA = 'qena', 'Qena'
    SHARQIA = 'sharqia', 'Sharqia'
    ASYUT = 'asyut', 'Asyut'
    ASWAN = 'aswan', 'Aswan'
    BENI_SUEF = 'beni_suef', 'Beni Suef'
    PORT_SAID = 'port_said', 'Port Said'
    RED_SEA = 'red_sea', 'Red Sea'
    SOHAG = 'sohag', 'Sohag'
    SOUTH_SINAI = 'south_sinai', 'South Sinai'
    NEW_VALLEY = 'new_valley', 'New Valley'
    MATRUH = 'matruh', 'Matruh'
    NORTH_SINAI = 'north_sinai', 'North Sinai'
    BEHEIRA = 'beheira', 'Beheira'

class Place(models.Model):
    
    name = models.CharField(max_length=250)
    desc = models.TextField()
    governrate = models.CharField(max_length=250 , choices=PlaceGovernrate.choices,)
    # lat = models.CharField()
    
    
    def __str__(self) -> str:
        return self.name
class Category(models.Model):
    class CategoryName(models.TextChoices):
        DESIGN ='design','Design'
        PROGRAMMING = 'programming','Programming'
        ENGLISH = 'english','English'
        
    
    name = models.CharField(max_length=150 , choices=CategoryName.choices)
    
    def __str__(self) -> str:
        return self.name

class Event(models.Model):
    created_by = models.ForeignKey(User , on_delete=models.CASCADE)
    topic = models.CharField(max_length=250)
    num_of_members = models.DecimalField(max_digits=10,decimal_places=0,
                                         validators=[MinValueValidator(3) ],default=3 )
    
    category = models.ForeignKey(Category, on_delete=models.PROTECT , null =True )
    
    place = models.ForeignKey(Place , on_delete=models.PROTECT )
    
    time = models.DateTimeField()
    
    is_active = models.BooleanField(verbose_name='active',default=True)
    
    def member_count(self):
        return self.members.count()
        
    
    def __str__(self) -> str:
        return self.topic
    

class Member(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    event = models.ForeignKey(Event , on_delete=models.CASCADE , related_name='members')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user','event'],name='user_event_unique')
        ]
    
    def __str__(self) -> str:
        return f'{self.user.email} in event {self.event.topic}'