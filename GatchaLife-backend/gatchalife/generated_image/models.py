from django.db import models

from gatchalife.character.models import CharacterVariant
from gatchalife.style.models import Style, Rarity, Theme


class GeneratedImage(models.Model):
    image = models.ImageField(upload_to="generated_images/")
    character_variant = models.ForeignKey(
        CharacterVariant, on_delete=models.CASCADE
    )
    rarity = models.ForeignKey(Rarity, on_delete=models.CASCADE)
    style = models.ForeignKey(Style, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"GeneratedImage {self.id} at {self.created_at}"
