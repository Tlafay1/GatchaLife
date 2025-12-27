from django.db import models
from django.core.files.base import ContentFile
from io import BytesIO
import os
from PIL import Image  # Requires pillow

from gatchalife.character.models import CharacterVariant
from gatchalife.style.models import Style, Rarity, Theme

class GeneratedImage(models.Model):
    image = models.ImageField(upload_to="generated_images/")
    # Add this field
    thumbnail = models.ImageField(
        upload_to="generated_images/thumbnails/", null=True, blank=True
    )

    character_variant = models.ForeignKey(CharacterVariant, on_delete=models.CASCADE)
    rarity = models.ForeignKey(Rarity, on_delete=models.CASCADE)
    style = models.ForeignKey(Style, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"GeneratedImage {self.id} at {self.created_at}"

    def save(self, *args, **kwargs):
        # Automatically generate thumbnail if missing
        if self.image and not self.thumbnail:
            self.generate_thumbnail()
        super().save(*args, **kwargs)

    def generate_thumbnail(self):
        try:
            img = Image.open(self.image)
            # Convert to RGB if necessary (e.g. for PNG with transparency handling)
            if img.mode != "RGBA":
                img = img.convert("RGB")

            # Resize to a reasonable card width (e.g., 300px width)
            # Maintain aspect ratio
            img.thumbnail((300, 450), Image.Resampling.LANCZOS)

            thumb_io = BytesIO()
            # Save as PNG to preserve quality/transparency
            img.save(thumb_io, format="PNG", optimize=True)

            thumb_filename = f"thumb_{os.path.basename(self.image.name)}"
            # Save=False to avoid infinite recursion loop in save()
            self.thumbnail.save(
                thumb_filename, ContentFile(thumb_io.getvalue()), save=False
            )
        except Exception as e:
            # Log error but don't crash save
            print(f"Error generating thumbnail: {e}")