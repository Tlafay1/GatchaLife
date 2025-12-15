import json
import random
from datetime import timedelta
from django.utils import timezone
from .models import ProcessedTask, TickTickTask
import structlog

logger = structlog.get_logger(__name__)

def process_completed_task(task_id, title, raw_tags, user):
    """
    Processes a completed task, calculates rewards, updates player stats, 
    and returns the result details.
    """
    from gatchalife.gamification.models import Player
    
    # Check if we've already processed this task
    if ProcessedTask.objects.filter(task_id=task_id).exists():
        logger.info("task_already_processed", task_id=task_id)
        return {
            "status": "already_processed",
            "message": f"Task {task_id} has already been rewarded",
        }

    # Get the default player (or specific user's player)
    player, _ = Player.objects.get_or_create(user=user)

    difficulty = "easy"
    difficulty_multiplier = 1.0

    # Check for difficulty tags
    for tag in raw_tags:
        lower_tag = tag.lower()
        if "extreme" in lower_tag:
            difficulty = "extreme"
            difficulty_multiplier = 3.0
            break
        elif "hard" in lower_tag:
            difficulty = "hard"
            difficulty_multiplier = 2.0
            break
        elif "medium" in lower_tag:
            difficulty = "medium"
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
            daily_bonus = 50 

            if last_date == today - timedelta(days=1):
                player.current_streak += 1
            else:
                player.current_streak = 1
    else:
        # Tout premier jour
        daily_bonus = 100
        player.current_streak = 1

    player.last_activity_date = now

    # 2. Calcul de la récompense variable (Skinner Box)
    base_currency = random.randint(15, 25)

    # 3. Multiplicateur de Streak (Max x1.5)
    streak_multiplier = 1 + min(player.current_streak * 0.05, 0.5)

    # 4. Critique / Jackpot (10% de chance de x2)
    is_crit = random.random() < 0.10
    crit_multiplier = 2.0 if is_crit else 1.0

    # Calcul Final
    currency_gain = int(
        (base_currency * difficulty_multiplier * streak_multiplier * crit_multiplier)
        + daily_bonus
    )
    xp_gain = int(currency_gain * 0.5)

    logger.info(
        "reward_calculated",
        task_id=task_id,
        currency_gain=currency_gain,
        xp_gain=xp_gain,
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
        player.gatcha_coins += 50
        xp_needed = player.level * 100
        logger.info("level_up", new_level=player.level, player=player.user.username)

    player.save()

    # Create ProcessedTask record
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
        tags=json.dumps(raw_tags),
    )

    return {
        "status": "success",
        "task_id": task_id,
        "task_name": title,
        "reward_details": {
            "base": base_currency,
            "difficulty": difficulty,
            "difficulty_multiplier": difficulty_multiplier,
            "daily_bonus": daily_bonus,
            "streak_bonus": streak_multiplier,
            "is_crit": is_crit,
            "crit_multiplier": crit_multiplier,
            "total_coins": currency_gain,
            "xp_gain": xp_gain,
        },
        "levels_gained": levels_gained,
        "new_level": player.level,
        "current_xp": player.xp,
        "current_currency": player.gatcha_coins,
    }
