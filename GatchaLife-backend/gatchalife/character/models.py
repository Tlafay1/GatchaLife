from django.db import models

class Series(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Character(models.Model):
    # ... (Same as before)
    name = models.CharField(max_length=100)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class CharacterVariant(models.Model):
    character = models.ForeignKey(Character, related_name='variants', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.character.name} ({self.name})"

class VariantReferenceImage(models.Model):
    """
    Stores multiple reference images for a single variant.
    """
    variant = models.ForeignKey(CharacterVariant, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ref_images/')
    
    def __str__(self):
        return f"Image for {self.variant.character.name} - {self.variant.name}"
