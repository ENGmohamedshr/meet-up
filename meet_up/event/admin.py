from django.contrib import admin

from .models import Member, Place,Category,Event
# Register your models here.

admin.site.register(Place)
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Member)