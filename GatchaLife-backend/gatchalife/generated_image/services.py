import requests
from io import BytesIO
import base64
import mimetypes
from django.conf import settings
import structlog

logger = structlog.get_logger(__name__)

from .models import GeneratedImage
from gatchalife.character.models import CharacterVariant
from gatchalife.character.serializers import (
    CharacterVariantSerializer,
    CharacterSerializer,
)
from gatchalife.style.models import Rarity, Style, Theme
from gatchalife.style.serializers import RaritySerializer, StyleSerializer, ThemeSerializer


def match_card_configuration(variant, rarity, style, theme):
    """
    Finds the specific card configuration that matches the given rarity, style, and theme
    for a character variant.
    """
    configs = variant.card_configurations_data or []

    for c in configs:
        # Check Rarity
        if c.get("rarity", "").upper() != rarity.name.upper():
            continue

        # Check Style
        # If config has a style, it MUST match. If config has no style, it accepts any style?
        # Usually config determines the style. So if config has style, we check equality.
        c_style = c.get("style", {}).get("name", "")
        if c_style and style and c_style.strip().lower() != style.name.strip().lower():
            continue

        # Check Theme
        c_theme = c.get("theme", {}).get("name", "")
        if c_theme and theme and c_theme.strip().lower() != theme.name.strip().lower():
            continue

        # Found match
        return c

    return None


def generate_image(character_variant: CharacterVariant, rarity: Rarity, style: Style, theme: Theme, pose: str = None, card_configuration: dict = None) -> GeneratedImage:
    # Trigger N8N workflow to generate image
    n8n_url = f"{settings.N8N_BASE_URL}/{settings.N8N_WORKFLOW_WEBHOOK_PATH}/{settings.N8N_GENERATE_IMAGE_WORKFLOW_ID}"

    character_variant_instance = character_variant
    character_instance = character_variant_instance.character

    character_variant_data = CharacterVariantSerializer(character_variant_instance).data
    character_data = CharacterSerializer(character_instance).data
    
    # Debug: Ensure we pass serializable data
    # Serializers usually return dicts, but let's be safe with UUIDs/DateTimes if any (DRF handles them usually)

    def encode_image_field(image_field):
        if not image_field:
            return None
        try:
            with image_field.open("rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        except Exception as e:
            logger.error(f"Failed to encode image: {e}")
            return None

    # Base64 encode Character Variant Reference Images (Existing logic)
    encoded_images_list = []

    # Force fetch images if lazy (though .all() does that)
    ref_images = character_variant_instance.images.all()

    for image_ref in ref_images:
         encoded_data = encode_image_field(image_ref.image)
         if encoded_data:
            mimetype, _ = mimetypes.guess_type(image_ref.image.name)
            encoded_images_list.append({
                "filename": image_ref.image.name,
                "mimetype": mimetype or "image/png",
                "data": encoded_data,
            })

    logger.info(
        "Encoded reference images for generation",
        variant=character_variant_instance.name,
        count=len(encoded_images_list),
    )
    
    # Base64 encode Specific Reference (Variant)
    specific_ref_b64 = encode_image_field(character_variant_instance.specific_reference_image)

    # Prepare Prioritized Identity Face / Variant Reference as Base64
    # Priority: Variant Specific Reference > Character Identity Face
    # This will be sent as 'identity_face_image_b64' in the root or character object for N8N to use
    
    final_identity_image_b64 = None
    
    # Check Variant Specific Reference First
    if character_variant_instance.specific_reference_image:
        final_identity_image_b64 = encode_image_field(character_variant_instance.specific_reference_image)
    
    # Fallback to Character Identity Face
    if not final_identity_image_b64 and character_instance.identity_face_image:
         final_identity_image_b64 = encode_image_field(character_instance.identity_face_image)

    payload = {
        "character_variant": {
            **character_variant_data, 
            "images": encoded_images_list,
            "specific_reference_image_b64": specific_ref_b64 
        },
        "character": {
            **character_data,
            # We explicitly override/set this field for the N8N workflow to easily pick it up
            "identity_face_image_b64": final_identity_image_b64
        },
        "rarity": RaritySerializer(rarity).data,
        "style": StyleSerializer(style).data,
        "theme": {
            **ThemeSerializer(theme).data,
        },
        "pose": pose,
        "card_configuration": card_configuration, # Pass full or partial config if needed
        "identity_face_image": final_identity_image_b64
    }

    response = requests.post(n8n_url, json=payload, timeout=600)

    response.raise_for_status()

    # Retrieve the binary image data from the response
    generated_image = response.content

    # Save the generated image to the model instance
    image_instance = GeneratedImage.objects.create(
        character_variant=character_variant_instance,
        rarity=rarity,
        style=style,
        theme=theme,
    )
    image_filename = f"generated_image_{image_instance.id}.png"
    image_instance.image.save(image_filename, BytesIO(generated_image), save=True)

    return image_instance
