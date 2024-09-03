from django.urls import path
from . import views

from django.contrib import admin


urlpatterns=[
    path('sendC/',views.send_comission,name='send_comission'),
]