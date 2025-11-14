from .models import Character, CharacterVariant, VariantReferenceImage, Series
from rest_framework import serializers


class VariantReferenceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantReferenceImage
        fields = ["id", "image"]


class CharacterVariantSerializer(serializers.ModelSerializer):
    images = VariantReferenceImageSerializer(many=True, read_only=True)

    class Meta:
        model = CharacterVariant
        fields = ["id", "name", "description", "images"]


class CharacterSerializer(serializers.ModelSerializer):
    variants = CharacterVariantSerializer(many=True, read_only=True)
    images = VariantReferenceImageSerializer(many=True, read_only=True)

    class Meta:
        model = Character
        fields = ["id", "name", "description", "images", "variants"]
        
class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = ["id", "name", "description"]