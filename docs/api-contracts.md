# API Contracts - GatchaLife

The GatchaLife backend provides a RESTful API using Django REST Framework. The frontend uses an auto-generated client from the backend's OpenAPI schema.

## Endpoints Summary

### Character Management
- `GET /api/series/`: List all character series.
- `GET /api/characters/`: List all characters.
- `POST /api/characters/`: Create a new character (triggers N8N/AI profiling).
- `GET /api/variants/`: List character variants.

### Gamification & Player
- `GET /api/players/me/`: Get current player stats and state.
- `GET /api/active-tamagotchis/`: Get current active tamagotchi companion.
- `POST /api/gatcha/summon/`: Perform a summon (Gatcha roll).
- `GET /api/collection/`: Get player's card collection.
- `GET /api/quests/`: List available and active quests.

### Asset Management
- `GET /api/generated-images/`: List available AI-generated images.
- `POST /api/companion-images/`: Manage and set companion visual states.

### Task Integration
- `GET /api/ticktick/sync/`: Manually trigger a sync with TickTick.
- `GET /api/ticktick/projects/`: List synced TickTick projects.

## Authentication
Uses Session authentication by default, with CSRF protection. In development, Basic auth is also supported.
- `authentication.py`: Contains custom `CsrfExemptSessionAuthentication`.

## API Documentation
The backend provides interactive documentation at:
- Swagger: `/apidocs/`
- Redoc: `/redoc/`
