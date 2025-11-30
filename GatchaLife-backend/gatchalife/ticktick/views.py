from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import TickTickTask, ProcessedTask, TickTickProject

class TickTickViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny] # For now, as per project settings

    @action(detail=False, methods=['get'])
    def stats(self, request):
        # Total completed tasks (status 2)
        total_completed = TickTickTask.objects.filter(status=2).count()
        
        # Tasks completed today (using last_synced_at as a proxy for now, or we need a completed_at field if n8n provides it)
        # The n8n schema has 'completedTime' removed? Let's check models.py again.
        # In models.py, completedTime was removed from the schema in the n8n JSON but let's check if I put it in the model.
        # I did NOT put completedTime in the model. I only have last_synced_at.
        # However, ProcessedTask has processed_at. We can use that for "Tasks Rewarded Today".
        
        today = timezone.now().date()
        processed_today = ProcessedTask.objects.filter(processed_at__date=today).count()
        total_processed = ProcessedTask.objects.count()
        
        # Recent tasks (from ProcessedTask joined with TickTickTask)
        recent_processed = ProcessedTask.objects.order_by('-processed_at')[:5]
        
        # Since ProcessedTask only has task_id (string), we can't easily select_related.
        # We have to fetch the IDs and then query TickTickTask.
        recent_ids = [p.task_id for p in recent_processed]
        # Fetch tasks, preserving order is tricky with IN clause, so we map them in python
        tasks_map = {t.id: t for t in TickTickTask.objects.filter(id__in=recent_ids)}
        
        recent_activity = []
        for p in recent_processed:
            task = tasks_map.get(p.task_id)
            if task:
                recent_activity.append({
                    'id': task.id,
                    'title': task.title,
                    'project': task.projectId, # We could fetch project name too
                    'processed_at': p.processed_at
                })
                
        # Project breakdown (top 5 projects by completed tasks)
        # This is harder without a direct FK. 
        # Let's just return simple stats for now.
        
        return Response({
            'total_completed_all_time': total_completed,
            'rewarded_total': total_processed,
            'rewarded_today': processed_today,
            'recent_activity': recent_activity
        })
