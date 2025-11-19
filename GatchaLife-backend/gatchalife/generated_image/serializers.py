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
        # Get a random Rarity, Style, and Theme. Weight the rarity based on rarity.min_roll_threshold
        rarity = (
            Rarity.objects.filter(min_roll_threshold__lte=random.randint(0, 99))
            .order_by("-min_roll_threshold")
            .first()
        )
        style = Style.objects.filter(rarity=rarity).order_by("?").first()
        theme = Theme.objects.order_by("?").first()

        return generate_image(validated_data["character_variant"], rarity, style, theme)
