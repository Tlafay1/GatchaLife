from django.db import models


class Rarity(models.Model):
    """
    Les règles de base du jeu. Ex: Common, Rare, Legendary.
    Créé via une migration de données, géré dans le code.
    """

    name = models.CharField(max_length=100, unique=True)
    # Seuil de 'roll' (0-100). Ex: Common=0, Rare=80, Legendary=95
    min_roll_threshold = models.PositiveIntegerField()
    # Couleur pour l'affichage dans le frontend
    ui_color_hex = models.CharField(max_length=7, default="#FFFFFF")

    class Meta:
        verbose_name_plural = "Rarities"

    def __str__(self):
        return self.name


class Style(models.Model):
    """
    Le style artistique. Ex: Chibi, Splash Art.
    Géré via le Django Admin.
    """

    name = models.CharField(max_length=100)
    # Un style est lié à une rareté (un style Chibi est TOUJOURS Common)
    rarity = models.ForeignKey(Rarity, on_delete=models.CASCADE, related_name="styles")
    style_keywords = models.TextField(
        blank=True, help_text="Prompts pour l'IA (ex: chibi style, cute, simple)"
    )
    composition_hint = models.TextField(
        blank=True, help_text="Rappel sur comment l'utiliser"
    )
    unlock_level = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.name} ({self.rarity.name})"


class Theme(models.Model):
    """
    Le contexte/background. Ex: Repaire du Hacker, Forêt Enchantée.
    Géré via le Django Admin.
    """

    name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=100, blank=True, help_text="Ex: Technologie, Fitness, Fantaisie"
    )
    ambiance = models.CharField(max_length=255, blank=True)
    keywords_theme = models.TextField(
        blank=True,
        help_text="Prompts pour l'IA (ex: moniteurs multiples, lignes de code)",
    )
    prompt_background = models.TextField(
        blank=True, help_text="Le prompt de fond complet pour l'IA"
    )
    integration_idea = models.TextField(
        blank=True, help_text="Rappel sur comment intégrer le personnage"
    )
    vibe_tags = models.JSONField(
        default=list, blank=True, help_text="Mots-clés de l'ambiance (ex: ['sacred', 'colorful light'])"
    )
    base_rarity_tier = models.PositiveIntegerField(
        default=1, help_text="1=Basic, 5=Legendary"
    )
    unlock_level = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name
