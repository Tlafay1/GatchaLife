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
import structlog

logger = structlog.get_logger(__name__)

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
                'processed_at': p.processed_at,
                'xp_gain': p.xp_gain,
                'coin_gain': p.coin_gain,
                'difficulty': p.difficulty,
                'is_crit': p.is_crit
            })
                
        # Get player streak
        from gatchalife.gamification.models import Player
        from django.contrib.auth.models import User
        
        current_streak = 0
        user = User.objects.first()
        if user:
            player = Player.objects.filter(user=user).first()
            if player and player.last_activity_date:
                last_date = player.last_activity_date.date()
                # If last activity was today or yesterday, streak is active
                if last_date >= today - timedelta(days=1):
                    current_streak = player.current_streak

        return Response({
            'total_completed_all_time': total_completed,
            'rewarded_total': total_processed,
            'rewarded_today': processed_today,
            'recent_activity': recent_activity,
            'current_streak': current_streak
        })

    @action(detail=False, methods=['get'])
    def history(self, request):
        """
        Returns full history of processed tasks with all reward details.
        """
        # Simple pagination
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        start = (page - 1) * page_size
        end = start + page_size
        
        tasks = ProcessedTask.objects.order_by('-processed_at')[start:end]
        total = ProcessedTask.objects.count()
        
        data = []
        for t in tasks:
            data.append({
                'id': t.task_id,
                'title': t.task_title,
                'processed_at': t.processed_at,
                'xp_gain': t.xp_gain,
                'coin_gain': t.coin_gain,
                'difficulty': t.difficulty,
                'is_crit': t.is_crit,
                'crit_multiplier': t.crit_multiplier,
                'base_reward': t.base_reward,
                'streak_multiplier': t.streak_multiplier,
                'daily_bonus': t.daily_bonus
            })
            
        return Response({
            'results': data,
            'total': total,
            'page': page,
            'pages': (total + page_size - 1) // page_size
        })

    @action(detail=False, methods=['get'])
    def progression(self, request):
        """
        Returns daily aggregated XP and Coin stats for the last 30 days.
        """
        from django.db.models import Sum
        from django.db.models.functions import TruncDate
        
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        daily_stats = ProcessedTask.objects.filter(processed_at__gte=thirty_days_ago)\
            .annotate(date=TruncDate('processed_at'))\
            .values('date')\
            .annotate(total_xp=Sum('xp_gain'), total_coins=Sum('coin_gain'))\
            .order_by('date')
            
        return Response(daily_stats)

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

    logger.info("webhook_received", task_id=task_id, title=title, raw_data=data)

    if not task_id:
        logger.error("webhook_missing_id", data=data)
        return Response({
            'error': 'id is required'
        }, status=http_status.HTTP_400_BAD_REQUEST)

    # Check if we've already processed this task
    if ProcessedTask.objects.filter(task_id=task_id).exists():
        logger.info("task_already_processed", task_id=task_id)
        return Response({
            'status': 'already_processed',
            'message': f'Task {task_id} has already been rewarded'
        }, status=http_status.HTTP_200_OK)

    # Get the default player
    user = User.objects.first()
    if not user:
        user = User.objects.create(username='Player1')
    player, _ = Player.objects.get_or_create(user=user)

    # Parse tags to determine difficulty
    # Zapier might send tags as a list or a string depending on how it's configured
    # We'll try to handle both or just assume it's passed in 'data'
    raw_tags = data.get("tags", [])
    if isinstance(raw_tags, str):
        # If it's a string representation of a list or comma separated
        if raw_tags.startswith('['):
            try:
                raw_tags = json.loads(raw_tags)
            except:
                raw_tags = []
        else:
            raw_tags = [t.strip() for t in raw_tags.split(',')]

    difficulty = 'easy'
    difficulty_multiplier = 1.0

    # Check for difficulty tags
    for tag in raw_tags:
        lower_tag = tag.lower()
        if 'difficulty/extreme' in lower_tag:
            difficulty = 'extreme'
            difficulty_multiplier = 3.0
            break
        elif 'difficulty/hard' in lower_tag:
            difficulty = 'hard'
            difficulty_multiplier = 2.0
            break
        elif 'difficulty/medium' in lower_tag:
            difficulty = 'medium'
            difficulty_multiplier = 1.5
            break
        # Default is easy (1.0)

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
    # Base entre 15 et 25
    base_currency = random.randint(15, 25)

    # 3. Multiplicateur de Streak (Max x1.5)
    streak_multiplier = 1 + min(player.current_streak * 0.05, 0.5)

    # 4. Critique / Jackpot (10% de chance de x2 - reduced from x3 to balance difficulty)
    is_crit = random.random() < 0.10
    crit_multiplier = 2.0 if is_crit else 1.0

    # Calcul Final
    # Formula: (Base * Difficulty * Streak * Crit) + Daily Bonus
    currency_gain = int((base_currency * difficulty_multiplier * streak_multiplier * crit_multiplier) + daily_bonus)
    xp_gain = int(currency_gain * 0.5) # L'XP suit la monnaie

    logger.info("reward_calculated", 
        task_id=task_id, 
        currency_gain=currency_gain, 
        xp_gain=xp_gain,
        breakdown={
            'base': base_currency,
            'difficulty': difficulty,
            'streak_mult': streak_multiplier,
            'crit': is_crit,
            'daily_bonus': daily_bonus
        }
    )

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
        logger.info("level_up", new_level=player.level, player=player.user.username)

    player.save()

    # Create ProcessedTask record with full details
    ProcessedTask.objects.create(
        task_id=task_id,
        task_title=title,
        xp_gain=xp_gain,
        coin_gain=currency_gain,
        difficulty=difficulty,
        is_crit=is_crit,
        crit_multiplier=crit_multiplier,
        base_reward=base_currency,
        streak_multiplier=streak_multiplier,
        daily_bonus=daily_bonus,
        tags=json.dumps(raw_tags)
    )

    return Response({
        'status': 'success',
        'task_id': task_id,
        'task_name': title,
        'reward_details': {
            'base': base_currency,
            'difficulty': difficulty,
            'difficulty_multiplier': difficulty_multiplier,
            'daily_bonus': daily_bonus,
            'streak_bonus': streak_multiplier,
            'is_crit': is_crit,
            'crit_multiplier': crit_multiplier,
            'total_coins': currency_gain,
            'xp_gain': xp_gain
        },
        'levels_gained': levels_gained,
        'new_level': player.level,
        'current_xp': player.xp,
        'current_currency': player.gatcha_coins
    }, status=http_status.HTTP_201_CREATED)
