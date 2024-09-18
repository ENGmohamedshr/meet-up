from django.contrib import admin

from .models import Profile, Skills, User

# Register your models here.


admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Skills)