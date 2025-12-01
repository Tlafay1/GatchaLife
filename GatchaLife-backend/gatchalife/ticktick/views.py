import json
import random
from datetime import timedelta
from rest_framework import viewsets, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status as http_status
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import TickTickTask, ProcessedTask, TickTickProject, TickTickColumn

class TickTickViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny] # For now, as per project settings

    @action(detail=False, methods=['get'])
    def stats(self, request):
        # Total completed tasks (status 2)
        total_completed = ProcessedTask.objects.count()  # All rewarded tasks
        
        today = timezone.now().date()
        processed_today = ProcessedTask.objects.filter(processed_at__date=today).count()
        total_processed = ProcessedTask.objects.count()
        
        # Recent tasks (from ProcessedTask)
        recent_processed = ProcessedTask.objects.order_by('-processed_at')[:5]
        
        recent_activity = []
        for p in recent_processed:
            recent_activity.append({
                'id': p.task_id,
                'title': p.task_title or f"Task {p.task_id}",
                'project': None,
                'processed_at': p.processed_at
            })
                
        return Response({
            'total_completed_all_time': total_completed,
            'rewarded_total': total_processed,
            'rewarded_today': processed_today,
            'recent_activity': recent_activity
        })

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def zapier_webhook(request):
    """
    Webhook endpoint for Zapier to call when a task is completed.
    
    Expected payload from Zapier:
    {
        "id": "string",
        "task_name": "string",
        "list": "string" (optional),
        "tag": "List[string]" (optional),
        "priority": "string" (optional),
        "timestamp": number (optional),
        "link_to_task": "string" (optional),
        "repeat_flag": "string" (optional)
    }
    """
    from gatchalife.gamification.models import Player
    from django.contrib.auth.models import User
    
    # Get task data from Zapier (using their field names)
    # FIXME: Couldn't get zapier to send JSON body properly, so using form-encoded 'data' field
    data = json.loads(request.data.get('data', '{}'))
    task_id = data.get('id')
    title = data.get('task_name', 'Unknown Task')
    
    if not task_id:
        return Response({
            'error': 'id is required'
        }, status=http_status.HTTP_400_BAD_REQUEST)
    
    # Check if we've already processed this task
    if ProcessedTask.objects.filter(task_id=task_id).exists():
        return Response({
            'status': 'already_processed',
            'message': f'Task {task_id} has already been rewarded'
        }, status=http_status.HTTP_200_OK)
    
    # Get the default player
    user = User.objects.first()
    if not user:
        user = User.objects.create(username='Player1')
    player, _ = Player.objects.get_or_create(user=user)
    
    # 1. Gestion du Streak et du Bonus Quotidien
    now = timezone.now()
    today = now.date()
    daily_bonus = 0

    if player.last_activity_date:
        last_date = player.last_activity_date.date()
        if last_date < today:
            # C'est la première tâche de la journée !
            daily_bonus = 50  # Gros boost : la moitié d'une carte offerte
            
            if last_date == today - timedelta(days=1):
                player.current_streak += 1
            else:
                player.current_streak = 1 # Reset si jour raté
    else:
        # Tout premier jour
        daily_bonus = 100 # Premier shoot gratuit (Onboarding)
        player.current_streak = 1

    player.last_activity_date = now

    # 2. Calcul de la récompense variable (Skinner Box)
    # Base entre 15 et 25 (au lieu de 5)
    base_currency = random.randint(15, 25)

    # 3. Multiplicateur de Streak (Max x1.5)
    streak_multiplier = 1 + min(player.current_streak * 0.05, 0.5)

    # 4. Critique / Jackpot (10% de chance de x3)
    is_crit = random.random() < 0.10
    crit_multiplier = 3 if is_crit else 1

    # Calcul Final
    currency_gain = int((base_currency * streak_multiplier * crit_multiplier) + daily_bonus)
    xp_gain = int(currency_gain * 0.5) # L'XP suit la monnaie
    
    player.xp += xp_gain
    player.gatcha_coins += currency_gain
    
    # Level up logic
    xp_needed = player.level * 100
    levels_gained = 0
    while player.xp >= xp_needed:
        player.level += 1
        levels_gained += 1
        player.xp -= xp_needed
        player.gatcha_coins += 50  # Level up bonus
        xp_needed = player.level * 100
    
    player.save()
    
    # Create ProcessedTask record
    ProcessedTask.objects.create(
        task_id=task_id,
        task_title=title
    )
    
    return Response({
        'status': 'success',
        'task_id': task_id,
        'task_name': title,
        'reward_details': {
            'base': base_currency,
            'daily_bonus': daily_bonus,
            'streak_bonus': streak_multiplier,
            'is_crit': is_crit,
            'total_coins': currency_gain,
            'xp_gain': xp_gain
        },
        'levels_gained': levels_gained,
        'new_level': player.level,
        'current_xp': player.xp,
        'current_currency': player.gatcha_coins
    }, status=http_status.HTTP_201_CREATED)
