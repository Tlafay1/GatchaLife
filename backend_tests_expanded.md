# Backend Unit Test Suite Expansion

I have expanded the unit test suite to cover the entire backend, including Character management and the core Gamification logic (Gatcha System).

## New Test Coverage

### 1. Character App (`gatchalife.character.tests`)
- **Series**: Listing and filtering.
- **Characters**: Creation and filtering by series.
- **Variants**: Creation.
- **API Paths**: Verified correct URL routing for all resources.

### 2. Gamification App (`gatchalife.gamification.tests`)
- **Gatcha Roll Logic**:
  - **Success**: Verifies coin deduction, card creation, and response structure.
  - **Insufficient Funds**: Ensures 400 Bad Request when coins are low.
  - **Rarity Selection**: Mocks RNG to verify that high rolls correctly select higher rarities.
  - **Duplicate Stacking**: Verifies that rolling a duplicate card increments the `count` on the existing `UserCard` instead of creating a new one. (Patched `random.choice` to handle existing data migrations).
- **Collection**:
  - **Listing**: Verifies that the collection endpoint returns the correct card counts and details.

## Existing Coverage (TickTick)
- **Zapier Webhook**: Idempotency, Reward Calculation (Difficulty, Streak, Crit), Level Up.
- **Stats Endpoints**: History, Progression, Dashboard Stats.

## How to Run All Tests

```bash
docker-compose exec backend python manage.py test gatchalife.ticktick gatchalife.character gatchalife.gamification
```

All 19 tests are passing.
