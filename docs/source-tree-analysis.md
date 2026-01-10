# Source Tree Analysis - GatchaLife

This document provides an annotated overview of the project's directory structure.

## Root Directory
```text
.
├── GatchaLife-backend/     # Django Backend Application
├── GatchaLife-frontend/    # Vue.js Frontend Application
├── nginx/                  # Nginx configuration for reverse proxy
├── docs/                   # Project documentation (BMM Project Knowledge)
├── _bmad/                  # BMad Method configuration and workflows
├── _bmad-output/           # BMad Method generated artifacts
├── docker-compose.yml      # Development environment configuration
└── docker-compose.prod.yml # Production environment configuration
```

## Backend Structure (`GatchaLife-backend/`)
```text
GatchaLife-backend/
├── gatchalife/             # Main Django Project Directory
│   ├── settings.py         # Application settings
│   ├── urls.py             # Main routing
│   ├── celery.py           # Celery task configuration
│   ├── character/          # Character & Series management
│   ├── gamification/       # Game loop (Tamagotchi, Card System)
│   ├── generated_image/    # Asset management for AI images
│   ├── style/              # Rarities, Styles, and Themes
│   ├── ticktick/           # Reward system & TickTick integration
│   └── workflow_engine/    # Async job management
├── static/                 # Static assets (including media)
├── requirements.txt        # Python dependencies
└── manage.py               # Django management script
```

## Frontend Structure (`GatchaLife-frontend/`)
```text
GatchaLife-frontend/
├── src/
│   ├── api/                # Auto-generated API client from OpenAPI
│   ├── components/         # Reusable Vue components
│   │   └── ui/             # Design system (Shadcn-like)
│   ├── gamification/       # Game mechanics (Dashboard, Collection, Gatcha)
│   ├── character/          # Character management views
│   ├── series/             # Series-related views
│   ├── style/              # Theme and Style views
│   ├── stores/             # Pinia state stores
│   ├── lib/                # Shared utilities and API client init
│   ├── router/             # Vue Router configuration
│   ├── types/              # TypeScript type definitions
│   ├── App.vue             # Root component
│   └── main.ts             # Application entry point
├── public/                 # Static assets (favicons, PWA icons)
├── package.json            # Node.js dependencies and scripts
└── vite.config.ts          # Vite build configuration
```
