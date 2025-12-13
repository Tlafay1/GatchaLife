import random
from rest_framework import serializers

from .models import GeneratedImage
from .services import generate_image
from gatchalife.style.models import Style, Rarity, Theme


class GeneratedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedImage
        fields = [
            "id",
            "image",
            "character_variant",
            "rarity",
            "style",
            "theme",
            "created_at",
        ]
        read_only_fields = ["created_at", "image", "rarity", "style", "theme"]

    def create(self, validated_data):
        # 1. Roll for Rarity
        rarity = (
            Rarity.objects.filter(min_roll_threshold__lte=random.randint(0, 99))
            .order_by("-min_roll_threshold")
            .first()
        )

        variant = validated_data["character_variant"]
        configs = variant.card_configurations_data or []

        # Filter configs for the rolled rarity
        matching_configs = [
            c for c in configs if c.get("rarity", "").upper() == rarity.name.upper()
        ]

        pose = None
        style = None
        theme = None

        if matching_configs:
            # Pick a curated configuration
            config = random.choice(matching_configs)
            pose = config.get("pose")

            style_name = config.get("style", {}).get("name")
            theme_name = config.get("theme", {}).get("name")

            if style_name:
                style = Style.objects.filter(
                    name__iexact=style_name, rarity=rarity
                ).first()
            if theme_name:
                theme = Theme.objects.filter(name__iexact=theme_name).first()

        # Fallbacks
        if not style:
            style = Style.objects.filter(rarity=rarity).order_by("?").first()
            # If we fall back on style, the pose might not match, but let's keep it if we have nothing else
            # Or reset it? Safer to reset if style changed significantly, but here we assume sync.

        if not theme:
            theme = Theme.objects.order_by("?").first()

        return generate_image(variant, rarity, style, theme, pose=pose)
