

from rest_framework.routers import DefaultRouter

from .views import EventViewSetApi


router = DefaultRouter()
router.register(r'',EventViewSetApi , basename='events')

urlpatterns = router.urls