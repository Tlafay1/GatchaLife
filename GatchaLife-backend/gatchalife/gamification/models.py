from django.db import models
from django.conf import settings
from gatchalife.character.models import CharacterVariant
from gatchalife.style.models import Rarity, Style, Theme

class Player(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default=1)
    xp = models.PositiveIntegerField(default=0)
    gatcha_coins = models.PositiveIntegerField(default=0)
    ticktick_api_key = models.CharField(max_length=255, blank=True, null=True)
    last_activity_date = models.DateTimeField(null=True, blank=True)
    current_streak = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} (Lvl {self.level})"

class Quest(models.Model):
    QUEST_TYPES = (
        ('DAILY', 'Daily'),
        ('ACHIEVEMENT', 'Achievement'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    xp_reward = models.PositiveIntegerField(default=10)
    currency_reward = models.PositiveIntegerField(default=10)
    type = models.CharField(max_length=20, choices=QUEST_TYPES, default='DAILY')
    condition_key = models.CharField(max_length=100, help_text="Key to identify the condition in code (e.g., 'task_completed')")

    def __str__(self):
        return self.title

class PlayerQuest(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='quests')
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    progress = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    claimed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.player.user.username} - {self.quest.title}"

class Card(models.Model):
    character_variant = models.ForeignKey(CharacterVariant, on_delete=models.CASCADE)
    rarity = models.ForeignKey(Rarity, on_delete=models.CASCADE)
    style = models.ForeignKey(Style, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('character_variant', 'rarity', 'style', 'theme')

    def __str__(self):
        return f"{self.character_variant.name} - {self.rarity.name}"

class UserCard(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='cards')
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
    obtained_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('player', 'card')

    def __str__(self):
        return f"{self.player.user.username} - {self.card} (x{self.count})"

class DailyCompanionState(models.Model):
    MOOD_CHOICES = (
        ("SAD", "Sad"),
        ("NEUTRAL", "Neutral"),
        ("HAPPY", "Happy"),
        ("EXCITED", "Excited"),
    )

    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="daily_states"
    )
    date = models.DateField()
    character_name = models.CharField(max_length=100)
    mood_state = models.CharField(
        max_length=20, choices=MOOD_CHOICES, default="NEUTRAL"
    )
    image = models.ImageField(upload_to="companion_daily/", blank=True, null=True)
    image_url = models.URLField(
        max_length=500, blank=True, null=True
    )  # Fallback if using external URL
    dialogue_text = models.TextField(blank=True)
    productivity_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("player", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.player.user.username} - {self.date} - {self.mood_state}"
