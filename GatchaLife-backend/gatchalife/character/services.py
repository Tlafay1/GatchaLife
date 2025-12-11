import logging
import requests
from django.conf import settings
from gatchalife.character.models import Character

logger = logging.getLogger(__name__)

def update_character_from_ai(character, ai_data):
    """
    Updates a character instance with data returned from the AI.
    Handles field mapping and validation (e.g., Enum conversion).
    """
    # Defensive programming: handle if 'output' wrapper exists or not
    if isinstance(ai_data, dict) and "output" in ai_data:
        ai_data = ai_data["output"]

    # Map fields
    if "appearance" in ai_data:
        character.description = ai_data.get("appearance", character.description)
    
    character.body_type_description = ai_data.get("body_type_description", "")
    
    # Height Perception Logic
    raw_height = ai_data.get("height_perception", "AVERAGE").strip().upper()
    if raw_height not in Character.HeightPerception.values and raw_height not in Character.HeightPerception.names:
            if "SHORT" in raw_height: raw_height = "SHORT"
            elif "TALL" in raw_height: raw_height = "TALL" 
            elif "GIANT" in raw_height: raw_height = "GIANT"
            else: raw_height = "AVERAGE"
    character.height_perception = raw_height

    character.visual_traits = ai_data.get("visual_traits", [])
    character.lore_tags = ai_data.get("lore_tags", [])
    character.affinity_environments = ai_data.get("affinity_environments", [])
    character.clashing_environments = ai_data.get("clashing_environments", [])
    # Ensure this is a string, not a list
    neg_traits = ai_data.get("negative_traits_suggestion", "")
    character.negative_traits_suggestion = neg_traits if isinstance(neg_traits, str) else str(neg_traits)
    
    character.hair_prompt = ai_data.get("hair_prompt", "")
    character.eye_prompt = ai_data.get("eye_prompt", "")
    
    character.save()
    return character

def trigger_character_profiling(character, wiki_text):
    """
    Triggers the n8n workflow to profile a character based on wiki text.
    Returns the raw response JSON from n8n or None if failed.
    """
    n8n_path = getattr(settings, "N8N_CHARACTER_WEBHOOK_URL", "character-profile")
    base_url = getattr(settings, "N8N_BASE_URL", None)
    webhook_path = getattr(settings, "N8N_WORKFLOW_WEBHOOK_PATH", "webhook")

    if not (n8n_path and base_url):
        logger.error("N8N settings missing for character profiling.")
        return None

    webhook_url = f"{base_url}/{webhook_path}/{n8n_path}"
    
    # Prepare payload expected by n8n
    payload = {
        "character_name": character.name,
        "series": character.series.name if character.series else "Unknown",
        "wiki_source_text": wiki_text, # Standardized key
        # Legacy key support if n8n expects 'Content'
        "Content": wiki_text
    }

    files = {}
    if character.identity_face_image:
        try:
            character.identity_face_image.open("rb")
            files["identity_face_image"] = (
                character.identity_face_image.name,
                character.identity_face_image,
                "application/octet-stream",
            )
        except Exception as file_err:
            logger.error(f"Could not prepare image file for automation: {file_err}")

    try:
        if files:
            response = requests.post(webhook_url, data=payload, files=files, timeout=60)
        else:
            response = requests.post(webhook_url, json=payload, timeout=60)

        if response.status_code == 200:
            ai_data_list = response.json()
            # Normalize list vs dict response
            ai_data = ai_data_list[0] if isinstance(ai_data_list, list) and ai_data_list else ai_data_list
            return ai_data
        else:
            logger.error(f"N8N Error {response.status_code}: {response.text}")
            return None

    except Exception as e:
        logger.error(f"Failed to trigger automation for character {character.id}: {e}")
        return None
