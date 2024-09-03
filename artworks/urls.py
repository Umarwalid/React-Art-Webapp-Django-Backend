
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   
    path('upload/', views.upload_artwork,name='Upload'),
    path('list/', views.list_artworks,name='list'),
    path('latest/', views.latest_artworks,name='latest'),
    path('view/<int:id>/',views.view_artwork,name='view'),
    path('catalogs/',views.all_catalogs,name='catalogs'),
    path('catalogs/<str:id>/',views.view_catalog,name='view_catalog'),
    path('listRC/',views.random_category,name='random_category'),
    path('listRA/',views. random_artworks,name=' random_artworks'),
]
 