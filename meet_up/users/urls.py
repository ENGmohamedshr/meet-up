

from rest_framework.routers import DefaultRouter

from .views import ProfileViewSetApi, UserViewSetApi


router =DefaultRouter()
router.register(f'user' , UserViewSetApi ,basename='user')
router.register(f'profile' , ProfileViewSetApi ,basename='user_profile')


urlpatterns = router.urls