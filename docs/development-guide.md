# Development Guide - GatchaLife

This guide covers the necessary steps to set up and develop the GatchaLife project.

## Quick Start (Docker)

The easiest way to get started is using Docker Compose.

```bash
docker-compose up --build
```

- **Frontend:** http://localhost:5173
- **Backend:** http://localhost:8000
- **Admin:** http://localhost:8000/admin

## Manual Setup (Local)

### Backend (Python/Django)
1.  **Navigate to backend directory:**
    ```bash
    cd GatchaLife-backend
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run migrations:**
    ```bash
    python manage.py migrate
    ```
5.  **Start the server:**
    ```bash
    python manage.py runserver
    ```

### Frontend (Vue/Vite)
1.  **Navigate to frontend directory:**
    ```bash
    cd GatchaLife-frontend
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Start the development server:**
    ```bash
    npm run dev
    ```

## Common Commands

### Frontend Scripts
- `npm run dev`: Start dev server.
- `npm run build`: Build for production.
- `npm run lint`: Run ESLint.
- `npm run format`: Format code with Prettier.
- `npm run api:sync`: Sync the API client with the backend (requires backend running).

### Backend Management
- `python manage.py makemigrations`: Create new migrations based on model changes.
- `python manage.py migrate`: Apply database changes.
- `python manage.py createsuperuser`: Create an admin account.
- `celery -A gatchalife worker -B`: Run Celery worker and beat (scheduled tasks).

## API Client Synchronization
The frontend uses `openapi-typescript-codegen` to generate its API client. If you change the backend models or views, you should regenerate the client:
1.  Ensure the backend is running at `http://localhost:8000`.
2.  Run `npm run api:sync` in the `GatchaLife-frontend` directory.
