# 0002_populate_gacha_rules.py
from django.db import migrations


def create_initial_rarities(apps, schema_editor):
    Rarity = apps.get_model("style", "Rarity")
    Rarity.objects.bulk_create(
        [
            Rarity(name="Common", min_roll_threshold=0, ui_color_hex="#AAAAAA"),
            Rarity(name="Rare", min_roll_threshold=80, ui_color_hex="#007BFF"),
            Rarity(name="Legendary", min_roll_threshold=95, ui_color_hex="#FFD700"),
        ]
    )


def create_initial_styles(apps, schema_editor):
    Style = apps.get_model("style", "Style")
    Rarity = apps.get_model("style", "Rarity")

    common = Rarity.objects.get(name="Common")
    rare = Rarity.objects.get(name="Rare")
    legendary = Rarity.objects.get(name="Legendary")

    Style.objects.bulk_create(
        [
            Style(
                rarity=common,
                name="Chibi Mignon",
                style_keywords="chibi style, cute, simple, large head, minimal details, sticker style, vector art, bright colors",
                composition_hint="Personnage en pose simple et mignonne. Le thème de fond doit être très simplifié...",
            ),
            Style(
                rarity=common,
                name="Croquis Rapide",
                style_keywords="anime manga sketch style, clean line art, monochrome, black and white, hatching, dynamic lines",
                composition_hint="Focus sur un portrait ou un buste du personnage.",
            ),
            Style(
                rarity=rare,
                name="Style Anime (Cel Shading)",
                style_keywords="high-quality anime cel shading, vibrant colors, crisp outlines, trending on pixiv, modern anime style, detailed character design",
                composition_hint="Personnage en pose dynamique, bien intégré dans le thème.",
            ),
            Style(
                rarity=rare,
                name="Aquarelle Douce",
                style_keywords="anime watercolor illustration, soft pastel colors, gentle smile, blooming effects, textured paper, artistic, elegant",
                composition_hint="Pose plus calme et contemplative.",
            ),
            Style(
                rarity=legendary,
                name="Splash Art Épique",
                style_keywords="cinematic splash art, epic, triumphant pose, detailed outfit, dramatic lighting, god rays, particle effects, highly detailed digital painting, 8k, masterpiece, trending on artstation, unreal engine 5",
                composition_hint="Scène complète. Utiliser la pose la plus dynamique...",
            ),
            Style(
                rarity=legendary,
                name="Vitrail Héroïque",
                style_keywords="Stained glass window art, heroic pose, vibrant saturated colors, bold black outlines, glowing light from behind, gothic style, ornate decorative frame, masterpiece",
                composition_hint="Le personnage est immortalisé.",
            ),
        ]
    )


def create_initial_themes(apps, schema_editor):
    Theme = apps.get_model("style", "Theme")
    Theme.objects.bulk_create(
        [
            Theme(
                name="Cyber-espace Néon",
                category="Technologie",
                ambiance="High-tech, digital, nocturne, mystérieux",
                keywords_theme="flux de données, grille néon, hologramme, code binaire, réflexions",
                prompt_background="Un paysage de données high-tech, digital et nocturne. Des grilles néon s'étendent à l'infini...",
                integration_idea="Le personnage interagit avec un hologramme, marche sur la grille néon...",
            ),
            Theme(
                name="Repaire du Hacker",
                category="Technologie",
                ambiance="Sombre, concentré, éclairé par les écrans",
                keywords_theme="moniteurs multiples, lignes de code, câbles emmêlés, tasse de café, clavier mécanique",
                prompt_background="Une pièce sombre et encombrée, dont la seule lumière provient de multiples écrans...",
                integration_idea="Le personnage est assis au bureau, concentré sur les écrans...",
            ),
            # ... Collez TOUS vos autres thèmes ici ...
            Theme(
                name="Plage Tropicale",
                category="Détente",
                ambiance="Relaxant, vacances, sérénité, chaleur",
                keywords_theme="mer turquoise, sable fin, palmiers, soleil, transat, cocktail",
                prompt_background="Une plage de sable blanc immaculée, une mer turquoise calme...",
                integration_idea="Le personnage est allongé sur un transat avec un cocktail...",
            ),
        ]
    )


class Migration(migrations.Migration):

    dependencies = [
        ("style", "0002_alter_rarity_options_and_more"),
    ]

    operations = [
        migrations.RunPython(create_initial_rarities),
        migrations.RunPython(create_initial_styles),
        migrations.RunPython(create_initial_themes),
    ]
