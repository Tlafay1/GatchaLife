from rest_framework import viewsets, filters, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend

from .models import GeneratedImage
from .serializers import GeneratedImageSerializer


class GeneratedImageViewSet(viewsets.ModelViewSet):
    queryset = GeneratedImage.objects.all()
    serializer_class = GeneratedImageSerializer
    permission_classes = [permissions.AllowAny]

    parser_classes = (MultiPartParser, FormParser, JSONParser)

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["id"]
    search_fields = ["id"]
