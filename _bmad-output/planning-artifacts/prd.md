---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
inputDocuments:
  - "docs/index.md"
  - "docs/project-overview.md"
  - "docs/architecture.md"
  - "docs/data-models.md"
  - "docs/api-contracts.md"
  - "docs/source-tree-analysis.md"
  - "docs/development-guide.md"
documentCounts:
  briefs: 0
  research: 0
  brainstorming: 0
  projectDocs: 7
workflowType: 'prd'
lastStep: 11
---

# Product Requirements Document - GatchaLife

**Author:** Tlafay
**Date:** 2026-01-10T15:59:41+01:00

## Executive Summary

**GatchaLife** is evolving from a card-collection productivity game into a **"Living Companion" ecosystem**. The core vision shifts focus to a high-stakes **Tamagotchi system** where the companion's state is directly tied to the user's real-world productivity.

Unlike standard gamification which relies on "points," GatchaLife leverages **Loss Aversion** and the **IKEA Effect**: protecting a unique, invested creation is a more powerful motivator than earning new rewards. To reinforce this loop, the system will expand beyond the browser into **Native Apps (Mobile/Desktop)** to ensure the companion is "always visible" via widgets ("Wingman Widgets") that not only display mood but actively serve the next productivity task to remove friction.

### What Makes This Special

**"The Externalized Conscience"**
GatchaLife isn't just a pet simulator; it's a visual mirror of your personal integrity. By stripping away abstract point systems and replacing them with a living entity that thrives only when you keep your promises, the system creates a powerful **"Alignment Loop."**

- **Identity Projection:** The detailed customization allows users to project their ideal self into the companion. Its health becomes a proxy for their own disciplined state.
- **Conscience Anchor:** The native widget serves as a constant, non-judgmental anchor to your intentions, reducing the cognitive load of "remembering to be good."
- **Dynamic Adaptation:** The system learns the user's rhythm to set fair "Floors" for survival (preventing burnout) while reserving "Bonus Tiers" for growth (preventing laziness).
- **Wingman Widget:** Transforms notifications from nagging to helping by offering the next immediate step to "save" the companion.
- **Investment Preservation:** The deep customization of the AI-generated characters ensures users fight to maintain their progress ("I built this, I won't let it fail").

## Project Classification

**Technical Type:** Hybrid Ecosystem (Centralized Django API + Native/Web Clients)
**Domain:** Gamified Productivity
**Complexity:** High (Cross-platform sync, adaptive algorithms, hardware/IoT roadmap)
**Project Context:** Brownfield - pivoting core mechanics and expanding platform reach of existing system.

## Success Criteria

### User Success
- **Cognitive Offloading:** Users rely on the "Wingman Widget" to decide their next task rather than browsing their todo list.
- **Emotional Alignment:** Users express a desire to "protect" their companion's state, indicating successful detailed customization and investment.
- **Habit Formation:** Users engage with the app/widget > 5 times daily in short bursts (< 10s), shifting from "session-based" usage to "lifestyle" usage.

### Business Success
- **Retention:** Achieve > 40% Day-30 Retention (significantly higher than standard productivity apps).
- **Expansion:** Successfully deploy compliant native wrappers to Android and Desktop environments.

### Technical Success
- **Synchronization:** State changes (e.g., task completion on desktop) reflect on mobile widget within < 5 seconds.
- **Battery Impact:** Native background services (mood decay polling) consume < 2% daily battery life.

## Product Scope

### MVP - Minimum Viable Product
- **Core Loop:** Mood Decay + Productivity Replenishment logic.
- **Platform:** Web PWA + Android Wrapper (Capacitor) with Basic Widget.
- **Notifications:** Integration with Firebase (FCM) for "Critical State" alerts.
- **Assets:** Static AI images with basic CSS animations (breathing, shaking).

### Growth Features (Post-MVP)
- **Dynamic Difficulty:** "Floors & Bonus Tiers" algorithm to adapt to user velocity.
- **Desktop Native:** Electron/Tauri build with "Always-on" desktop widget.
- **Advanced Visuals:** Sprite-sheet based animations.

### Vision (Future)
- **Physical Companion:** IoT hardware integration.
- **Social Ecosystem:** Shared quests and companion visits.

## User Journeys

### Journey 1: The "Wingman" Intervention (Primary User - Mobile)
**Persona:** Alex, a productivity-focused user who often gets overwhelmed by long todo lists.
**Opening Scene:** Ideally Alex should be working, but he's doom-scrolling on his phone. He glances at his home screen and sees the GatchaLife widget.
**Rising Action:** The widget shows "Kai" (his companion) looking exhausted, with a speech bubble: *"I'm fading... just one 'Quick Task' to save me?"* It displays the easiest task from his TickTick list: "Water the plants."
**Climax:** The friction barrier is broken. It's just one small task. Alex puts the phone down, waters the plants, and taps the widget completion button.
**Resolution:** Kai instantly transforms to a "Relieved/Happy" state with a small confetti animation on the widget. Alex feels a micro-dopamine hit—not from "points," but from *saving* his friend. He decides to do "just one more."

### Journey 2: The "Deep Work" Sync (Primary User - Desktop)
**Persona:** Sarah, a user who works on her laptop all day.
**Opening Scene:** Sarah finishes a massive coding sprint. She checks off 4 tasks in her TickTick desktop app.
**Rising Action:** She doesn't open GatchaLife immediately. She grabs a coffee. When she returns, she glances at her secondary monitor where the GatchaLife Desktop Widget lives.
**Climax:** The widget has already synced (via the backend). Her companion, "Luna," is now glowing with a "Supercharged" aura. The widget displays: *"4 Tasks Crushed! Bonus Tier Active: 2x XP for next hour!"*
**Resolution:** Sarah feels recognized. The passive synchronization validated her work without her needing to manually log it. She feels "seen" by her digital companion.

### Journey 3: The "IKEA Effect" Creation (Primary User - Creator)
**Persona:** Leo, who loves customizing and "owning" his tools.
**Opening Scene:** Leo unlocks a "Rare Evolution Crystal" after a 7-day streak. He enters the "Evolution Forge" (Web App).
**Rising Action:** He doesn't just click "Upgrade." He parses a prompt description for his companion's new form: *"Cyberpunk Samurai with a neon katana."* He waits for the AI generation.
**Climax:** The result is unique—a 1-of-1 image that no other user has. He names it "Ronin."
**Resolution:** "Ronin" is now his widget. The investment of creation makes him fiercely protective. He sets a "Vacation Mode" (freezing decay) before his weekend trip because he genuinely cares about not letting "Ronin" die.

### Journey Requirements Summary
- **Mobile Widget:** Must support interactive buttons (Complete Task) and dynamic image updates.
- **Backend Sync:** Must ingest TickTick webhooks/polling and push state to all clients in near real-time.
- **AI Generation:** The "Forge" needs an interface for prompting and selecting/saving generated images.
- **State Logic:** "Bonus Tiers" and "Streak" logic must be calculated server-side to prevent cheating and ensure cross-platform consistency.

## Domain-Specific Requirements

### Gamified Productivity & Psychological Safety

**The "Healthy Habit" Constraint**
Unlike standard games, GatchaLife consumption is tied to real-world energy. User burnout prevention creates retention.

- **Dynamic Baselines:** Productivity targets must adapt to user rhythm (rolling 7-day average).
- **"Rest Potion" Mechanic:** A consumable item (bought with Coins) that pauses mood decay for a set duration. Gamifies "rest" as a earned strategic resource.
- **No-Shame "Stasis":** Inactive (unequipped) characters are frozen in time. They do not decay, allowing users to maintain a roster without "Tamagotchi Fatigue."

### "Cute Death" & Financial Consequence Loop

**Death Mechanic (Shadow State):**
If a companion is neglected to 0 mood:
- They assume a "Shadow Form" (visual lockout).
- **The Haunting:** A dead companion applies a global **-50% Coin Multiplier Debuff** on all tasks until resolved. This creates immediate urgency.
- **The Ultimatum:** The user has [X] days to resolve the haunting by either:
    1.  **Paying the Price:** A massive Coin fee to revive them (forcing a "Savings Account" strategy).
    2.  **Exorcism:** Permanently deleting the character (and their unique AI art) to remove the debuff.

### Native Platform Compliance

- **Widget Efficiency:** Android Widgets must use `WorkManager` for background updates to respect battery standards (<2% daily usage).
- **Notification Channels:** Separation of "Critical Health" (bypass DND) and "Fluff" (silent) notifications.

## Innovation & Novel Patterns

### Detected Innovation Areas

**1. The "Cute Death" Reincarnation Loop**
Most gamification apps either have no death (Habitica reserves death for party raids) or permanent deletion (Tamagotchi). GatchaLife introduces a middle ground: **Asset Permadeath with Stat Persistence.**
-   **Innovation:** Destroying the *aesthetic* investment (the specific AI-generated face/name) while preserving the *functional* investment (levels/stats). This balances "Loss Aversion" (avoiding pain) with "Retention" (not quitting in rage).

**2. The "Haunting" Economic Debuff**
Instead of simple point deduction, GatchaLife introduces a **Viral Debuff Mechanics**. A neglected character doesn't just "die quietly"; they become a liability that actively taxes the user's future productivity (-50% Coin Generation).
-   **Innovation:** This turns a passive failure state into an active "Emergency" that cannot be ignored, forcing engagement to "clean up the mess."

**3. The "Wingman" Widget Intervention**
Moving beyond passive displays (showing a sad face), the widget actively proposes specific, low-friction tasks ("Water Plants") to break procrastination loops.
-   **Innovation:** Transformation from a "Nagging" system (telling you what you didn't do) to a "Helping" system (handing you the easiest win).

### Market Context & Competitive Landscape
-   **Habitica:** Focuses on RPG parties and pixel art. Death is a stat reset. GatchaLife diverges by focusing on *Individual* emotional bonds and high-fidelity AI assets.
-   **Forest:** Focuses on "locking" the phone. GatchaLife focuses on *integration* with the phone (Widgets).
-   **Tamagotchi:** Focuses on arbitrary needs (poop/food). GatchaLife ties needs strictly to *real-world productivity*.

### Validation Approach
-   **A/B Test - The Haunting:** Measure user recovery rates with "Shadow State" (Lockout only) vs. "Haunting" (Lockout + 50% Tax). Hypothesis: The Tax will drive 2x higher revival rates.
-   **Retention Metric:** Monitor "Day 7 Survival Rate" of the first companion. High death rate early on suggests the difficulty floor is too high.

### Risk Mitigation
-   **Risk:** "Rage Quit" upon Reincarnation.
-   **Mitigation:** The "Memory Stone" graveyard. Allowing users to keep a static image of their lost friend softens the blow, turning it into a nostalgic collectible rather than a total loss.

## Mobile/Native Specific Requirements

### Project-Type Overview
GatchaLife will utilize **Capacitor** to wrap the existing Vue 3 PWA into native Android/iOS bundles. The primary goal is **"Home Screen Presence"** via Widgets, not just a native app icon.

### Technical Architecture Considerations

**1. Widget Architecture (Hybrid)**
-   **Core:** Android `AppWidgetProvider` (Kotlin/Java) for the native widget shell.
-   **Data Sync:** A background `WorkManager` job will poll the GatchaLife API (Django) every 15-30 minutes to fetch:
    -   Current Companion Image URL (Mood-based).
    -   Next Priority Task Name/ID.
-   **Interaction Layer:**
    -   **MVP:** Clicking the widget deep-links into the specific PWA page (e.g., ticking the task opens the `TaskCompletion` view).
    -   **Growth:** Implement `PendingIntent` to trigger API calls directly from the widget (Background Completion).

**2. Offline Capabilities**
-   **State Caching:** The native wrapper must cache the last known "Companion State" and "Task List" locally.
-   **Degraded Mode:** If offline, the widget displays the cached state with a subtle "Offline" indicator (e.g., greyed out aura) rather than an error spinner, preserving aesthetics.

**3. Push Notification Bridge**
-   **Infrastructure:** Firebase Cloud Messaging (FCM).
-   **Strategy:** "Critical Alerts" (Death/Decay warnings) utilize high-priority channels to bypass aggressive battery optimization.

**4. Platform Compliance (Self-Use)**
-   **Monetization:** None. Coins are purely a gameplay loop outcome.
-   **Permissions:** `POST_NOTIFICATIONS` is the only mandatory runtime permission. `FOREGROUND_SERVICE` may be required for the Widget Sync depending on Android version.

### Implementation Considerations
-   **Asset Handling:** AI-Generated images (Companion Faces) should be cached (`Glide`/`Coil` on Android side) to prevent bandwidth drain on the widget's frequent updates.
-   **Deep Linking:** Configure `Intent Filters` in `AndroidManifest.xml` to handle `gatchalife://task/{id}` URLs.

## Project Scoping & Phased Development

### MVP Strategy & Philosophy
**MVP Approach:** **Experience MVP**
For a personal motivation tool, "Delight" is a functional requirement. The MVP must establish the emotional bond immediately via high-quality visuals (AI Images) and frictionless access (Widgets).

**Resource Requirements:** Single Developer + AI Agent capability for asset generation.

### MVP Feature Set (Phase 1)
**Core User Journeys Supported:**
-   Journey 1: The "Wingman" Intervention (Mobile Widget).
-   Journey 3: The "IKEA Effect" Creation (Character Forge).

**Must-Have Capabilities:**
-   **Unified Economy:** Coins used for both Gatcha and Upkeep.
-   **Death Loop v1:** Character Locking (Shadow State) + Haunting Debuff.
-   **Mobile Widget (Passive):** Displays current mood image and top task.
-   **TickTick Integration via n8n:** n8n workflows manage task synchronization and AI logic, ensuring GatchaLife DB reflects real-time task status.

### Post-MVP Features

**Phase 2 (Growth - "Strategy Layer"):**
-   **Roster Handling:** Stasis logic, specific Character Bonuses (e.g., +10% XP for specific tags).
-   **Consumables:** "Rest Potions" and "Revival Rituals."
-   **Interactive Widgets:** Complete tasks directly from home screen (Android PendingIntent).

**Phase 3 (Vision):**
-   **Desktop Native:** Electron build.
-   **IoT:** Dedicated hardware companion.

### Risk Mitigation Strategy
-   **Technical Risk:** **Widget Sync Battery Drain.**
    -   *Mitigation:* Strict 15-min polling limits via `WorkManager`.
-   **Motivation Risk:** **"Death Spiral" (Too hard to revive).**
    -   *Mitigation:* "Bailout" mechanic where the first revival is free/cheap to teach the lesson without crushing the user.

## Functional Requirements

### Core Companion Engine
- FR1: System must calculate "Mood Decay" based on time elapsed since last productive action.
- FR2: System must determine "Companion State" strictly using these tiers:
    - **Extremely Happy (80-100%)**
    - **Happy (60-80%)**
    - **Neutral (40-60%)**
    - **Pouting (20-40%)**
    - **Very Distressed (1-20%)**
    - **Dead (0%)**
    - **Sleeping** (Time-based override)
- FR3: System must apply "Sleep State" logic during user-configured hours, freezing decay but preventing interaction.
- FR4: System must enforce "Shadow State" (Lockout) when Mood reaches 0 (Dead), preventing equipping or use of the character.
- FR5: System must apply a "Haunting Debuff" (50% Coin reduction) if any character in the roster is in Shadow State.

### Productivity Integration
- FR6: System must ingest Task Completion events from TickTick Webhooks (via n8n).
- FR7: System must calculate XP and Coin rewards based on **Task Difficulty** (tagged in TickTick) and current multipliers (Companion Mood, Haunting Debuff, Streak).
- FR8: System must update the Active Companion's Mood upon task completion (Healing), with healing amount scaled by Task Difficulty.

### Economy & Shop
- FR9: User can view current Coin balance (Unified Currency).
- FR10: User can spend Coins to Purchase "Card Packs" (Gatcha) to acquire new characters.
- FR11: User can spend Coins to Purchase "Rest Potions" (Consumables).
- FR12: User can consume a "Rest Potion" to pause Mood Decay for [X] hours.
- FR13: User can spend Coins to "Resurrect" a character in Shadow State, restoring them to Neutral Mood.
- FR14: User can "Exorcise" (Delete) a character in Shadow State to remove the Haunting Debuff permanently.

### Roster Management
- FR15: User can view all owned characters in a "Roster" view.
- FR16: User can "Equip" one character as the Active Companion.
- FR17: Equipped character is the only one subject to Mood Decay and receiving XP.
- FR18: Unequipped characters must remain in "Stasis" (Mood frozen).
- FR19: Roster view must clearly indicate "Shadow/Locked" characters.

### Widget & Mobile Presence
- FR20: Mobile Widget must display the Active Companion's current Image (based on State).
- FR21: Mobile Widget must display the Name of the highest priority pending Task from TickTick.
- FR22: Mobile Widget must periodically poll (every 15-30m) or receive push updates for State changes.
- FR23: (Removed) Offline Mode Requirements (User is expected to be Online).

### Character Forge (Creation)
- FR24: User can input a text prompt to generate a new Character appearance (via AI).
- FR25: System must generate a unique image based on the prompt.
- FR26: User can "Save/Mint" the generated character into their collection.

## Non-Functional Requirements

### Usability & Aesthetics (Critical)
- **NFR1 - Friction:** Mobile Widget "Task View" must load and become interactive within <2 seconds.
- **NFR2 - Aesthetics:** AI-generated visuals must maintain a consistent style (Anime/Gatcha) via fixed negative prompt engineering to prevent jarring visual quality shifts.
- **NFR3 - Battery Impact:** Background sync services (Widget polling) must consume < 2% of daily battery life on Android devices.

### Reliability & Data Integrity
- **NFR4 - State Consistency:** Task completion on one device (e.g., Desktop TickTick) must reflect on the Mobile Widget within 15 minutes (polling interval) or immediately via Push (if fully implemented).
- **NFR5 - Haunting Logic:** The "Haunting Debuff" calculation must be atomic; race conditions between task completion and mood decay updates must default to the *user's benefit* (e.g., counting the task before the decay tick).

### Performance
- **NFR6 - Asset Loading:** Companion images (often large AI files) must be cached locally on mobile devices. Subsequent loads of the same mood/state must be instant (<100ms).
- **NFR7 - Generation Speed:** Character creation (Forge) should complete within < 30 seconds to maintain the "impulse" excitement.
