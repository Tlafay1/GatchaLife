# 🛠️ GatchaLife - Technical Documentation

## 🏗️ Architecture
The project is built as a modern web application using a decoupled architecture, containerized with Docker.

- **Frontend**: Vue.js 3 (Vite)
- **Backend**: Django REST Framework (Python)
- **Database**: PostgreSQL
- **AI Service**: External n8n webhook integration

## 🐳 Infrastructure
The application runs via `docker-compose`.
- **`db`**: PostgreSQL 15 container.
- **`backend`**: Python 3.11 container running Django development server (Gunicorn/Uvicorn in prod).
- **`frontend`**: Node.js container running Vite development server.

## 🔙 Backend (`GatchaLife-backend`)
Built with Django 4.2 and Django REST Framework.

### Key Apps
1. **`gamification`**:
   - Core logic for Players, Quests, and the Gacha system.
   - **Models**: `Player`, `Card`, `UserCard`, `Quest`.
   - **Views**: `GatchaViewSet` handles the rolling logic and triggers image generation.
2. **`character`**:
   - Manages base character data.
   - **Models**: `Series`, `Character`, `CharacterVariant`.
3. **`style`**:
   - Manages aesthetic parameters for generation.
   - **Models**: `Rarity`, `Style`, `Theme`.
4. **`generated_image`**:
   - Handles the interface with the AI generation service.
   - **Service**: `generate_image()` sends a payload to n8n and saves the returned binary.

### 🤖 AI Integration (n8n)
The backend triggers image generation via a POST request to an n8n webhook.
- **Payload**: Includes Character details, Style keywords, Theme description, and Rarity.
- **Format**: Enforces `portrait, vertical aspect ratio 2:3` and `full bleed` via injected prompt keywords.
- **Storage**: Generated images are saved locally in `media/generated_images/` and served via Django.

## 🖥️ Frontend (`GatchaLife-frontend`)
Built with Vue 3, TypeScript, and Tailwind CSS.

### Key Technologies
- **Build Tool**: Vite
- **State/Data Fetching**: TanStack Query (Vue Query)
- **Styling**: Tailwind CSS with a custom dark/premium theme.
- **Routing**: Vue Router
- **API Client**: Generated via `openapi-typescript-codegen`.

### Project Structure
- `src/gamification/`: Core game components (`Dashboard`, `Collection`, `GatchaAnimation`).
- `src/lib/api-client.ts`: Custom hooks wrapping the generated API client.
- `src/style.css`: Global styles and Tailwind configuration.

## 💾 Database Schema
Key relationships:
- `Player` 1:1 `User`
- `Card` is unique by (`CharacterVariant`, `Style`, `Theme`, `Rarity`).
- `UserCard` links `Player` to `Card` with a `count` field.
- `GeneratedImage` stores the actual image file, linked to the same 4 parameters as a Card.

## 🚀 Running the Project
```bash
# Start all services
docker-compose up --build

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser (optional)
docker-compose exec backend python manage.py createsuperuser
```
