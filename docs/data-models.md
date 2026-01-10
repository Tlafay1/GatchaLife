# Data Models - GatchaLife

This document describes the core database entities in the GatchaLife system.

## Character System
- **Series:** Groups characters (e.g., "Genshin Impact", "Originals").
- **Character:** Primary entity with metadata (name, description, wiki source).
- **CharacterVariant:** Variations of a character (costumes, forms).
- **VariantReferenceImage:** Source images used for AI variant generation.

## Gamification System
- **Player:** Central entity for tracking currency, experience, levels, and streaks.
- **Card:** Definitive list of collectible cards.
- **UserCard:** Instance of a card owned by a player (with quantity).
- **ActiveTamagotchi:** Current companion being nurtured by the player (with hunger, mood, etc.).
- **CompanionImage:** Visual assets for different companion states (normal, feeding, sleeping).

## Style & Rarity
- **Rarity:** Defines drop rates and visual hierarchy (Common, Rare, SSR, etc.).
- **Style:** Artistic styles for images/cards.
- **Theme:** Broad visual themes.

## Task Integration (TickTick)
- **TickTickProject / Column:** Mirror of the external task organization.
- **TickTickTask:** Tracks external tasks and their completion status.
- **ProcessedTask:** Log of tasks that have already granted rewards to the player.

## Async Jobs
- **AsyncJob:** Tracks the progress and results of background tasks (e.g., AI generations).
