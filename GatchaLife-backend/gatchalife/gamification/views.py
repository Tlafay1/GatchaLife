from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Player, PlayerQuest, Card, UserCard
from .serializers import PlayerSerializer, PlayerQuestSerializer, UserCardSerializer
from gatchalife.character.models import CharacterVariant
from gatchalife.style.models import Rarity, Style, Theme
import random
import structlog
from gatchalife.generated_image.services import generate_image, match_card_configuration
from gatchalife.generated_image.models import GeneratedImage

logger = structlog.get_logger(__name__)

def get_default_player():
    # Get the first user or create a default one
    user = User.objects.first()
    if not user:
        user = User.objects.create(username='Player1')
    player, _ = Player.objects.get_or_create(user=user)
    return player

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return get_default_player()

class PlayerQuestViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlayerQuestSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        player = get_default_player()
        return PlayerQuest.objects.filter(player=player)

    @action(detail=True, methods=['post'])
    def claim(self, request, pk=None):
        player_quest = self.get_object()
        if player_quest.completed and not player_quest.claimed:
            player = player_quest.player
            player.xp += player_quest.quest.xp_reward
            player.gatcha_coins += player_quest.quest.currency_reward
            player.save()
            
            player_quest.claimed = True
            player_quest.save()
            return Response({'status': 'claimed'})
        return Response({'error': 'Cannot claim reward'}, status=status.HTTP_400_BAD_REQUEST)

class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserCardSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        player = get_default_player()
        queryset = UserCard.objects.filter(player=player)
        return queryset
            
        return queryset

    @action(detail=True, methods=["post"])
    def reroll_image(self, request, pk=None):
        user_card = self.get_object()
        card = user_card.card

        logger.info(
            "Rerolling image...",
            card_id=card.id,
            variant=card.character_variant.name,
            rarity=card.rarity.name,
            style=card.style.name,
            theme=card.theme.name,
        )

        # Lookup configuration
        matched_config = match_card_configuration(
            card.character_variant, card.rarity, card.style, card.theme
        )
        pose = matched_config.get("pose") if matched_config else None

        if pose:
            logger.info("Found configuration for reroll", pose=pose)
        else:
            logger.info(
                "No exact configuration matched for reroll, generating without specific pose"
            )

        try:
            generate_image(
                card.character_variant,
                card.rarity,
                card.style,
                card.theme,
                pose=pose,
                card_configuration=matched_config,
            )
            # Re-fetch serializer to get new image URL
            # We need to invalidate the prefetch cache if any, or just re-serialize
            # Since generate_image creates a new DB row, re-serializing should pick it up
            # if the serializer method performs a fresh query.
            # CardSerializer.get_image_url performs a fresh query.
            serializer = self.get_serializer(user_card)
            return Response(serializer.data)
        except Exception as e:
            logger.error("image_regeneration_failed", error=str(e))
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        
        rarity = self.request.query_params.get('rarity')
        if rarity:
            queryset = queryset.filter(card__rarity__name=rarity)
            
        theme = self.request.query_params.get('theme')
        if theme:
            queryset = queryset.filter(card__theme__name=theme)
            
        character = self.request.query_params.get('character')
        if character:
            queryset = queryset.filter(card__character_variant__character__name__icontains=character)
            
        style = self.request.query_params.get('style')
        if style:
            queryset = queryset.filter(card__style__name=style)
            
        series = self.request.query_params.get('series')
        if series:
            queryset = queryset.filter(card__character_variant__character__series__name=series)
            
        return queryset


class GatchaViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["post"])
    def roll(self, request):
        player = get_default_player()
        cost = 100

        if player.gatcha_coins < cost:
            return Response(
                {"error": "Not enough coins"}, status=status.HTTP_400_BAD_REQUEST
            )

        player.gatcha_coins -= cost
        player.save()

        drops_data = [] # List of dicts with selected r, variant, style, theme
        rarities = Rarity.objects.all()
        if not rarities.exists():
            return Response(
                {"error": "No rarities defined"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        ordered_rarities = list(rarities.order_by("-min_roll_threshold"))
        fallback_rarity = rarities.order_by("min_roll_threshold").first()

        # --- STEP 1: Determine Drop Outcomes ---
        # Pre-fetch all variants with their configs to avoid N+1 equivalent in loop
        # Exclude legacy characters and legacy variants
        all_variants = list(
            CharacterVariant.objects.filter(
                character__legacy=False, legacy=False
            ).select_related("character")
        )
        
        # Map rarity names for easier lookup
        # Assuming Rarity.name matches the keys in JSON (e.g. "COMMON", "RARE") case-insensitivity might be needed

        attempts = 0
        max_attempts = 20  # Safety break

        while len(drops_data) < 5 and attempts < max_attempts:
            attempts += 1
            # ... (Roll Logic kept same) ...
            base_roll = random.randint(1, 100)
            level_bonus = min(player.level * 0.5, 20.0)
            final_roll = min(base_roll + level_bonus, 100)

            selected_rarity = None
            for r in ordered_rarities:
                if final_roll >= r.min_roll_threshold:
                    selected_rarity = r
                    break
            if not selected_rarity:
                selected_rarity = fallback_rarity

            # Flatten probability: Collect all valid (variant, config) pairs for this rarity
            valid_cards = []
            for v in all_variants:
                configs = v.card_configurations_data
                for c in configs:
                    if c.get(
                        "rarity", ""
                    ).upper() == selected_rarity.name.upper() and not c.get("legacy"):
                        valid_cards.append({"variant": v, "config": c})

            if not valid_cards:
                # Fallback: Pick any variant from valid ones for this rarity
                selection = {
                    "variant": random.choice(all_variants) if all_variants else None,
                    "config": {},
                }
                if selection["variant"]:
                    configs = selection["variant"].card_configurations_data or []
                    valid_configs = [c for c in configs if not c.get("legacy")]
                    selection["config"] = (
                        random.choice(valid_configs) if valid_configs else {}
                    )
            else:
                selection = random.choice(valid_cards)

            if not selection.get("variant"):
                continue

            variant = selection["variant"]
            target_config = selection["config"]

            # Resolve Style and Theme from Config
            style_name = target_config.get('style', {}).get('name')
            theme_name = target_config.get('theme', {}).get('name')
            pose_prompt = target_config.get('pose', '')
            
            style = None
            theme = None
            
            if style_name:
                style = Style.objects.filter(
                    name=style_name, rarity=selected_rarity
                ).first()
                if not style:
                     style = Style.objects.filter(name=style_name).first()

            if theme_name:
                theme = Theme.objects.filter(name=theme_name).first()

            # Double Fallback if not found
            if not style:
                style = Style.objects.filter(rarity=selected_rarity).first() or Style.objects.first()
            if not theme:
                theme = Theme.objects.first()

            # Check if this specific card combination is archived (legacy)
            existing_card = Card.objects.filter(
                character_variant=variant,
                rarity=selected_rarity,
                style=style,
                theme=theme,
            ).first()

            if existing_card and existing_card.legacy:
                logger.info("Skipping legacy card drop", card=existing_card)
                continue

            drops_data.append({
                "variant": variant,
                "rarity": selected_rarity,
                "style": style,
                "theme": theme,
                "pose": pose_prompt,
                "card_configuration": target_config, # Pass full config
                "roll_info": {
                    "base_roll": base_roll,
                    "level_bonus": level_bonus,
                    "final_roll": final_roll,
                    "rarity": selected_rarity.name,
                }
            })

        # --- STEP 2: Identify Missing Images (Deduplicated) ---
        # Deduplicate tasks by (Variant, Rarity, Style, Theme) key.
        # We process the first encountered configuration for any given key.
        tasks_map = {} 
        for d in drops_data:
             key = (d["variant"], d["rarity"], d["style"], d["theme"])
             if key not in tasks_map:
                 tasks_map[key] = d["card_configuration"]
        
        missing_combinations = []
        # Check DB
        for (variant, r, s, t), config in tasks_map.items():
            if not GeneratedImage.objects.filter(character_variant=variant, rarity=r, style=s, theme=t).exists():
                missing_combinations.append((variant, r, s, t, config)) # Pass config instead of just pose

        # --- STEP 3: Parallel Generation ---
        if missing_combinations:
            from concurrent.futures import ThreadPoolExecutor, as_completed
            
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {
                    executor.submit(
                        generate_image,
                        variant,
                        r,
                        s,
                        t,
                        pose=config.get("pose"),
                        card_configuration=config,
                    ): (variant, r, s, t)
                    for (variant, r, s, t, config) in missing_combinations
                }
                
                for future in as_completed(futures):
                    combo = futures[future]
                    try:
                        future.result() # Wait for completion, raise exception if any
                    except Exception as e:
                        logger.error("image_generation_failed", combo=combo, error=str(e))
                        # We continue even if one fails, to give the user their cards (even if image is missing)

        # --- STEP 4: Create Cards and UserCards ---
        final_drops = []
        for d in drops_data:
            card, _ = Card.objects.get_or_create(
                character_variant=d["variant"],
                rarity=d["rarity"],
                style=d["style"],
                theme=d["theme"],
            )

            user_card, created_user_card = UserCard.objects.get_or_create(
                player=player, card=card
            )
            if not created_user_card:
                user_card.count += 1
                user_card.save()

            serializer = UserCardSerializer(user_card, context={"request": request})
            drop_item = serializer.data
            drop_item["is_new"] = created_user_card
            drop_item["roll_info"] = d["roll_info"]
            final_drops.append(drop_item)

        return Response(
            {
                "drops": final_drops,
                "remaining_coins": player.gatcha_coins,
            }
        )
