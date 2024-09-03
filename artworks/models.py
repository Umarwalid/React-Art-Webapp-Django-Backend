
from django.db import models
class Artwork(models.Model):
    
    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=255) 
    category = models.CharField(max_length=255)  
    description = models.TextField()  
    artist = models.CharField(max_length=255)  
    inspiration = models.TextField()  
    image_url = models.URLField(max_length=200,  null=True) 
    timestamp = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.name  #
