from rest_framework import serializers
from .models import Player, Quest, PlayerQuest, Card, UserCard
from gatchalife.character.models import CharacterVariant
from gatchalife.style.models import Rarity, Style, Theme

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

    class Meta:
        model = Card
        fields = ['id', 'character_variant', 'character_variant_name', 'character_name', 'series_name', 'rarity', 'rarity_name', 'style', 'style_name', 'theme', 'theme_name', 'image_url', 'pose', 'visual_override', 'description']

    def get_image_url(self, obj):
        # Logic to find the generated image for this card
        # This is a bit complex because GeneratedImage links to CharacterVariant, Rarity, Style, Theme
        # We might need to fetch the latest GeneratedImage matching these criteria
        from gatchalife.generated_image.models import GeneratedImage
        image = GeneratedImage.objects.filter(
            character_variant=obj.character_variant,
            rarity=obj.rarity,
            style=obj.style,
            theme=obj.theme
        ).order_by('-created_at').first()
        if image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(image.image.url)
            return image.image.url
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
