# Backend Unit Test Suite

I have implemented a comprehensive unit test suite for the backend, focusing on the critical gamification logic triggered by Zapier webhooks.

## Test Coverage

### 1. Zapier Webhook (`ZapierWebhookTests`)
This suite tests the core game loop logic:
- **Validation**: Ensures requests with missing IDs are rejected (400 Bad Request).
- **Idempotency**: Verifies that duplicate task IDs are handled gracefully (200 OK) without double-rewarding the player.
- **Reward Calculation**:
  - **Basic Task**: Verifies base reward calculation for a standard task.
  - **Difficulty Multipliers**: Tests that `medium` (1.5x), `hard` (2.0x), and `extreme` (3.0x) tags correctly multiply the reward.
  - **Critical Success**: Mocks the random number generator to force a critical hit and verifies the 2x multiplier.
  - **Streak Logic**: Simulates tasks completed on consecutive days vs. gaps to ensure streaks increment and reset correctly.
  - **Level Up**: Simulates a massive XP gain to verify level-up logic and bonus coin awards.

### 2. Stats & History (`TickTickStatsTests`)
This suite tests the data visualization endpoints:
- **Stats Endpoint**: Verifies total counts and recent activity structure.
- **History Endpoint**: Verifies pagination and data field correctness.
- **Progression Endpoint**: Verifies daily aggregation of XP and Coins.

## How to Run Tests

You can run the full suite using Docker:

```bash
docker-compose exec backend python manage.py test gatchalife.ticktick
```

## Implementation Details
- **Mocking**: Used `unittest.mock.patch` to control `random.randint`, `random.random`, and `django.utils.timezone.now` for deterministic testing of probability and time-based logic.
- **Timezones**: Handled timezone-aware datetimes correctly to ensure tests pass in any environment.
