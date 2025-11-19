from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Rarity, Style, Theme
from .serializers import RaritySerializer, StyleSerializer, ThemeSerializer


class RarityViewSet(viewsets.ModelViewSet):
    queryset = Rarity.objects.all()
    serializer_class = RaritySerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["id", "name"]
    search_fields = ["name"]


class StyleViewSet(viewsets.ModelViewSet):
    queryset = Style.objects.all()
    serializer_class = StyleSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["id", "name", "rarity__id", "rarity__name"]
    search_fields = ["name", "rarity__name"]


class ThemeViewSet(viewsets.ModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["id", "name", "category", "ambiance"]
    search_fields = ["name", "category", "ambiance"]
