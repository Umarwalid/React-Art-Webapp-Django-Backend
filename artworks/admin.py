

from django.contrib import admin
from .models import Artwork

class ArtworkAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
   

admin.site.register(Artwork, ArtworkAdmin)
