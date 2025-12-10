import requests
import logging
from django.conf import settings
from rest_framework import viewsets, filters, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
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
            n8n_path = getattr(settings, "N8N_CHARACTER_WEBHOOK_URL", None)
            base_url = getattr(settings, "N8N_BASE_URL", None)
            webhook_path = getattr(settings, "N8N_WORKFLOW_WEBHOOK_PATH", "webhook")

            webhook_url = None
            if n8n_path and base_url:
                webhook_url = f"{base_url}/{webhook_path}/{n8n_path}"

            if webhook_url:
                try:
                    # 2. Préparation du payload
                    # IMPORTANT : La clé "Content" correspond à ce que ton Agent n8n attend ({{ $json.Content }})
                    payload = {
                        "character_name": character.name,
                        "series": character.series.name
                        if character.series
                        else "Unknown",
                        "Content": wiki_text,
                    }

                    files = {}
                    if character.identity_face_image:
                        try:
                            # Re-open the file to ensure we can read it
                            character.identity_face_image.open("rb")
                            files["identity_face_image"] = (
                                character.identity_face_image.name,
                                character.identity_face_image,
                                "application/octet-stream",
                            )
                        except Exception as file_err:
                            logger.error(
                                f"Could not prepare image file for automation: {file_err}"
                            )

                    # 3. Appel Synchrone (Blocking)
                    # On augmente le timeout car l'IA met du temps à répondre (ex: 30s)
                    # Use data=payload + files=files for multipart/form-data
                    if files:
                        response = requests.post(
                            webhook_url, data=payload, files=files, timeout=30
                        )
                    else:
                        response = requests.post(webhook_url, json=payload, timeout=30)

                    if response.status_code == 200:
                        # 4. Récupération et Parsing des données structurées
                        ai_data = response.json()

                        # Mise à jour des champs du modèle Character
                        # Assure-toi que ces champs existent dans ton modèle Django
                        character.body_type_description = ai_data.get(
                            "body_type_description", ""
                        )
                        character.height_perception = ai_data.get(
                            "height_perception", "average"
                        )
                        character.visual_traits = ai_data.get(
                            "visual_traits", []
                        )  # Supposant un JSONField ou ArrayField
                        character.lore_tags = ai_data.get("lore_tags", [])
                        character.affinity_environments = ai_data.get(
                            "affinity_environments", []
                        )
                        character.clashing_environments = ai_data.get(
                            "clashing_environments", []
                        )

                        # Sauvegarde finale avec les données enrichies
                        character.save()

                    else:
                        logger.error(
                            f"N8N Error {response.status_code}: {response.text}"
                        )

                except requests.Timeout:
                    logger.warning(
                        f"N8N timed out for character {character.id}. Background processing might be needed."
                    )
                except Exception as e:
                    # On log l'erreur mais on ne bloque pas la création du perso,
                    # il sera créé mais sans les données IA.
                    logger.error(
                        f"Failed to trigger automation for character {character.id}: {e}"
                    )
            else:
                logger.warning("N8N_CHARACTER_WEBHOOK_URL is not set in settings.")


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