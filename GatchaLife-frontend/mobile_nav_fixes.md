# Mobile Navigation Fixes

I have fixed the mobile navigation issues and added the missing routes.

## Changes

1.  **Created `SummonBanner.vue`**:
    *   Extracted the summoning logic and UI from `PlayerDashboard.vue` into a reusable component.
    *   This component handles the roll logic, animation, and display of the banner.

2.  **Created `GatchaView.vue`**:
    *   Created a dedicated page for summoning (`/gatcha`).
    *   This page uses the `SummonBanner` component.
    *   Includes a mobile-friendly header.

3.  **Updated `PlayerDashboard.vue`**:
    *   Replaced the inline summoning code with the `<SummonBanner />` component.
    *   Cleaned up unused imports and variables.

4.  **Updated Router**:
    *   Added the `/gatcha` route pointing to `GatchaView.vue`.

5.  **Updated `MobileNav.vue`**:
    *   Changed the "Creator" link from `/creator` (which was broken) to `/studio` (the correct route for Creator Studio).

## Verification
- **Build**: Passed.
- **Navigation**:
    - Clicking "Summon" on mobile now goes to `/gatcha` (working page).
    - Clicking "Creator" on mobile now goes to `/studio` (working page).
