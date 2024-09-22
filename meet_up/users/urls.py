

from django.urls import path 
from rest_framework.routers import DefaultRouter

from .views import ProfileViewSetApi, UserViewSetApi, VerifyEmailApiView


router =DefaultRouter()
router.register(f'user' , UserViewSetApi ,basename='user')
router.register(f'profile' , ProfileViewSetApi ,basename='user_profile')


urlpatterns =[
    path('user/verify-email/<uuid:token>/',VerifyEmailApiView.as_view() )
]

urlpatterns += router.urls