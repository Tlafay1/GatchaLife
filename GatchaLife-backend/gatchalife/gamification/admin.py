from django.contrib import admin
from .models import (
    Player,
    Quest,
    PlayerQuest,
    Card,
    UserCard,
    ActiveTamagotchi,
    CompanionImage,
)

admin.site.register(Player)
admin.site.register(Quest)
admin.site.register(PlayerQuest)
admin.site.register(Card)
admin.site.register(UserCard)
admin.site.register(ActiveTamagotchi)
admin.site.register(CompanionImage)
