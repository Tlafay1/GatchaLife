from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Player, PlayerQuest, Card, UserCard
from .serializers import PlayerSerializer, PlayerQuestSerializer, UserCardSerializer
from gatchalife.character.models import CharacterVariant
from gatchalife.style.models import Rarity, Style, Theme
import random
import structlog
from gatchalife.generated_image.services import generate_image
from gatchalife.generated_image.models import GeneratedImage

logger = structlog.get_logger(__name__)

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
        return queryset
            
        return queryset

    @action(detail=True, methods=["post"])
    def reroll_image(self, request, pk=None):
        user_card = self.get_object()
        card = user_card.card
        try:
            generate_image(card.character_variant, card.rarity, card.style, card.theme)
            # Re-fetch serializer to get new image URL
            # We need to invalidate the prefetch cache if any, or just re-serialize
            # Since generate_image creates a new DB row, re-serializing should pick it up
            # if the serializer method performs a fresh query.
            # CardSerializer.get_image_url performs a fresh query.
            serializer = self.get_serializer(user_card)
            return Response(serializer.data)
        except Exception as e:
            logger.error("image_regeneration_failed", error=str(e))
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        
        rarity = self.request.query_params.get('rarity')
        if rarity:
            queryset = queryset.filter(card__rarity__name=rarity)
            
        theme = self.request.query_params.get('theme')
        if theme:
            queryset = queryset.filter(card__theme__name=theme)
            
        character = self.request.query_params.get('character')
        if character:
            queryset = queryset.filter(card__character_variant__character__name__icontains=character)
            
        style = self.request.query_params.get('style')
        if style:
            queryset = queryset.filter(card__style__name=style)
            
        series = self.request.query_params.get('series')
        if series:
            queryset = queryset.filter(card__character_variant__character__series__name=series)
            
        return queryset


class GatchaViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["post"])
    def roll(self, request):
        player = get_default_player()
        cost = 100

        if player.gatcha_coins < cost:
            return Response(
                {"error": "Not enough coins"}, status=status.HTTP_400_BAD_REQUEST
            )

        player.gatcha_coins -= cost
        player.save()

        drops = []
        rarities = Rarity.objects.all()
        if not rarities.exists():
            return Response(
                {"error": "No rarities defined"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        ordered_rarities = list(rarities.order_by("-min_roll_threshold"))
        fallback_rarity = rarities.order_by("min_roll_threshold").first()

        for _ in range(5):
            # Drop Logic
            # 1. Pick Rarity based on weights with Level Boost

            # Base roll 1-100
            base_roll = random.randint(1, 100)

            # Level Boost: +0.5% chance for higher rarities per level (capped at +20%)
            # We simulate this by adding a bonus to the roll
            level_bonus = min(player.level * 0.5, 20.0)
            final_roll = min(base_roll + level_bonus, 100)

            selected_rarity = None
            # Sort by threshold descending to find the highest matching one
            for r in ordered_rarities:
                if final_roll >= r.min_roll_threshold:
                    selected_rarity = r
                    break

            if not selected_rarity:
                selected_rarity = fallback_rarity

            # 2. Pick Character, Style, Theme based on Unlock Level
            # Filter variants where character unlock level AND series unlock level are met
            variants = CharacterVariant.objects.filter(
                character__unlock_level__lte=player.level,
                character__series__unlock_level__lte=player.level,
            )

            styles = Style.objects.filter(
                rarity=selected_rarity, unlock_level__lte=player.level
            )

            themes = Theme.objects.filter(unlock_level__lte=player.level)

            # Fallback
            if not variants.exists():
                variants = CharacterVariant.objects.all()
            if not styles.exists():
                styles = Style.objects.filter(rarity=selected_rarity)
                if not styles.exists():
                    styles = Style.objects.all()
            if not themes.exists():
                themes = Theme.objects.all()

            if not variants.exists() or not styles.exists() or not themes.exists():
                continue  # Skip this drop if something is really wrong, or error out?
                # Ideally we should ensure data exists. For 5 drops, let's just try to get 5.
                # If we error out here, the user loses coins.
                # Let's hope the previous check was enough, or we just get what we can.

            variant = random.choice(list(variants))
            style = random.choice(list(styles))
            theme = random.choice(list(themes))

            # 3. Check for existing image or Generate New
            image_exists = GeneratedImage.objects.filter(
                character_variant=variant,
                rarity=selected_rarity,
                style=style,
                theme=theme,
            ).exists()

            if not image_exists:
                try:
                    generate_image(variant, selected_rarity, style, theme)
                except Exception as e:
                    logger.error("image_generation_failed", error=str(e))

            # 4. Get or Create Card
            card, created_card = Card.objects.get_or_create(
                character_variant=variant,
                rarity=selected_rarity,
                style=style,
                theme=theme,
            )

            # 5. Add to User Collection
            user_card, created_user_card = UserCard.objects.get_or_create(
                player=player, card=card
            )
            if not created_user_card:
                user_card.count += 1
                user_card.save()

            serializer = UserCardSerializer(user_card, context={"request": request})
            drop_data = serializer.data
            drop_data["is_new"] = created_user_card
            drop_data["roll_info"] = {
                "base_roll": base_roll,
                "level_bonus": level_bonus,
                "final_roll": final_roll,
                "rarity": selected_rarity.name,
            }
            drops.append(drop_data)

        return Response(
            {
                "drops": drops,
                "remaining_coins": player.gatcha_coins,
            }
        )
