# 🎮 GatchaLife - Functional Documentation

## 🌟 Overview
GatchaLife is a gamification platform designed to turn your daily life management into an engaging Gacha game. By completing tasks in your real life (integrated with TickTick), you earn XP and Coins to summon unique, AI-generated collectible cards.

## 🕹️ Core Features

### 1. 🏠 Dashboard
The central hub of your GatchaLife experience.
- **Player Stats**: View your current Level, XP progress, and Coin balance.
- **XP Bar**: Visual progress bar showing how close you are to the next level.
- **Daily Tasks**: Sync with your TickTick account to claim rewards for completed tasks.
  - *Current Reward Rate*: 10 XP and 5 Coins per task.
- **Summoning**: Access the Gacha system to spend your hard-earned coins.

### 2. ✨ Gacha System (Summoning)
The heart of the game. Spend coins to collect unique cards.
- **Cost**: 100 Coins per summon.
- **Mechanics**:
  - **Rarity Roll**: The system first determines the rarity of your drop (Common, Rare, Legendary).
  - **Combination**: It then randomly selects a **Character Variant**, a **Style**, and a **Theme**.
  - **AI Generation**: If this specific combination has never been seen before, an AI (via n8n) generates a unique illustration for it on the fly.
- **Duplicates**: If you roll a card you already own, your collection count for that card increases.

### 3. 🃏 Collection
Your personal gallery of unlocked treasures.
- **Grid View**: See all your cards at a glance.
- **Filtering**: Filter your collection by Rarity (Common, Rare, Legendary) to find your best pulls.
- **Visuals**: Cards have distinct borders and glow effects corresponding to their rarity.
  - ⚪ **Common**: Grey/Silver
  - 🔵 **Rare**: Blue
  - 🟡 **Legendary**: Gold

### 4. 🔍 Card Details
Click on any card in your collection to view it in full glory.
- **Full-Bleed Art**: View the high-quality AI-generated artwork without obstructions.
- **Metadata**: See the Character Name, Variant Name, Style, and Theme used to generate the card.
- **Stats**: View when you obtained the card and how many copies you own.

## 🔄 The Game Loop
1. **Do Tasks**: Complete tasks in your real life (TickTick).
2. **Sync**: Click "Sync TickTick" on the Dashboard to get XP and Coins.
3. **Level Up**: Gain enough XP to increase your Player Level (unlocking potential future bonuses).
4. **Summon**: Use Coins to roll for new cards.
5. **Collect**: Build your collection and hunt for Legendary cards!
