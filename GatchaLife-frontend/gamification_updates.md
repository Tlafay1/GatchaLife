# Gamification Updates

## Features Implemented

### 1. Crit System
- **Backend**: Implemented a 10% chance for a "Critical Success" on task completion, which applies a **2x multiplier** to the total reward.
- **Frontend**: Added a "CRIT!" badge with a pulse animation in the Recent Activity feed and History view when a critical success occurs.

### 2. Difficulty-Based Rewards
- **Logic**: Rewards are now calculated based on task tags:
  - `difficulty/easy` (or no tag): **1x Multiplier**
  - `difficulty/medium`: **1.5x Multiplier**
  - `difficulty/hard`: **2x Multiplier**
  - `difficulty/extreme`: **3x Multiplier**
- **Implementation**: The backend parses tags from the Zapier payload and applies the appropriate multiplier before calculating the final reward.

### 3. Detailed Reward Visualization ("Why")
- **Data Storage**: The `ProcessedTask` model now stores a complete snapshot of the reward calculation:
  - Base Reward
  - Difficulty Multiplier
  - Streak Multiplier
  - Crit Multiplier
  - Daily Bonus
- **UI**:
  - **Dashboard**: Shows XP, Coins, and Difficulty badges in the Recent Activity feed.
  - **History Page**: Added a detailed tooltip on hover for each task, showing the exact formula used to calculate the total coins (e.g., "Base (20) x Difficulty (Hard 2.0) x Streak (1.1) = 44").

### 4. Progression Visualization
- **New Page**: Created `/history` (accessible via "View Full History" on the dashboard).
- **Chart**: Added a line chart showing XP and Coins earned daily over the last 30 days.
- **List**: A paginated list of all completed tasks with their reward details.

## Technical Changes
- **Database**: Updated `ProcessedTask` table to include new fields (`xp_gain`, `coin_gain`, `difficulty`, `is_crit`, etc.).
- **API**:
  - Updated `POST /ticktick/webhook` to handle tags and save detailed stats.
  - Updated `GET /ticktick/stats` to include recent activity details.
  - Added `GET /ticktick/history` for paginated task history.
  - Added `GET /ticktick/progression` for daily aggregated stats.
- **Frontend**:
  - Added `chart.js` and `vue-chartjs`.
  - Created `HistoryView.vue`.
  - Updated `PlayerDashboard.vue`.
  - Updated `api-client.ts`.

## Verification
- **Linting**: Passed.
- **Type Check**: Passed.
- **Build**: Passed.
