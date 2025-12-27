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
from django.urls import reverse
from gatchalife.generated_image.services import generate_image, match_card_configuration
from gatchalife.generated_image.models import GeneratedImage
from django.conf import settings

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
            callback_url = request.build_absolute_uri(reverse("n8n-callback"))
            generate_image(
                card.character_variant,
                card.rarity,
                card.style,
                card.theme,
                pose=pose,
                card_configuration=matched_config,
                callback_url=callback_url,
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

    def list(self, request, *args, **kwargs):
        show_all = request.query_params.get("show_all") == "true"
        show_archived = request.query_params.get("show_archived") == "true"

        if not show_all and not show_archived:
            # Optimization: If not showing all, using standard list might suffice,
            # BUT standard list filters owned cards.
            # If user wants to see owned archived cards, standard list might hide them if standard filter_qs hides them?
            # Standard filter_qs does NOT hide legacy cards by default (unless I changed it).
            # Let's check filter_queryset. It just applies Rarity/Theme/etc.
            # So default behavior shows owned legacy cards.
            # But if show_all is False, we just return super().list().
            return super().list(request, *args, **kwargs)

        # --- Show All Logic ---
        player = get_default_player()

        # 1. Fetch base variants (applying character/series filters)
        variants_qs = CharacterVariant.objects.select_related("character")

        if not show_archived:
            variants_qs = variants_qs.filter(legacy=False, character__legacy=False)

        series_param = request.query_params.get("series")
        if series_param:
            variants_qs = variants_qs.filter(character__series__name=series_param)

        character_param = request.query_params.get("character")
        if character_param:
            variants_qs = variants_qs.filter(character__name__icontains=character_param)

        # 2. Fetch owned cards for mapping
        owned_user_cards = UserCard.objects.filter(player=player).select_related(
            "card",
            "card__character_variant",
            "card__character_variant__character",
            "card__rarity",
            "card__style",
            "card__theme",
        )

        # Map (VariantID, RarityName, StyleName, ThemeName) -> UserCard instance
        owned_map = {}
        for uc in owned_user_cards:
            c = uc.card
            key = (
                c.character_variant_id,
                c.rarity.name.upper(),
                c.style.name if c.style else None,
                c.theme.name if c.theme else None,
            )
            owned_map[key] = uc

        # 3. Build comprehensive list
        combined_list = []

        # Optimization: Prefetch all images for these variants to avoid N+1 in Serializer
        # We fetch all images for the variants we are about to process
        # This is much faster than querying per card
        all_images = (
            GeneratedImage.objects.filter(character_variant__in=variants_qs)
            .values(
                "character_variant_id",
                "rarity_id",
                "style_id",
                "theme_id",
                "image",
                "created_at",
            )
            .order_by("created_at")
        )

        # Build map: (v_id, r_id, s_id, t_id) -> image_url
        # Since we ordered by created_at, iterating will overwrite with latest
        image_map = {}
        for img in all_images:
            if img["image"]:
                key = (
                    img["character_variant_id"],
                    img["rarity_id"],
                    img["style_id"],
                    img["theme_id"],
                )
                # Construct URL manually to avoid object instantiation overhead
                # Assuming standard file storage configuration
                url = settings.MEDIA_URL + img["image"]
                image_map[key] = url

        # Prepare base context once
        base_context = self.get_serializer_context()
        base_context["image_map"] = image_map

        # Pre-fetch Rarity/Style/Theme objects for name lookup to ensure consistency if needed
        # But for constructing the "virtual" card, strings might be enough if Serializer handles it
        # Actually, we need to manually construct the dict to match Serializer output

        for variant in variants_qs:
            configs = variant.card_configurations_data or []
            for config in configs:
                if config.get("legacy") and not show_archived:
                    continue

                r_name = config.get("rarity", "").upper()
                s_name = config.get("style", {}).get("name")
                t_name = config.get("theme", {}).get("name")

                # Apply filters (Rarity, Style, Theme)
                if (
                    request.query_params.get("rarity")
                    and request.query_params.get("rarity").upper() != r_name
                ):
                    continue
                if (
                    request.query_params.get("style")
                    and request.query_params.get("style") != s_name
                ):
                    continue
                if (
                    request.query_params.get("theme")
                    and request.query_params.get("theme") != t_name
                ):
                    continue

                key = (variant.id, r_name, s_name, t_name)
                is_archived = (
                    variant.legacy
                    or variant.character.legacy
                    or config.get("legacy", False)
                )

                if key in owned_map:
                    # User owns it - serialize normally
                    # Use manual instantiation to pass optimized context
                    serializer = UserCardSerializer(
                        owned_map[key], context=base_context
                    )
                    combined_list.append(serializer.data)
                else:
                    # User doesn't own it - create placeholder
                    # REQUEST 404: Don't show uncollected cards if they are legacy
                    if is_archived:
                        continue

                    # Try to find image url from map for placeholder
                    # We need the IDs for the key.
                    # This is tricky because we only have names here.
                    # Ideally we should map names to IDs or change image_map key to names.
                    # But CardSerializer uses IDs.
                    # For virtual cards, we don't use CardSerializer (we assume None).
                    # Actually, we might want to show the image if it exists even if unowned?
                    # The current code sets "image_url": None.
                    # If we want to show image for unowned, we need to map names to IDs or use IDs if we have them.
                    # We have variant.id. But we don't have rarity_id easily without refreshing cache.
                    # However, the previous code essentially set image_url to None for virtual cards.
                    # So we ignore image_map for virtual cards for now.

                    combined_list.append(
                        {
                            "id": None,  # Virtual
                            "count": 0,
                            "obtained_at": None,
                            "card": {
                                "id": None,
                                "character_variant": variant.id,
                                "character_variant_name": variant.name,
                                "character_name": variant.character.name,
                                "series_name": variant.character.series.name
                                if variant.character.series
                                else "Unknown",
                                "rarity_name": r_name,
                                "style_name": s_name,
                                "theme_name": t_name,
                                "image_url": None,  # Placeholder trigger
                                "visual_override": variant.visual_override,
                                "description": variant.description,
                                "is_archived": is_archived,
                            },
                        }
                    )

        # 4. Pagination (Manual)
        page = self.paginate_queryset(combined_list)
        if page is not None:
            return self.get_paginated_response(page)

        return Response(combined_list)

    @action(detail=False, methods=["get"])
    def preview(self, request):
        variant_id = request.query_params.get("variant_id")
        rarity_name = request.query_params.get("rarity")
        style_name = request.query_params.get("style")
        theme_name = request.query_params.get("theme")

        if not all([variant_id, rarity_name]):
            return Response({"error": "Missing params"}, status=400)

        try:
            variant = CharacterVariant.objects.get(id=variant_id)
        except CharacterVariant.DoesNotExist:
            return Response({"error": "Variant not found"}, status=404)

        configs = variant.card_configurations_data or []
        target_config = None
        for c in configs:
            if (
                c.get("rarity", "").upper() == rarity_name.upper()
                and c.get("style", {}).get("name") == style_name
                and c.get("theme", {}).get("name") == theme_name
            ):
                target_config = c
                break

        if not target_config:
            return Response({"error": "Configuration not found"}, status=404)

        # Mock response
        data = {
            "id": None,
            "count": 0,
            "obtained_at": None,
            "card": {
                "id": None,
                "character_variant": variant.id,
                "character_variant_name": variant.name,
                "character_name": variant.character.name,
                "series_name": variant.character.series.name
                if variant.character.series
                else "Unknown",
                "rarity_name": rarity_name,
                "style_name": style_name,
                "theme_name": theme_name,
                "image_url": None,
                "visual_override": variant.visual_override,
                "description": variant.description,
                "pose": target_config.get("pose"),
                "is_archived": False,
            },
        }

        rarity_obj = Rarity.objects.filter(name__iexact=rarity_name).first()
        style_obj = Style.objects.filter(name=style_name).first()
        theme_obj = Theme.objects.filter(name=theme_name).first()

        # Careful: Style/Theme might be None if user passed 'None' string or empty, but logic above handles names.
        # If objects found, try to correct data with real card info if exists
        if rarity_obj:
            filters = {
                "character_variant": variant,
                "rarity": rarity_obj,
            }
            if style_obj:
                filters["style"] = style_obj
            if theme_obj:
                filters["theme"] = theme_obj

            real_card = Card.objects.filter(**filters).first()

            if real_card:
                from .serializers import (
                    CardSerializer,
                )  # Import here to avoid circular if any

                serializer = CardSerializer(real_card, context={"request": request})
                data["card"] = serializer.data

        return Response(data)

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

            callback_url = request.build_absolute_uri(reverse("n8n-callback"))

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
                        callback_url=callback_url,
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
