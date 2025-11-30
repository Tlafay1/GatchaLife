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
    
    Expected payload:
    {
        "task_id": "string",
        "title": "string",
        "project_id": "string" (optional),
        "completed_at": "ISO datetime" (optional)
    }
    """
    from gatchalife.gamification.models import Player
    from django.contrib.auth.models import User
    
    # Get task data from Zapier
    task_id = request.data.get('task_id') or request.data.get('id')
    title = request.data.get('title', 'Unknown Task')
    
    if not task_id:
        return Response({
            'error': 'task_id is required'
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
    
    # Award rewards
    xp_gain = 10
    currency_gain = 5
    
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
        'xp_gained': xp_gain,
        'currency_gained': currency_gain,
        'levels_gained': levels_gained,
        'new_level': player.level,
        'current_xp': player.xp,
        'current_currency': player.gatcha_coins
    }, status=http_status.HTTP_201_CREATED)
