import logging
import requests
from django.conf import settings
from gatchalife.character.models import Character, CharacterVariant
from gatchalife.style.models import Theme

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
            response = requests.post(webhook_url, data=payload, files=files, timeout=600)
        else:
            response = requests.post(webhook_url, json=payload, timeout=600)

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

def update_variants_from_ai(character, ai_data):
    """
    Updates character variants based on AI output.
    Output schema: 
    { 
      variants: [{ 
        name, type, visual_override, description, 
        card_configurations: [{ rarity, pose, theme: {...}, style: {...} }] 
      }] 
    }
    """
    if isinstance(ai_data, dict) and "output" in ai_data:
        ai_data = ai_data["output"]
    
    variants_data = ai_data.get("variants", [])
    created_variants = []
    
    # Imports inside function to avoid circular imports layout issues if any (though usually fine at top)
    from gatchalife.style.models import Rarity, Style

    for v_data in variants_data:
        variant_name = v_data.get("name")
        if not variant_name: continue
        
        # Normalize Rarities in configurations before saving
        configs = v_data.get("card_configurations", [])
        for config in configs:
            raw_rarity = config.get("rarity", "COMMON").upper()
            if raw_rarity in ["UR", "SSR", "LEGENDARY"]:
                config["rarity"] = "LEGENDARY"
            elif raw_rarity in ["RARE", "SR", "R"]:
                config["rarity"] = "RARE"
            else:
                config["rarity"] = "COMMON"

        # Create/Update Variant
        # Create/Update Variant (Robust Case-Insensitive Match)
        variant = CharacterVariant.objects.filter(
            character=character, name__iexact=variant_name
        ).first()

        defaults = {
            "variant_type": v_data.get("type", "SKIN"),
            "visual_override": v_data.get("visual_override", ""),
            "description": v_data.get("description", ""),
            "card_configurations_data": configs,
        }

        if variant:
            # Update existing
            for key, value in defaults.items():
                setattr(variant, key, value)
            variant.name = variant_name  # Update casing to match AI output if desirable
            variant.save()
        else:
            # Create new
            variant = CharacterVariant.objects.create(
                character=character, name=variant_name, **defaults
            )
        
        # Process Configurations to ensure embedded Styles and Themes exist in DB
        for config in configs:
            # 1. Theme
            theme_data = config.get("theme", {})
            t_name = theme_data.get("name")
            if t_name:
                raw_vibes = theme_data.get("vibe_tags", "")
                vibe_list = [t.strip() for t in raw_vibes.split(",") if t.strip()] if isinstance(raw_vibes, str) else (raw_vibes or [])
                
                Theme.objects.update_or_create(
                    name=t_name,
                    defaults={
                        "prompt_background": theme_data.get("prompt_background", ""),
                        "vibe_tags": vibe_list,
                    }
                )
            
            # 2. Style & Rarity
            # Required for GeneratedImage ForeignKeys
            rarity_name = config.get("rarity", "COMMON") # Already normalized

            # Try to match Rarity
            rarity_obj = Rarity.objects.filter(name__iexact=rarity_name).first()
            if not rarity_obj:
                rarity_obj, _ = Rarity.objects.get_or_create(
                    name=rarity_name, 
                    defaults={
                        "min_roll_threshold": 95 if rarity_name == "LEGENDARY" else (80 if rarity_name == "RARE" else 0), 
                        "ui_color_hex": "#ffd700" if rarity_name == "LEGENDARY" else ("#0070dd" if rarity_name == "RARE" else "#cccccc")
                    }
                )

            style_data = config.get("style", {})
            s_name = style_data.get("name")
            if s_name and rarity_obj:
                Style.objects.update_or_create(
                    name=s_name,
                    rarity=rarity_obj, # A style belongs to a rarity in data model
                    defaults={
                        "style_keywords": style_data.get("style_keywords", "")
                    }
                )

        created_variants.append(variant)
        
    return created_variants
