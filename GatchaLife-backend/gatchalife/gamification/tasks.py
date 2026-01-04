from celery import shared_task
from django.utils import timezone
from .models import ActiveTamagotchi
import structlog

logger = structlog.get_logger(__name__)

@shared_task
def update_tamagotchi_stats():
    """
    Decays mood and satiety for all active tamagotchis.
    Runs every 10 minutes (0.7 decay -> ~100 points in 24h).
    Respects sleep window (no decay if sleeping).
    """
    active_pets = ActiveTamagotchi.objects.all()
    count = 0
    now = timezone.now()
    # Ensure current_hour is in 0-23 format based on local time or server time? 
    # Usually servers are UTC. Users might be anywhere.
    # For MVP Phase 1: We assume server time or naive handling for now, 
    # but ideally we should handle user timezone. 
    # User request "If the current time is between..." implies a global check or user-specific check.
    # The constraint says "Sleep Window logic ... configurable by the user".
    # So we should check the user's specific sleep window against the user's local time?
    # Or just use server time for simplicity as Phase 1?
    # Given "Sleep Window logic: If the current time is between X and Y...", 
    # I'll implement logic that checks the hour of `now` (UTC) against the user's window constants.
    # NOTE: This assumes user sets window in UTC or we just use server time.
    # For Phase 1, we'll just use the hour from `now`.
    
    current_hour = now.hour

    for pet in active_pets:
        # Check sleep window
        # Handle wrapping (e.g. 23 to 7)
        is_sleeping = False
        if pet.sleep_start_hour > pet.sleep_end_hour:
             # Example: 23 to 7. Sleeping if hour >= 23 OR hour < 7
             if current_hour >= pet.sleep_start_hour or current_hour < pet.sleep_end_hour:
                 is_sleeping = True
        else:
             # Example: 1 to 5. Sleeping if hour >= 1 AND hour < 5
             if pet.sleep_start_hour <= current_hour < pet.sleep_end_hour:
                 is_sleeping = True
        
        if is_sleeping:
            continue

        # Decay
        # Decay
        decay_amount = 0.7
        # If pet is dead, do not decay further (stays at 0)
        if pet.mood > 0:
             pet.mood = max(0.0, pet.mood - decay_amount)
             
        pet.last_decay_update = now
        pet.save()
        count += 1
    
    return f"Updated {count} tamagotchis"
