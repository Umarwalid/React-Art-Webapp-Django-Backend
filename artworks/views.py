from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from .models import Artwork
from .serializers import ArtworkSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def upload_artwork(request):
    # View to handle artwork metadata upload
    serializer = ArtworkSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # Save the metadata if valid
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_artworks(request):
    # View to retrieve all artworks metadata
    artworks = Artwork.objects.all()
    serializer = ArtworkSerializer(artworks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def latest_artworks(request):
    # View to retrieve all artworks metadata
    artworks = Artwork.objects.all().order_by('-timestamp')[:5]
    serializer = ArtworkSerializer(artworks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def random_artworks(request):
    # View to retrieve 5 random artworks
    artworks = Artwork.objects.all().order_by('?')[:5]
    serializer = ArtworkSerializer(artworks, many=True)
    return Response(serializer.data)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Artwork
from .serializers import ArtworkSerializer
import random

@api_view(['GET'])
@permission_classes([AllowAny])
def random_category(request):
    try:
        # Retrieve all unique categories then take 5 artworks from a random one of them
        categories = Artwork.objects.values_list('category', flat=True).distinct()
        
        if categories:
            random_category = random.choice(categories)
            artworks = Artwork.objects.filter(category=random_category).order_by('?')[:5]
            
            serializer = ArtworkSerializer(artworks, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "No categories found."}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def view_artwork(request,id):
    try:
        artworks = Artwork.objects.get(id=id)
    except Artwork.DoesNotExist:
        return Response({'error:artwork not found'},status=status.HTTP_404_NOT_FOUND)
    serializer = ArtworkSerializer(artworks)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def all_catalogs(request):
    catalogs = Artwork.objects.values_list('category', flat=True).distinct()
    return Response(list(catalogs))

@api_view(['GET'])
@permission_classes([AllowAny])
def view_catalog(request, id):
    try:
        artworks = Artwork.objects.filter(category=id)
        serializer = ArtworkSerializer(artworks, many=True)
        return Response(serializer.data)
    
    except Artwork.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
@permission_classes([AllowAny])
def view_catalog(request, id):
    try:
        artworks = Artwork.objects.filter(category=id)
        serializer = ArtworkSerializer(artworks, many=True)
        return Response(serializer.data)
    
    except Artwork.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)