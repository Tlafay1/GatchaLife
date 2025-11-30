from django.contrib import admin
from .models import Player, Quest, PlayerQuest, Card, UserCard

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'xp', 'gatcha_coins')

@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'xp_reward', 'currency_reward')

@admin.register(PlayerQuest)
class PlayerQuestAdmin(admin.ModelAdmin):
    list_display = ('player', 'quest', 'completed', 'claimed')
    list_filter = ('completed', 'claimed')

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('character_variant', 'rarity', 'style', 'theme')
    list_filter = ('rarity', 'style', 'theme')

@admin.register(UserCard)
class UserCardAdmin(admin.ModelAdmin):
    list_display = ('player', 'card', 'count', 'obtained_at')
