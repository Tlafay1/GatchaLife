# Project Overview - GatchaLife

GatchaLife is a web-based gatcha game and companion system that integrates with external task management tools (like TickTick) to gamify productivity.

## Project Metadata
- **Project Name:** GatchaLife
- **Type:** Multi-part (Web Frontend + REST Backend)
- **Primary Language:** TypeScript (Frontend), Python (Backend)
- **Architecture Pattern:** Component-based Frontend, Service-oriented REST Backend
- **Repository Structure:** Monorepo-style structure with `/GatchaLife-frontend` and `/GatchaLife-backend`.

## Technology Stack

### Frontend
- **Framework:** Vue 3.5 (Composition API)
- **Build Tool:** Vite 7.1
- **Language:** TypeScript
- **Styling:** Tailwind CSS 4.1, Shadcn UI (Vue ports)
- **State Management:** Pinia, TanStack Vue Query
- **Routing:** Vue Router
- **Animations:** VueUse Motion, Animate.css
- **PWA:** Vite PWA Plugin

### Backend
- **Framework:** Django 5.2.8
- **API:** Django REST Framework
- **Task Queue:** Celery with Redis
- **Database:** PostgreSQL
- **Logging:** StructLog
- **Documentation:** DRF-Yasg (Swagger/OpenAPI)
- **Deployment:** Docker, Gunicorn, WhiteNoise

## Core Components
- **Gamification:** Card system, summoning (gathca), player progression, and companion (tamagotchi) mechanics.
- **Task Integration:** Synchronization with TickTick for rewarding task completion.
- **Creation Tools:** Character forge and variant generator with N8N/AI integration.
- **Workflow Engine:** Internal system for handling asynchronous jobs and AI workflows.
