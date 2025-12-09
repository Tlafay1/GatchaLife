from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from .models import Player, DailyCompanionState
from gatchalife.ticktick.models import ProcessedTask
from django.conf import settings
import requests
import base64
from datetime import timedelta
from django.core.files.base import ContentFile

class CompanionViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'])
    def today(self, request):
        """
        Get the companion state for today.
        """
        # Since authentication is disabled/optional, just get the first player
        player = Player.objects.first()
        if not player:
             return Response({'status': 'no_player'}, status=status.HTTP_404_NOT_FOUND)
             
        today = timezone.now().date()
        
        state = DailyCompanionState.objects.filter(player=player, date=today).first()
        
        if not state:
            # Fallback / Sleeping State
            return Response({
                'status': 'sleeping',
                'character_name': 'Unknown',
                'mood_state': 'NEUTRAL',
                'image_url': None, # Frontend should show sleeping placeholder
                'dialogue_text': 'Zzz...',
                'productivity_score': 0
            })
            
        return Response({
            'status': 'active',
            'character_name': state.character_name,
            'mood_state': state.mood_state,
            'image_url': state.image.url if state.image else state.image_url,
            'dialogue_text': state.dialogue_text,
            'productivity_score': state.productivity_score,
            'date': state.date
        })

    @action(detail=False, methods=['post'])
    def generate_daily_mood(self, request):
        """
        Trigger the daily mood generation.
        Calculates score based on yesterday's activity and sends it to n8n.
        """
        player = Player.objects.first()
        if not player:
             return Response({'error': 'No player found'}, status=status.HTTP_404_NOT_FOUND)

        # 1. Calculate Yesterday's Stats
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        
        tasks_yesterday = ProcessedTask.objects.filter(
            processed_at__date=yesterday
        )
        task_count = tasks_yesterday.count()
        
        # Simple Logic for MVP
        # Score = min(Tasks * 10, 100)
        # Ideally, we'd have 'due date' logic but ProcessedTask tracks completion
        score = min(task_count * 15, 100)
        
        # Streak Bonus
        if player.current_streak > 3:
            score += 10
        
        score = min(score, 100)

        # 2. Determine Mood
        mood = 'NEUTRAL'
        if score < 30:
            mood = 'SAD'
        elif score < 60:
            mood = 'NEUTRAL'
        elif score < 90:
            mood = 'HAPPY'
        else:
            mood = 'EXCITED'

        # 3. Send to n8n
        n8n_url = f"{settings.N8N_BASE_URL}/{settings.N8N_WORKFLOW_WEBHOOK_PATH}"
        
        payload = {
            "player_id": player.id,
            "username": player.user.username,
            "date": str(today), # Generating mood FOR today based on yesterday
            "yesterday_date": str(yesterday),
            "score": score,
            "mood": mood,
            "tasks_completed": task_count,
            "streak": player.current_streak,
            "character_name": "Rem" # Default, could be dynamic
        }
        
        try:
            # We don't wait for the image generation if it takes too long, 
            # OR we assume n8n returns 'Started'.
            # If n8n workflow is async, this is fire-and-forget.
            # If n8n workflow returns the generated data immediately, we could process it here.
            # However, existing set_companion_state suggests n8n calls back.
            # Let's assume fire-and-forget or simple trigger.
            response = requests.post(n8n_url, json=payload, timeout=5)
            response.raise_for_status()
            
            return Response({
                'status': 'triggered', 
                'calculated_mood': mood, 
                'calculated_score': score,
                'n8n_status': response.status_code
            })
            
        except requests.exceptions.RequestException as e:
            return Response({'error': f"Failed to contact n8n: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['POST'])
@permission_classes([permissions.AllowAny]) # Protected by manual key check if needed, or rely on internal network / simple auth
def set_companion_state(request):
    """
    Admin/Service endpoint to set daily state.
    Expected payload:
    {
        "player_id": 1,
        "date": "YYYY-MM-DD",
        "mood": "HAPPY",
        "character": "Rem",
        "image_base64": "...", (optional)
        "image_url": "...", (optional)
        "dialogue": "..."
    }
    """
    # Simply check for a secret header for now if needed, or rely on obscurity/docker network
    # For now allowing any, assuming n8n connects securely
    
    data = request.data
    
    try:
        # Resolve Player
        # Support finding by username or ID
        player_id = data.get('player_id')
        username = data.get('username')
        
        if player_id:
            player = Player.objects.get(id=player_id)
        elif username:
            player = Player.objects.get(user__username=username)
        else:
            # Default to first player if single user instance
            player = Player.objects.first()
            if not player:
                 return Response({'error': 'No player found'}, status=status.HTTP_404_NOT_FOUND)

        date_str = data.get('date', str(timezone.now().date()))
        
        # update_or_create to handle re-runs
        state, created = DailyCompanionState.objects.update_or_create(
            player=player,
            date=date_str,
            defaults={
                'character_name': data.get('character', 'Unknown'),
                'mood_state': data.get('mood', 'NEUTRAL'),
                'dialogue_text': data.get('dialogue', '...'),
                'productivity_score': data.get('score', 0),
                'image_url': data.get('image_url')
            }
        )
        
        # Handle Base64 Image if provided
        img_b64 = data.get('image_base64')
        if img_b64:
            format, imgstr = img_b64.split(';base64,') 
            ext = format.split('/')[-1] 
            state.image.save(f"companion_{date_str}_{player.id}.{ext}", ContentFile(base64.b64decode(imgstr)), save=True)

        return Response({'status': 'success', 'id': state.id, 'created': created})

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
