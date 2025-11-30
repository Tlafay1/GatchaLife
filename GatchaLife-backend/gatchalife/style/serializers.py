from rest_framework import serializers

from .models import Rarity, Style, Theme


class RaritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Rarity
        fields = ["id", "name", "min_roll_threshold", "ui_color_hex"]


class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style
        fields = [
            "id",
            "name",
            "style_keywords",
            "composition_hint",
            "rarity",
            "unlock_level",
        ]


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = [
            "id",
            "name",
            "category",
            "ambiance",
            "keywords_theme",
            "prompt_background",
            "integration_idea",
            "unlock_level",
        ]
