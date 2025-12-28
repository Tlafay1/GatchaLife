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
    permission_classes = [permissions.AllowAny]  # For now, as per project settings

    @action(detail=False, methods=["get"])
    def stats(self, request):
        # Total completed tasks (status 2)
        total_completed = ProcessedTask.objects.count()  # All rewarded tasks

        today = timezone.now().date()
        processed_today = ProcessedTask.objects.filter(processed_at__date=today).count()
        total_processed = ProcessedTask.objects.count()

        # Recent tasks (from ProcessedTask)
        recent_processed = ProcessedTask.objects.order_by("-processed_at")[:5]

        recent_activity = []
        for p in recent_processed:
            recent_activity.append(
                {
                    "id": p.task_id,
                    "title": p.task_title or f"Task {p.task_id}",
                    "project": None,
                    "processed_at": p.processed_at,
                    "xp_gain": p.xp_gain,
                    "coin_gain": p.coin_gain,
                    "difficulty": p.difficulty,
                    "is_crit": p.is_crit,
                }
            )

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

        return Response(
            {
                "total_completed_all_time": total_completed,
                "rewarded_total": total_processed,
                "rewarded_today": processed_today,
                "recent_activity": recent_activity,
                "current_streak": current_streak,
            }
        )

    @action(detail=False, methods=["get"])
    def history(self, request):
        """
        Returns full history of processed tasks with all reward details.
        """
        # Simple pagination
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 20))
        start = (page - 1) * page_size
        end = start + page_size

        tasks = ProcessedTask.objects.order_by("-processed_at")[start:end]
        total = ProcessedTask.objects.count()

        data = []
        for t in tasks:
            data.append(
                {
                    "id": t.task_id,
                    "title": t.task_title,
                    "processed_at": t.processed_at,
                    "xp_gain": t.xp_gain,
                    "coin_gain": t.coin_gain,
                    "difficulty": t.difficulty,
                    "is_crit": t.is_crit,
                    "crit_multiplier": t.crit_multiplier,
                    "base_reward": t.base_reward,
                    "streak_multiplier": t.streak_multiplier,
                    "daily_bonus": t.daily_bonus,
                }
            )

        return Response(
            {
                "results": data,
                "total": total,
                "page": page,
                "pages": (total + page_size - 1) // page_size,
            }
        )

    @action(detail=False, methods=["post"])
    def manual_task(self, request):
        """
        Manually complete a task without webhook.
        Payload: { "title": "...", "difficulty": "medium", "tags": [...] }
        """
        from .services import process_completed_task
        from django.contrib.auth.models import User
        import uuid

        title = request.data.get("title", "Manual Task")
        # If difficulty provided directly, use it to fake a tag, or rely on tags
        difficulty = request.data.get("difficulty", "easy")
        tags = request.data.get("tags", [])
        
        # Ensure difficulty tag is present if passed explicitly
        if difficulty and difficulty.lower() not in [t.lower() for t in tags]:
            tags.append(difficulty.lower())

        # Generate a synthetic ID
        task_id = f"manual_{uuid.uuid4().hex[:8]}"
        
        user = User.objects.first() # Default user logic from before
        if not user:
            user = User.objects.create(username="Player1")

        result = process_completed_task(task_id, title, tags, user)
        
        if result.get("status") == "already_processed":
             return Response(result, status=http_status.HTTP_200_OK)
             
        return Response(result, status=http_status.HTTP_201_CREATED)


@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def zapier_webhook(request):
    """
    Webhook endpoint for Zapier to call when a task is completed.
    """
    from gatchalife.gamification.models import Player
    from django.contrib.auth.models import User
    from .services import process_completed_task

    # Get task data from Zapier (using their field names)
    # FIXME: Couldn't get zapier to send JSON body properly, so using form-encoded 'data' field
    data = request.data
    task_id = data.get("id")
    title = data.get("task_name", "Unknown Task")

    logger.info("webhook_received", task_id=task_id, title=title, raw_data=data)

    if not task_id:
        logger.error("webhook_missing_id", data=data)
        return Response(
            {"error": "id is required"}, status=http_status.HTTP_400_BAD_REQUEST
        )

    # Get the default player
    user = User.objects.first()
    if not user:
        user = User.objects.create(username="Player1")

    # Parse tags
    raw_tags_input = data.get("tag", data.get("tags", []))
    raw_tags = []
    if isinstance(raw_tags_input, str):
        cleaned_input = raw_tags_input.replace(",", " ")
        parts = cleaned_input.split()
        raw_tags = [p.strip() for p in parts if p.strip()]
    elif isinstance(raw_tags_input, list):
        raw_tags = raw_tags_input

    result = process_completed_task(task_id, title, raw_tags, user)

    status_code = http_status.HTTP_200_OK if result.get("status") == "already_processed" else http_status.HTTP_201_CREATED
    return Response(result, status=status_code)
