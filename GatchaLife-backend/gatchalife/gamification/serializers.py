from rest_framework import serializers
from .models import (
    Player,
    Quest,
    PlayerQuest,
    Card,
    UserCard,
    ActiveTamagotchi,
    CompanionImage,
)
# Removed unused imports
from gatchalife.generated_image.services import match_card_configuration

class CompanionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanionImage
        fields = ["id", "character", "image", "state"]


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'level', 'xp', 'gatcha_coins']
        read_only_fields = ['level', 'xp', 'gatcha_coins']

class QuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = '__all__'

class PlayerQuestSerializer(serializers.ModelSerializer):
    quest = QuestSerializer(read_only=True)
    
    class Meta:
        model = PlayerQuest
        fields = ['id', 'quest', 'progress', 'completed', 'claimed']
        read_only_fields = ['completed', 'claimed']


class CardSerializer(serializers.ModelSerializer):
    character_variant_name = serializers.CharField(source='character_variant.name', read_only=True)
    character_name = serializers.CharField(source='character_variant.character.name', read_only=True)
    rarity_name = serializers.CharField(source='rarity.name', read_only=True)
    style_name = serializers.CharField(source='style.name', read_only=True)
    theme_name = serializers.CharField(source='theme.name', read_only=True)
    series_name = serializers.CharField(source='character_variant.character.series.name', read_only=True)
    image_url = serializers.SerializerMethodField()
    pose = serializers.SerializerMethodField()
    visual_override = serializers.CharField(source='character_variant.visual_override', read_only=True)
    description = serializers.CharField(source='character_variant.description', read_only=True)
    is_archived = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = [
            "id",
            "character_variant",
            "character_variant_name",
            "character_name",
            "series_name",
            "rarity",
            "rarity_name",
            "style",
            "style_name",
            "theme",
            "theme_name",
            "image_url",
            "pose",
            "visual_override",
            "description",
            "is_archived",
            "thumbnail_url",
        ]

    def get_is_archived(self, obj):
        matched_config = match_card_configuration(
            obj.character_variant, obj.rarity, obj.style, obj.theme
        )
        is_config_legacy = (
            matched_config.get("legacy", False) if matched_config else False
        )

        return (
            obj.legacy
            or obj.character_variant.legacy
            or obj.character_variant.character.legacy
            or is_config_legacy
        )

    def get_image_url(self, obj):
        # Update to handle the new dict structure in image_map
        image_map = self.context.get("image_map")
        if image_map:
            key = (obj.character_variant_id, obj.rarity_id, obj.style_id, obj.theme_id)
            data = image_map.get(key)
            if data:
                url = data.get("image_url")
                request = self.context.get("request")
                if request and url:
                    return request.build_absolute_uri(url)
                return url
            return None

        # Fallback to single query (slow)
        from gatchalife.generated_image.models import GeneratedImage

        image = (
            GeneratedImage.objects.filter(
                character_variant_id=obj.character_variant_id,
                rarity_id=obj.rarity_id,
                style_id=obj.style_id,
                theme_id=obj.theme_id,
            )
            .order_by("-created_at")
            .first()
        )

        if image:
            try:
                if not image.image:
                    return None
                url = image.image.url
                request = self.context.get("request")
                if request:
                    return request.build_absolute_uri(url)
                return url
            except ValueError:
                return None
        return None

    def get_thumbnail_url(self, obj):
        # New method for thumbnail
        image_map = self.context.get("image_map")
        if image_map:
            key = (obj.character_variant_id, obj.rarity_id, obj.style_id, obj.theme_id)
            data = image_map.get(key)
            if data:
                url = data.get("thumbnail_url")
                request = self.context.get("request")
                if request and url:
                    return request.build_absolute_uri(url)
                return url
            return None

        # Fallback logic for single object
        from gatchalife.generated_image.models import GeneratedImage

        image = (
            GeneratedImage.objects.filter(
                character_variant_id=obj.character_variant_id,
                rarity_id=obj.rarity_id,
                style_id=obj.style_id,
                theme_id=obj.theme_id,
            )
            .order_by("-created_at")
            .first()
        )

        if image:
            # Return thumbnail if exists, else full image
            target_field = image.thumbnail if image.thumbnail else image.image
            if not target_field:
                return None
            url = target_field.url
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(url)
            return url
        return None

    def get_pose(self, obj):
        # Infer pose from matching config in variant
        configs = obj.character_variant.card_configurations_data
        # Match by Rarity AND Style AND Theme to be precise
        # (Assuming V/R/S/T uniqueness holds as fixed in previous step)
        for config in configs:
            c_rarity = config.get("rarity", "").upper()
            c_style = config.get("style", {}).get("name")
            c_theme = config.get("theme", {}).get("name")
            
            if (c_rarity == obj.rarity.name.upper() and
                c_style == obj.style.name and
                c_theme == obj.theme.name):
                return config.get("pose", "")
        
        # Fallback: loose match or first matching rarity
        for config in configs:
            if config.get("rarity", "").upper() == obj.rarity.name.upper():
                 return config.get("pose", "")
        return ""

class UserCardSerializer(serializers.ModelSerializer):
    card = CardSerializer(read_only=True)
    
    class Meta:
        model = UserCard
        fields = ['id', 'card', 'count', 'obtained_at']

class ActiveTamagotchiSerializer(serializers.ModelSerializer):
    character_id = serializers.IntegerField()
    character_image = serializers.SerializerMethodField()
    is_sleeping = serializers.SerializerMethodField()
    character_name = serializers.CharField(source="character.name", read_only=True)

    class Meta:
        model = ActiveTamagotchi
        fields = [
            "id",
            "name",
            "mood",
            "last_feed_time",
            "last_pet_time",
            "last_daily_reset",
            "last_decay_update",
            "sleep_start_hour",
            "sleep_end_hour",
            "character_id",
            "character_image",
            "character_name",
            "is_sleeping",
        ]
        read_only_fields = ["last_decay_update", "name"]

    def get_is_sleeping(self, obj):
        from django.utils import timezone

        now_hour = timezone.localtime().hour
        if obj.sleep_start_hour > obj.sleep_end_hour:
            return now_hour >= obj.sleep_start_hour or now_hour < obj.sleep_end_hour
        else:
            return obj.sleep_start_hour <= now_hour < obj.sleep_end_hour

    def get_character_image(self, obj):
        from .models import CompanionImage, CompanionState

        # Determine current state
        if self.get_is_sleeping(obj):
            current_state = CompanionState.SLEEPING
        else:
            # Map mood to state
            mood = obj.mood
            if mood >= 80:
                current_state = CompanionState.EXTREMELY_HAPPY
            elif mood >= 60:
                current_state = CompanionState.HAPPY
            elif mood >= 40:
                current_state = CompanionState.NEUTRAL
            elif mood >= 20:
                current_state = CompanionState.POUTING
            elif mood > 0:
                current_state = CompanionState.DISTRESSED
            else:
                current_state = CompanionState.DEAD

        # Find image for state
        mood_image = CompanionImage.objects.filter(
            character=obj.character, state=current_state
        ).first()

        # If we have a mood image, use it
        target_image = None
        if mood_image:
            target_image = mood_image.image
        # Fallback to character face if no mood image (unless DEAD or generic fallback needed?)
        elif obj.character and obj.character.identity_face_image:
            target_image = obj.character.identity_face_image

        if target_image:
            request = self.context.get("request")
            url = target_image.url
            if request:
                return request.build_absolute_uri(url)
            return url
        return None
