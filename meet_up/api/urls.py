


from django.urls import include, path


urlpatterns = [
    path('accounts/', include('users.urls')),
    path('events/',include('event.urls'))
]