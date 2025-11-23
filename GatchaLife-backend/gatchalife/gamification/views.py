from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Player, Quest, PlayerQuest, Card, UserCard
from .serializers import PlayerSerializer, QuestSerializer, PlayerQuestSerializer, UserCardSerializer
from gatchalife.character.models import CharacterVariant
from gatchalife.style.models import Rarity, Style, Theme
import random

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def get_object(self):
        # Ensure we always return the player for the current user (or the only player)
        # For now, assuming single user, we get the first player or create one
        player, created = Player.objects.get_or_create(user=self.request.user)
        return player

    @action(detail=False, methods=['post'])
    def sync_ticktick(self, request):
        # Placeholder for TickTick sync logic
        # In a real implementation, this would fetch tasks from TickTick API
        # For now, we can simulate completing a task
        player = self.get_object()
        tasks_completed = request.data.get('tasks_completed', 1)
        
        xp_gain = tasks_completed * 10
        currency_gain = tasks_completed * 5
        
        player.xp += xp_gain
        player.gatcha_coins += currency_gain
        
        # Level up logic (simple: level * 100 xp required)
        xp_needed = player.level * 100
        if player.xp >= xp_needed:
            player.level += 1
            player.xp -= xp_needed
            # Bonus currency for leveling up
            player.gatcha_coins += 50
            
        player.save()
        
        return Response({
            'status': 'synced',
            'xp_gained': xp_gain,
            'currency_gained': currency_gain,
            'new_level': player.level,
            'current_xp': player.xp,
            'current_currency': player.gatcha_coins
        })

class PlayerQuestViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlayerQuestSerializer

    def get_queryset(self):
        player, _ = Player.objects.get_or_create(user=self.request.user)
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

    def get_queryset(self):
        player, _ = Player.objects.get_or_create(user=self.request.user)
        queryset = UserCard.objects.filter(player=player)
        
        rarity = self.request.query_params.get('rarity')
        if rarity:
            queryset = queryset.filter(card__rarity__name=rarity)
            
        return queryset

class GatchaViewSet(viewsets.ViewSet):
    
    @action(detail=False, methods=['post'])
    def roll(self, request):
        player, _ = Player.objects.get_or_create(user=request.user)
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
        roll = random.randint(0, 100)
        selected_rarity = None
        # Sort by threshold descending to find the highest matching one
        for r in rarities.order_by('-min_roll_threshold'):
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
        
        # 3. Get or Create Card
        card, created = Card.objects.get_or_create(
            character_variant=variant,
            rarity=selected_rarity,
            style=style,
            theme=theme
        )
        
        # 4. Add to User Collection
        user_card, created = UserCard.objects.get_or_create(player=player, card=card)
        if not created:
            user_card.count += 1
            user_card.save()
            
        # 5. Trigger Image Generation (Async in real app, placeholder here)
        # For now, we assume the image might not exist yet. 
        # In a real scenario, we would trigger a celery task here.
        
        serializer = UserCardSerializer(user_card)
        return Response({
            'drop': serializer.data,
            'is_new': created,
            'remaining_coins': player.gatcha_coins
        })
