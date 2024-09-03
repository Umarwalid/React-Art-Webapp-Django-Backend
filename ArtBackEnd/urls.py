
from django.contrib import admin
from .views import *
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('artworks/', include('artworks.urls')),
    path('mail/',include('mail.urls')),
    path('health/', health_check, name='health_check'),
]
