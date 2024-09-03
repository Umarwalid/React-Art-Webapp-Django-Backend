
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   
    path('verify/', views.firebase_login,name='firebase_login'),
]
