from django.db import models
from gatchalife.style.models import Theme


class Series(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    unlock_level = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name


class Character(models.Model):
    # ... (Same as before)
    name = models.CharField(max_length=100)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    unlock_level = models.PositiveIntegerField(default=1)
    legacy = models.BooleanField(default=False)

    class HeightPerception(models.TextChoices):
        SHORT = "SHORT", "Short"
        AVERAGE = "AVERAGE", "Average"
        TALL = "TALL", "Tall"
        GIANT = "GIANT", "Giant"

    # Phase 2: Visual & Lore Anchors
    identity_face_image = models.ImageField(upload_to="character_faces/", blank=True, null=True)
    body_type_description = models.CharField(
        max_length=255, blank=True, help_text="ex: petite stature, slender build, flat chest"
    )
    height_perception = models.CharField(
        max_length=50,
        choices=HeightPerception.choices,
        default=HeightPerception.AVERAGE,
        blank=True,
        help_text="ex: short, tall, giant",
    )
    hair_prompt = models.TextField(
        blank=True, help_text="Description visuelle des cheveux"
    )
    eye_prompt = models.TextField(blank=True, help_text="Description visuelle des yeux")

    visual_traits = models.JSONField(
        default=list,
        blank=True,
        help_text="Liste de traits physiques immuables ex: ['scar on left eye', 'pale skin']",
    )

    lore_tags = models.JSONField(
        default=list, blank=True, help_text="ex: ['stealth', 'modern', 'cynical']"
    )
    affinity_environments = models.JSONField(
        default=list,
        blank=True,
        help_text="ex: [{'name': 'shadows', 'visual_prompt': 'dark alley'}]",
    )
    clashing_environments = models.JSONField(
        default=list, blank=True, help_text="ex: ['holy church', 'bright beach']"
    )
    negative_traits_suggestion = models.TextField(
        blank=True, help_text="Negative prompt morphologique"
    )

    def __str__(self):
        return self.name


class CharacterVariant(models.Model):
    character = models.ForeignKey(
        Character, related_name="variants", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    # Phase 2: Variant details
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, null=True, blank=True)
    visual_override = models.TextField(
        blank=True, help_text="Description de la tenue et de l'adaptation"
    )

    class VariantType(models.TextChoices):
        CANON = 'CANON', 'Canon'
        SKIN = 'SKIN', 'Skin'

    variant_type = models.CharField(
        max_length=50,
        choices=VariantType.choices,
        default=VariantType.CANON,
    )
    specific_reference_image = models.ImageField(
        upload_to="variant_refs/", blank=True, null=True
    )
    card_configurations_data = models.JSONField(
        default=list, blank=True, help_text="AI generated card configurations (rarity, pose, theme, style)"
    )
    legacy = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.character.name} ({self.name})"


class VariantReferenceImage(models.Model):
    """
    Stores multiple reference images for a single variant.
    """

    variant = models.ForeignKey(
        CharacterVariant, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="ref_images/")

    def __str__(self):
        return f"Image for {self.variant.character.name} - {self.variant.name}"
