from rest_framework import viewsets, status, filters
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Series, Character, CharacterVariant, VariantReferenceImage
from .serializers import (
    SeriesSerializer, 
    CharacterSerializer, 
    CharacterVariantSerializer, 
    VariantReferenceImageSerializer
)

class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer

class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['series']
    search_fields = ['name']

class CharacterVariantViewSet(viewsets.ModelViewSet):
    queryset = CharacterVariant.objects.all()
    serializer_class = CharacterVariantSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['character']

class VariantReferenceImageViewSet(viewsets.ModelViewSet):
    queryset = VariantReferenceImage.objects.all()
    serializer_class = VariantReferenceImageSerializer
    
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['variant']