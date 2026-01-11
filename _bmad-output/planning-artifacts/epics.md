---
stepsCompleted: [1, 2, 3, 4]
inputDocuments:
  - "_bmad-output/planning-artifacts/prd.md"
  - "_bmad-output/planning-artifacts/architecture.md"
  - "_bmad-output/planning-artifacts/ux-design-specification.md"
---

# GatchaLife - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for GatchaLife, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR1: System must calculate "Mood Decay" based on time elapsed since last productive action.
FR2: System must determine "Companion State" strictly using these tiers: Extremely Happy (80-100%), Happy (60-80%), Neutral (40-60%), Pouting (20-40%), Very Distressed (1-20%), Dead (0%), Sleeping (Time-based override).
FR3: System must apply "Sleep State" logic during user-configured hours, freezing decay but preventing interaction.
FR4: System must enforce "Shadow State" (Lockout) when Mood reaches 0 (Dead), preventing equipping or use of the character.
FR5: System must apply a "Haunting Debuff" (50% Coin reduction) if any character in the roster is in Shadow State.
FR6: System must ingest Task Completion events from TickTick Webhooks (via n8n).
FR7: System must calculate XP and Coin rewards based on Task Difficulty (tagged in TickTick) and current multipliers (Companion Mood, Haunting Debuff, Streak).
FR8: System must update the Active Companion's Mood upon task completion (Healing), with healing amount scaled by Task Difficulty.
FR9: User can view current Coin balance (Unified Currency).
FR10: User can spend Coins to Purchase "Card Packs" (Gatcha) to acquire new characters.
FR11: User can spend Coins to Purchase "Rest Potions" (Consumables).
FR12: User can consume a "Rest Potion" to pause Mood Decay for [X] hours.
FR13: User can spend Coins to "Resurrect" a character in Shadow State, restoring them to Neutral Mood.
FR14: User can "Exorcise" (Delete) a character in Shadow State to remove the Haunting Debuff permanently.
FR15: User can view all owned characters in a "Roster" view.
FR16: User can "Equip" one character as the Active Companion.
FR17: Equipped character is the only one subject to Mood Decay and receiving XP.
FR18: Unequipped characters must remain in "Stasis" (Mood frozen).
FR19: Roster view must clearly indicate "Shadow/Locked" characters.
FR20: Mobile Widget must display the Active Companion's current Image (based on State).
FR21: Mobile Widget must display the Name of the highest priority pending Task from TickTick.
FR22: Mobile Widget periodically polls (15-30m) or receive push updates for State changes.
FR24: User can input a text prompt to generate a new Character appearance (via AI).
FR25: System must generate a unique image based on the prompt.
FR26: User can "Save/Mint" the generated character into their collection.

### NonFunctional Requirements

NFR1: Mobile Widget "Task View" must load and become interactive within <2 seconds.
NFR2: AI-generated visuals must maintain a consistent style (Anime/Gatcha) via fixed negative prompt engineering to prevent jarring visual quality shifts.
NFR3: Background sync services (Widget polling) must consume < 2% of daily battery life on Android devices.
NFR4: Task completion on one device (e.g., Desktop TickTick) must reflect on the Mobile Widget within 15 minutes (polling interval) or immediately via Push (if fully implemented).
NFR5: The "Haunting Debuff" calculation must be atomic; race conditions between task completion and mood decay updates must default to the user's benefit.
NFR6: Companion images (often large AI files) must be cached locally on mobile devices. Subsequent loads of the same mood/state must be instant (<100ms).
NFR7: Character creation (Forge) should complete within < 30 seconds to maintain the "impulse" excitement.

### Additional Requirements

- **Starter Template:** Existing GatchaLife Monorepo (Django 5.2, Vue 3.5).
- **Native Bridge:** Android Native project is missing and must be initialized (Capacitor wrapper).
- **Data Architecture:** Hard Schema Reset. Create fresh `Mana` system, discarding legacy stats.
- **Widget Sync:** High-Latency Polling (15m) using Android `WorkManager`.
- **Asset Delivery:** Contextual Pre-Caching. Equip action triggers download of all 5 mood variants.
- **API Strategy:** Strict `openapi-typescript-codegen` usage for frontend types.
- **Visual Direction:** "The Glass Menagerie" (Modern/Premium). Glassmorphism and soft gradients.
- **Lore Voice:** System messages and notifications should use character-specific voice/lore where possible.

### FR Coverage Map

FR1: Epic 1 - Mood Decay logic
FR2: Epic 1 - Companion State tiers
FR3: Epic 1 - Sleep State logic
FR4: Epic 4 - Shadow State enforcement
FR5: Epic 4 - Haunting Debuff penalty
FR6: Epic 1 - TickTick ingestion (n8n)
FR7: Epic 1 - XP/Coin reward math
FR8: Epic 1 - Mood healing from tasks
FR9: Epic 3 - Coin balance view
FR10: Epic 3 - Card Pack purchase
FR11: Epic 3 - Rest Potion purchase
FR12: Epic 3 - Rest Potion consumption
FR13: Epic 4 - Character Resurrection
FR14: Epic 4 - Character Exorcism
FR15: Epic 3 - Roster view
FR16: Epic 1 - Equip Active Companion
FR17: Epic 1 - Equipped character decay/XP
FR18: Epic 1 - Unequipped character stasis
FR19: Epic 3 - Visual Shadow/Locked indicators
FR20: Epic 2 - Widget Image display
FR21: Epic 2 - Widget Priority Task display
FR22: Epic 2 - Widget polling service
FR24: Epic 5 - AI Prompt input
FR25: Epic 5 - AI Image generation
FR26: Epic 5 - Save/Mint character

## Epic List

### Epic 1: Foundation & "The Living Companion" (Core Loop)
Users can see their companion's state and experience the "Caretaker Loop" through task-based healing and time-based decay.
**FRs covered:** FR1, FR2, FR3, FR6, FR7, FR8, FR16, FR17, FR18.

### Epic 2: The "Wingman" Widget (Native Bridge)
Users can monitor their companion and see their top task directly on their Android home screen without opening the app.
**FRs covered:** FR20, FR21, FR22.

### Epic 3: Roster & Discovery (The Acquisition Layer)
Users can acquire new character templates through multiple channels (**Gatcha Cards** or **The Forge**) and view their entire collection in a unified inventory.
**FRs covered:** FR9, FR10, FR15, FR19.

### Epic 4: Consequences & Redemption (The Shadow State)
Users experience the weight of neglect through "The Haunting" (global debuff) and can redeem or delete "Dead" companions.
**FRs covered:** FR4, FR5, FR13, FR14.

### Epic 5: The Character Forge (Standalone Creation)
Users can **independently** design and "Mint" unique characters using AI prompting, adding them directly to their collection alongside Gatcha-sourced cards.
**FRs covered:** FR24, FR25, FR26.

---

## Epic 1: Foundation & "The Living Companion" (Core Loop)

Users can see their companion's state and experience the "Caretaker Loop" through task-based healing and time-based decay.

### Story 1.1: Project Initialization & Mana Schema

As a **Developer**,
I want to **establish the new `CompanionState` model and clean the database**,
So that **the implementation of the new Caretaker Loop has a clean, conflict-free foundation.**

**Acceptance Criteria:**

**Given** a Django backend with legacy happiness/energy fields
**When** I run the "Hard Schema Reset" migration
**Then** the legacy fields are removed and a new `CompanionState` model is created.
**And** `CompanionState` includes a `ForeignKey` to the existing `Character` model (allowing users to "Activate" any character as their companion).
**And** `CompanionState` includes a `mana` field (0-100), `xp`, `level`, and `is_equipped` flags.
**And** the `openapi.json` is updated to reflect these schema changes.

### Story 1.2: The Pulse (Mood Decay Ticker)

As a **System**,
I want to **decay the active companion's Mana periodically using Celery Beat**,
So that **the user feels the weight of time and neglect.**

**Acceptance Criteria:**

**Given** an active companion with Mana > 0
**When** the Celery Beat ticker completes its interval (e.g., every hour)
**Then** the companion's Mana decreases by a configurable decay rate.
**And** the companion's state (Extremely Happy -> Dead) is recalculated based on the new Mana value.
**And** no decay occurs if the companion is unequipped or is in a "Sleep State."

### Story 1.3: Inflow (TickTick Webhook Integration)

As a **Developer**,
I want to **expose a robust webhook endpoint for TickTick/n8n signals**,
So that **external productivity events can influence the game state.**

**Acceptance Criteria:**

**Given** an incoming POST request from n8n with a TickTick task payload
**When** the endpoint is hit with valid authentication
**Then** the system logs the event and maps it to the correct internal user based on the payload.
**And** the system rejects invalid or malformed payloads with a 400 error.

### Story 1.4: The Healing Loop (Rewards & Mana Recovery)

As a **User**,
I want **my companion to heal and earn coins when I complete tasks**,
So that **my productivity is rewarded with positive emotional feedback.**

**Acceptance Criteria:**

**Given** a validated TickTick task completion signal
**When** the "Healing Logic" processes the task difficulty tags
**Then** the active companion's Mana is increased by the corresponding healing amount.
**And** Coins and XP are calculated and added to the user/companion totals.
**And** the "Last Interaction" timestamp is updated to reset the decay timer.

### Story 1.5: Character Registry (Equip & Stasis Logic)

As a **User**,
I want to **select which companion is active and keep others safe**,
So that **I can manage my roster without worrying about inactive companions dying.**

**Acceptance Criteria:**

**Given** multiple companions in the user's roster
**When** I "Equip" a specific companion
**Then** all other companions are set to `is_equipped = false`.
**And** only the companion with `is_equipped = true` is subject to decay ticks.
**And** the frontend UI reflects the current active companion as the "Primary" focus.

### Story 1.6: Night Cycle (Sleep State Logic)

As a **User**,
I want **my companion to sleep during my configured resting hours**,
So that **I don't lose progress while I am also offline/asleep.**

**Acceptance Criteria:**

**Given** a user-configured sleep window (e.g., 23:00 to 07:00)
**When** the current system time falls within this window
**Then** the companion's state is set to "Sleeping."
**And** all Mana decay ticks are skipped for that companion until the window ends.
**And** user interactions like "Petting" are visually disabled or show a "Sleeping" notification.

---

## Epic 2: The "Wingman" Widget (Native Bridge)

Users can monitor their companion and see their top task directly on their Android home screen without opening the app.

### Story 2.1: Native Wrapper & Capacitor Bridge

As a **Developer**,
I want to **initialize the Android native project and Capacitor bridge**,
So that **I can build native widgets that interact with the web backend.**

**Acceptance Criteria:**

**Given** an existing Vue 3 PWA
**When** I add the Capacitor Android platform and run `npx cap open android`
**Then** a valid `android/` directory is created with basic app scaffolding.
**And** a custom bridge interface (or standard HTTP client) is configured to allow native Kotlin code to call the Django API.

### Story 2.2: Widget Provider Foundation

As a **User**,
I want to **add a GatchaLife widget to my home screen**,
So that **I can see my companion even when the app is closed.**

**Acceptance Criteria:**

**Given** a native Android project
**When** I implement the `AppWidgetProvider` and `RemoteViews`
**Then** the GatchaLife widget appears in the Android widget picker.
**And** placing the widget displays a placeholder companion image and the app logo.

### Story 2.3: WorkManager Polling Service

As a **System**,
I want to **periodically poll the Django API from the Android background**,
So that **the widget data stays fresh without draining the battery.**

**Acceptance Criteria:**

**Given** a configured `WorkManager` job
**When** the periodic interval (15-30m) triggers
**Then** the native code makes an authenticated GET request to the GatchaLife `CompanionState` endpoint.
**And** the response (Mana, State, Task Name) is stored in the widget's local cache.

### Story 2.4: Dynamic Widget UI (Mood & Task)

As a **User**,
I want **the widget to show my companion's current mood and my next task**,
So that **I know exactly how my friend is doing and what I need to do next.**

**Acceptance Criteria:**

**Given** fresh data in the widget's local cache
**When** the widget UI is updated
**Then** the companion's image reflects their current mood (Happy, Pouting, etc.).
**And** the name of the highest priority pending task is clearly legible.
**And** the UI degrades gracefully (showing "Offline" or "Syncing") if the network fails.

### Story 2.5: Deep Linking (Quick Action)

As a **User**,
I want to **tap the widget to open the app directly to my companion**,
So that **I can take quick care actions without navigating menus.**

**Acceptance Criteria:**

**Given** a GatchaLife widget on the home screen
**When** I tap the companion image or task name
**Then** the Android system launches the GatchaLife app via a deep link.
**And** the app opens directly to the Sanctuary view or Task Completion view.

---

## Epic 3: Roster & Discovery (The Acquisition Layer)

Users can acquire new character templates through multiple channels (**Gatcha Cards** or **The Forge**) and view their entire collection in a unified inventory.

### Story 3.1: The Roster View (Unified Collection)

As a **User**,
I want to **browse my entire collection of characters from all sources**,
So that **I can admire my unique forged characters alongside my gatcha cards.**

**Acceptance Criteria:**

**Given** a user with characters from both Forge and Gatcha pulls
**When** I navigate to the "Roster" view
**Then** the UI displays a unified grid of character cards following the "Glass Menagerie" aesthetic.
**And** each card indicates the source (e.g., "Forged" or "Epic Card") and link status to an active `CompanionState`.
**And** clicking a character opens a detail view showing their specific stats (if active) or a prompt to "Equip/Activate".

### Story 3.2: Card Pull & Character Discovery

As a **User**,
I want to **pull cards from Gatcha packs using my Coins**,
So that **I can unlock rare character templates.**

**Acceptance Criteria:**

**Given** a user with enough Coins
**When** I trigger a "Summon" action in the Gatcha view
**Then** the system deducts the Coin cost and selects a character from the pool based on rarity weights.
**And** a new entry is added to the user's `Character` collection (or `CharacterVariant` if a skin).
**And** a cinematic reveal animation plays before showing the results.

### Story 3.3: Companion Activation (Instance Initialization)

As a **User**,
I want to **equip a character I just discovered for the first time**,
So that **I can start building their levels and Mana.**

**Acceptance Criteria:**

**Given** a character template that has never been equipped
**When** I select "Equip" in the Roster
**Then** the system creates a new `CompanionState` instance linked to that character.
**And** the instance starts with Neutral Mana (50%) and Level 1 (0 XP).
**And** the character becomes the "Active Companion" subject to decay and rewards.

### Story 3.4: The Coin Shop (Consumables)

As a **User**,
I want to **spend my extra Coins on meaningful utility items**,
So that **I can strategically manage my companion's health.**

**Acceptance Criteria:**

**Given** a user in the "Shop" view
**When** I purchase a "Rest Potion"
**Then** my Coin balance decreases and the item is added to my inventory.
**And** the shop UI reflects the transaction with clear success/error toasts.

### Story 3.5: Consumption & Effect (Rest Potion)

As a **User**,
I want to **use a Rest Potion on my companion**,
So that **I can pause their decay for a few hours while I'm away.**

**Acceptance Criteria:**

**Given** an active companion and a Rest Potion in inventory
**When** I "Consume" the potion from the Sanctuary view
**Then** the companion's decay is paused for exactly 8 hours.
**And** the UI shows a "Resting" buff indicator with a countdown timer.
**And** the potion is removed from the user's inventory.

---

## Epic 4: Consequences & Redemption (The Shadow State)

Users experience the weight of neglect through "The Haunting" (global debuff) and can redeem or delete "Dead" companions.

### Story 4.1: The Shutdown (Shadow State Transition)

As a **System**,
I want to **lock a companion when their Mana hits 0**,
So that **neglect has a clear, non-negotiable consequence.**

**Acceptance Criteria:**

**Given** an active companion whose Mana reaches 0 during a decay tick
**When** the calculation completes
**Then** the companion enters the "Shadow State" (is_dead = true).
**And** the companion is automatically unequipped and cannot be re-equipped until revived.
**And** a "Critical State" notification is triggered for the user.

### Story 4.2: The Haunting (Economic Debuff)

As a **User**,
I want **"Dead" companions to actively hinder my progress**,
So that **I have a strong incentive to revive them immediately.**

**Acceptance Criteria:**

**Given** one or more companions in the roster in "Shadow State"
**When** I complete a task and earn Coins
**Then** the system applies a global -50% multiplier to the Coin reward (`base_reward / 2`).
**And** the UI clearly displays a "Haunting Active" debuff icon during reward reveals.

### Story 4.3: The Revival Ritual (Redemption)

As a **User**,
I want to **pay a price to bring my companion back to life**,
So that **I can resume my bond and clear my economic debuffs.**

**Acceptance Criteria:**

**Given** a companion in Shadow State and sufficient Coins
**When** I select "Revive" in the Roster/Detail view
**Then** the system deducts a high Coin fee (e.g., 5,000 Coins).
**And** the companion instance is restored to Neutral Mana and the `Shadow State` is cleared.
**And** the "Haunting" debuff is recalculated (removed if no other dead companions remain).

### Story 4.4: The Exorcism (Deletion)

As a **User**,
I want to **permanently delete a dead character if I can't afford to revive them**,
So that **I can clear the debuff, even at the cost of my asset.**

**Acceptance Criteria:**

**Given** a companion in Shadow State
**When** I select "Exorcise" and confirm the permanent loss warning
**Then** the companion instance and its parent character template are permanently deleted from the database.
**And** the "Haunting" debuff is cleared.
**And** a "Memory Stone" (static image link) is generated for the user's history log.

---

## Epic 5: The Character Forge (Standalone Creation)

Users can **independently** design and "Mint" unique characters using AI prompting, adding them directly to their collection alongside Gatcha-sourced cards.

### Story 5.1: The Forge UI (Prompt Engineering)

As a **Creator**,
I want **a dedicated space to design my next companion**,
So that **I can express my creativity through text and visual previews.**

**Acceptance Criteria:**

**Given** the user has navigated to the "Forge" view
**When** I enter a text prompt and click "Enter"
**Then** the UI validates the prompt for length and basic safety.
**And** the UI displays an "Opening Synthesis" animation while the request is being prepared.

### Story 5.2: AI Synthesis (n8n & Image Generation)

As a **Creator**,
I want **the system to generate a unique high-quality image from my text prompt**,
So that **I can feel true ownership of a 1-of-1 companion.**

**Acceptance Criteria:**

**Given** a valid text prompt from the user
**When** I click "Synthesize"
**Then** the backend makes a synchronous call to the n8n image generation webhook.
**And** the system waits for the AI response (handling timeouts gracefully).
**And** the generated Image URL is returned and displayed as a large, high-fidelity preview in the "Glass" card.

### Story 5.3: Mood Extraction (Multimodal Synthesis)

As a **System**,
I want **to automatically generate the 5 mood-specific variants for the forged character**,
So that **the new character is fully compatible with the Widget and Sanctuary views.**

**Acceptance Criteria:**

**Given** a successfully generated "Base" image
**When** the user proceeds to "Accept" the character
**Then** the system sends the base prompt back to the AI with specific "Mood Modifiers" (e.g., "Pouting", "Crying", "Angry").
**And** five distinct images are generated and linked to the new character's identity.

### Story 5.4: Character "Minting" (Persistence)

As a **Creator**,
I want to **save my masterpiece to my permanent collection**,
So that **I can equip them and start our journey together.**

**Acceptance Criteria:**

**Given** a complete set of generated images (Base + Moods)
**When** I click "Mint Character"
**Then** the system creates a new `Character` record in the database with the generated images and user-provided Name.
**And** the character appears immediately in the "Roster" view with a "FORGED" badge.

### Story 5.5: Forge Balancing (Generation Costs)

As a **User**,
I want **forging a character to be a significant, high-value investment**,
So that **unlocking gatcha cards still feels exciting and meaningful.**

**Acceptance Criteria:**

**Given** a user attempting to use the Forge
**When** the "Synthesize" action is triggered
**Then** the system deducts a significant Coin cost (e.g., 10,000 Coins) or checks a "Forge Token" balance.
**And** the user is prevented from forging if they lack sufficient resources.
