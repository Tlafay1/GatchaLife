import requests
import logging
from django.conf import settings
from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from django.urls import reverse

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
            from .services import trigger_character_profiling

            # Trigger async job (fire and forget)
            callback_url = self.request.build_absolute_uri(reverse("n8n-callback"))
            trigger_character_profiling(character, wiki_text, callback_url=callback_url)

    @action(detail=True, methods=['post'], url_path='regenerate_from_wiki')
    def regenerate_from_wiki(self, request, pk=None):
        """
        Re-runs the profiling logic on an existing character using the provided character data (wiki text).
        Returns the Job ID.
        """
        character = self.get_object()
        wiki_text = request.data.get("wiki_source_text", "")
        
        if not wiki_text:
             return Response(
                {"error": "Wiki source text is required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        from .services import trigger_character_profiling

        callback_url = request.build_absolute_uri(reverse("n8n-callback"))
        job_id = trigger_character_profiling(
            character, wiki_text, callback_url=callback_url
        )

        if job_id:
            return Response(
                {"job_id": job_id, "status": "PENDING"}, status=status.HTTP_202_ACCEPTED
            )
        else:
            return Response(
                {"error": "Failed to trigger profiling job."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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

        # Create Async Job
        from gatchalife.workflow_engine.models import AsyncJob

        job = AsyncJob.objects.create(
            job_type="create_variants",
            content_object=character,
            payload={"prompt": request.data.get("prompt", "")},
        )

        # Prepare Payload
        try:
            callback_url = request.build_absolute_uri(reverse("n8n-callback"))
            payload = {
                "job_id": str(job.id),
                "callback_url": callback_url,
                "character_id": character.id,
                "name": character.name,
                "series": character.series.name if character.series else "Unknown",
                "user_prompt": request.data.get("prompt", ""),
                # Detailed Description Fields
                "lore_tags": character.lore_tags,
                "body_type": character.body_type_description,
                "appearance": character.description,
                "visual_traits": character.visual_traits,
                "hair_prompt": character.hair_prompt,
                "eye_prompt": character.eye_prompt,
                "height_perception": character.height_perception,
                "affinity_environments": character.affinity_environments,
                "clashing_environments": character.clashing_environments,
                "negative_traits_suggestion": character.negative_traits_suggestion,
                # Context for AI to avoid duplicates
                "existing_variants": [
                    {"name": v.name, "description": v.description}
                    for v in character.variants.all()
                ],
            }
            
            # Prepare Files (Binary)
            files = {}
            if character.identity_face_image:
                try:
                    character.identity_face_image.open("rb")
                    files["identity_face_image"] = (
                        character.identity_face_image.name,
                        character.identity_face_image,
                        "application/octet-stream",
                    )
                except Exception as e:
                    logger.error(f"Failed to open face image for binary upload: {e}")

            # Send to n8n (Async trigger)
            if files:
                requests.post(webhook_url, data=payload, files=files, timeout=5)
            else:
                requests.post(webhook_url, json=payload, timeout=5)

            job.status = AsyncJob.Status.PROCESSING
            job.save()

            return Response(
                {
                    "message": "Variant generation started.",
                    "job_id": job.id,
                    "status": "PENDING",
                },
                status=status.HTTP_202_ACCEPTED,
            )

        except Exception as e:
            logger.exception("Error in create_variants trigger")
            job.status = AsyncJob.Status.FAILED
            job.error_message = str(e)
            job.save()
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