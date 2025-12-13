import random
from rest_framework import serializers

import structlog

logger = structlog.get_logger(__name__)

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
        logger.info(
            "Rarity rolled",
            rarity=rarity.name,
            variant=validated_data["character_variant"].name,
        )

        variant = validated_data["character_variant"]
        configs = variant.card_configurations_data or []
        logger.debug(
            "Available configurations", variant=variant.name, total_configs=len(configs)
        )

        # Filter configs for the rolled rarity
        matching_configs = [
            c for c in configs if c.get("rarity", "").upper() == rarity.name.upper()
        ]
        logger.debug(
            "Matching configurations found for rarity",
            variant=variant.name,
            rarity=rarity.name,
            num_matching=len(matching_configs),
        )

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
                    name__iexact=style_name.strip(), rarity=rarity
                ).first()
            if theme_name:
                theme = Theme.objects.filter(name__iexact=theme_name.strip()).first()

            logger.info(
                "Matched configuration",
                variant=variant.name,
                rarity=rarity.name,
                pose=pose,
                style=style_name,
                theme=theme_name,
            )
        else:
            logger.info(
                "No matching configuration for rarity",
                variant=variant.name,
                rarity=rarity.name,
            )

        # Fallbacks
        if not style:
            style = Style.objects.filter(rarity=rarity).order_by("?").first()
            # If we fall back on style due to lookup fail or no config, preserve pose if it was set

        if not theme:
            theme = Theme.objects.order_by("?").first()

        return generate_image(variant, rarity, style, theme, pose=pose)
