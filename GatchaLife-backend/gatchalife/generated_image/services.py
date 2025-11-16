import requests
from io import BytesIO
import base64
import mimetypes
from django.conf import settings

from .models import GeneratedImage
from gatchalife.character.models import CharacterVariant
from gatchalife.character.serializers import (
    CharacterVariantSerializer,
    CharacterSerializer,
)
from gatchalife.style.models import Rarity, Style, Theme
from gatchalife.style.serializers import RaritySerializer, StyleSerializer, ThemeSerializer


def generate_image(character_variant: CharacterVariant, rarity: Rarity, style: Style, theme: Theme) -> GeneratedImage:
    # Trigger N8N workflow to generate image
    n8n_url = f"{settings.N8N_BASE_URL}/{settings.N8N_WORKFLOW_WEBHOOK_PATH}/{settings.N8N_GENERATE_IMAGE_WORKFLOW_ID}"

    character_variant_instance = character_variant
    character_instance = character_variant_instance.character

    character_variant_data = CharacterVariantSerializer(character_variant_instance).data
    character_data = CharacterSerializer(character_instance).data

    encoded_images_list = []
    for image_ref in character_variant_instance.images.all():
        image_file = image_ref.image

        with image_file.open("rb") as f:
            binary_data = f.read()
            base64_encoded_data = base64.b64encode(binary_data)
            base64_string = base64_encoded_data.decode("utf-8")

            mimetype, _ = mimetypes.guess_type(image_file.name)

            encoded_images_list.append(
                {
                    "filename": image_file.name,
                    "mimetype": mimetype or "image/png",
                    "data": base64_string,
                }
            )

    # --- Modification ici ---

    payload = {
        "character_variant": {**character_variant_data, "images": encoded_images_list},
        "character": {
            "name": character_data["name"],
            "description": character_data["description"],
        },
        "rarity": RaritySerializer(rarity).data,
        "style": StyleSerializer(style).data,
        "theme": ThemeSerializer(theme).data,
    }

    response = requests.post(n8n_url, json=payload)

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
