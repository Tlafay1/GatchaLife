from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Player, Quest, PlayerQuest, Card, UserCard
from .serializers import PlayerSerializer, QuestSerializer, PlayerQuestSerializer, UserCardSerializer
from gatchalife.character.models import CharacterVariant
from gatchalife.style.models import Rarity, Style, Theme
import random

def get_default_player():
    # Get the first user or create a default one
    user = User.objects.first()
    if not user:
        user = User.objects.create(username='Player1')
    player, _ = Player.objects.get_or_create(user=user)
    return player

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return get_default_player()

class PlayerQuestViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlayerQuestSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        player = get_default_player()
        return PlayerQuest.objects.filter(player=player)

    @action(detail=True, methods=['post'])
    def claim(self, request, pk=None):
        player_quest = self.get_object()
        if player_quest.completed and not player_quest.claimed:
            player = player_quest.player
            player.xp += player_quest.quest.xp_reward
            player.gatcha_coins += player_quest.quest.currency_reward
            player.save()
            
            player_quest.claimed = True
            player_quest.save()
            return Response({'status': 'claimed'})
        return Response({'error': 'Cannot claim reward'}, status=status.HTTP_400_BAD_REQUEST)

class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserCardSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        player = get_default_player()
        queryset = UserCard.objects.filter(player=player)
        
        rarity = self.request.query_params.get('rarity')
        if rarity:
            queryset = queryset.filter(card__rarity__name=rarity)
            
        return queryset

from gatchalife.generated_image.services import generate_image
from gatchalife.generated_image.models import GeneratedImage

class GatchaViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['post'])
    def roll(self, request):
        player = get_default_player()
        cost = 100
        
        if player.gatcha_coins < cost:
            return Response({'error': 'Not enough coins'}, status=status.HTTP_400_BAD_REQUEST)
            
        player.gatcha_coins -= cost
        player.save()
        
        # Drop Logic
        # 1. Pick Rarity based on weights
        rarities = Rarity.objects.all()
        if not rarities.exists():
             return Response({'error': 'No rarities defined'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Simple weighted random (assuming min_roll_threshold is 0-100)
        roll = random.randint(1, 100)
        
        selected_rarity = None
        # Sort by threshold descending to find the highest matching one
        ordered_rarities = list(rarities.order_by('-min_roll_threshold'))
        for r in ordered_rarities:
            if roll >= r.min_roll_threshold:
                selected_rarity = r
                break
        
        if not selected_rarity:
            selected_rarity = rarities.order_by('min_roll_threshold').first()

        # 2. Pick Character, Style, Theme
        variants = CharacterVariant.objects.all()
        styles = Style.objects.filter(rarity=selected_rarity)
        themes = Theme.objects.all()
        
        if not variants.exists() or not styles.exists() or not themes.exists():
             return Response({'error': 'Missing game data (variants/styles/themes)'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        variant = random.choice(list(variants))
        style = random.choice(list(styles))
        theme = random.choice(list(themes))
        
        # 3. Check for existing image or Generate New
        # We only generate if we don't have an image for this specific combination
        image_exists = GeneratedImage.objects.filter(
            character_variant=variant,
            rarity=selected_rarity,
            style=style,
            theme=theme
        ).exists()

        if not image_exists:
            try:
                generate_image(variant, selected_rarity, style, theme)
            except Exception as e:
                # If generation fails, we might still want to give the card, but maybe log error
                # For now, let's just print it and continue, the card will have no image
                print(f"Image generation failed: {e}")

        # 4. Get or Create Card
        card, created = Card.objects.get_or_create(
            character_variant=variant,
            rarity=selected_rarity,
            style=style,
            theme=theme
        )
        
        # 5. Add to User Collection
        user_card, created = UserCard.objects.get_or_create(player=player, card=card)
        if not created:
            user_card.count += 1
            user_card.save()
            
        serializer = UserCardSerializer(user_card, context={'request': request})
        return Response({
            'drop': serializer.data,
            'is_new': created,
            'remaining_coins': player.gatcha_coins
        })
