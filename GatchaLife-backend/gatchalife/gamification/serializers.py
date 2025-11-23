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
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = ['id', 'character_variant', 'character_variant_name', 'character_name', 'rarity', 'rarity_name', 'style', 'style_name', 'theme', 'theme_name', 'image_url']

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
            return image.image.url
        return None

class UserCardSerializer(serializers.ModelSerializer):
    card = CardSerializer(read_only=True)
    
    class Meta:
        model = UserCard
        fields = ['id', 'card', 'count', 'obtained_at']
