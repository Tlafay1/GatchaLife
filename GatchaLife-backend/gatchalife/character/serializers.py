from .models import Character, CharacterVariant, VariantReferenceImage, Series
from rest_framework import serializers


class VariantReferenceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantReferenceImage
        fields = ["id", "image", "variant"]


class CharacterVariantSerializer(serializers.ModelSerializer):
    images = VariantReferenceImageSerializer(many=True, read_only=True)

    class Meta:
        model = CharacterVariant
        fields = ["id", "name", "description", "images", "character"]


class CharacterSerializer(serializers.ModelSerializer):
    variants = CharacterVariantSerializer(many=True, read_only=True)
    images = VariantReferenceImageSerializer(many=True, read_only=True)

    class Meta:
        model = Character
        fields = ["id", "name", "description", "images", "variants", "series"]


class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = ["id", "name", "description"]
