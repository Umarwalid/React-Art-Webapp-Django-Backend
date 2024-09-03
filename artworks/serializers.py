from rest_framework import serializers
from .models import Artwork

# Serializer to convert Artwork model instances to JSON
class ArtworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artwork
        fields = '__all__'  # Include all fields of the Artwork model
