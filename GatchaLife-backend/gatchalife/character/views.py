import requests
import logging
from django.conf import settings
from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import base64
import mimetypes
from django_filters.rest_framework import DjangoFilterBackend

from .models import Series, Character, CharacterVariant, VariantReferenceImage
from .serializers import (
    SeriesSerializer, 
    CharacterSerializer, 
    CharacterVariantSerializer, 
    VariantReferenceImageSerializer
)

logger = logging.getLogger(__name__)


class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    permission_classes = [permissions.AllowAny]

class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['series']
    search_fields = ['name']

    def perform_create(self, serializer):
        # 1. Sauvegarde initiale du personnage
        character = serializer.save()

        # Automation Trigger: Check for raw wiki text to start processing
        wiki_text = self.request.data.get("wiki_source_text")

        if wiki_text:
            from .services import trigger_character_profiling, update_character_from_ai
            
            ai_data = trigger_character_profiling(character, wiki_text)
            if ai_data:
               update_character_from_ai(character, ai_data)

    @action(detail=True, methods=['post'], url_path='regenerate_from_wiki')
    def regenerate_from_wiki(self, request, pk=None):
        """
        Re-runs the profiling logic on an existing character using the provided character data (wiki text).
        """
        character = self.get_object()
        wiki_text = request.data.get("wiki_source_text", "")
        
        if not wiki_text:
             return Response(
                {"error": "Wiki source text is required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        from .services import trigger_character_profiling, update_character_from_ai
        
        ai_data = trigger_character_profiling(character, wiki_text)
        
        if ai_data:
            update_character_from_ai(character, ai_data)
            serializer = self.get_serializer(character)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "Failed to regenerate character data from AI."}, 
                status=status.HTTP_502_BAD_GATEWAY
            )

    @action(detail=True, methods=['post'], url_path='create-variants')
    def create_variants(self, request, pk=None):
        character = self.get_object()
        
        n8n_path = getattr(settings, "N8N_CREATE_VARIANTS_WEBHOOK_URL", None)
        base_url = getattr(settings, "N8N_BASE_URL", None)
        webhook_path = getattr(settings, "N8N_WORKFLOW_WEBHOOK_PATH", "webhook")
        
        if not (n8n_path and base_url):
            return Response(
                {"error": "N8N configuration missing"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
        webhook_url = f"{base_url}/{webhook_path}/{n8n_path}"
        
        # Prepare Payload
        try:
            payload = {
                "character_id": character.id,
                "name": character.name,
                "lore_tags": character.lore_tags, # Will be sent as string if multipart, n8n might need parsing
                "body_type": character.body_type_description,
                "appearance": character.description, 
                "series": character.series.name if character.series else "Unknown",
                "user_prompt": request.data.get("prompt", "") 
            }
            
            # Prepare Files (Binary)
            files = {}
            if character.identity_face_image:
                 try:
                    character.identity_face_image.open("rb")
                    files["identity_face_image"] = (
                        character.identity_face_image.name,
                        character.identity_face_image,
                        "application/octet-stream", # Or guess mime type
                    )
                 except Exception as e:
                     logger.error(f"Failed to open face image for binary upload: {e}")

            # Send to n8n
            # We use a longer timeout as generating ideas might take a moment.
            # Using data=payload + files=files automagically sends multipart/form-data
            if files:
                response = requests.post(webhook_url, data=payload, files=files, timeout=60)
            else:
                response = requests.post(webhook_url, json=payload, timeout=60)
            
            if response.status_code == 200:
                try:
                    # Check if content is empty
                    if not response.content:
                         raise ValueError("Received empty response from N8N")
                         
                    data = response.json()
                except ValueError as json_err:
                     logger.error(f"Invalid JSON from N8N: {response.text}")
                     return Response(
                        {"error": f"N8N returned invalid JSON: {str(json_err)}"}, 
                        status=status.HTTP_502_BAD_GATEWAY
                    )

                from .services import update_variants_from_ai
                created_variants = update_variants_from_ai(character, data)
                
                return Response({
                    "message": f"Successfully created {len(created_variants)} variants.",
                    "variants": [v.name for v in created_variants]
                })
            else:
                 return Response(
                    {"error": f"N8N Error: {response.text}"}, 
                    status=status.HTTP_502_BAD_GATEWAY
                )

        except Exception as e:
            logger.exception("Error in create_variants") # Log full traceback
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CharacterVariantViewSet(viewsets.ModelViewSet):
    queryset = CharacterVariant.objects.all()
    serializer_class = CharacterVariantSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['character']

class VariantReferenceImageViewSet(viewsets.ModelViewSet):
    queryset = VariantReferenceImage.objects.all()
    serializer_class = VariantReferenceImageSerializer
    permission_classes = [permissions.AllowAny]
    
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['variant']