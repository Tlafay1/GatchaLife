stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
workflowType: 'architecture'
lastStep: 8
status: 'complete'
completedAt: '2026-01-11'
inputDocuments:
  - "_bmad-output/planning-artifacts/prd.md"
  - "_bmad-output/planning-artifacts/ux-design-specification.md"
workflowType: 'architecture'
project_name: 'GatchaLife'
user_name: 'Tlafay'
date: '2026-01-11'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**
*   **Core Logic:** System logic is driven by "Mood Decay" (time-based state change) and "Haunting" (state-based penalty) state machines.
*   **Ingestion:** "Work" signals are ingested asynchronously from **TickTick via n8n** webhooks.
*   **Native Bridge:** Android Widget requires a specific data sync layer effectively bridging the web-based game state to the native home screen.

**Scale & Complexity:**
*   **Primary Technical Domain:** Hybrid (Django/Celery Backend + Vue/Capacitor Frontend).
*   **Complexity Level:** Medium-High. The complexity lies not in the data volume but in the **Asynchronous State Interactions** (Time vs User Action vs External Webhook).
*   **Estimated Components:** ~10 (Backend API, Celery Worker, n8n Workflow, Frontend PWA, Capacitor Bridge, Widget Service, etc.)

### Technical Constraints & Dependencies

*   **Task Queue:** **Celery** is mandated as the backbone for calculation (Mood Decay) and ingestion (Webhooks).
*   **Sync Latency:** The system accepts a **30s-60s delay** between real-world action (checking a task) and Game State update. Real-time sockets are not required; "Eventual Consistency" is acceptable.
*   **Widget Limitations:** Android background execution limits necessitate a **High-Latency Polling (15m)** + **Manual Refresh** strategy. Instant push updates to widgets are deprioritized.

### Cross-Cutting Concerns Identified

*   **Asset Management:** Dynamic AI images must be cached effectively on the client to prevent bandwidth drain/pop-in.
*   **Resilience:** Handling n8n webhook failures via Celery retries is critical to prevent "Lost Work" frustration.
## Starter Template Evaluation

### Primary Technology Domain

**Hybrid Web/Mobile Application** (Brownfield Refactor)

### Starter Options Considered

Since this is an existing project, the "Starter" is the current codebase. We evaluated the current stack against the project requirements.

### Selected Foundation: Existing GatchaLife Monorepo

**Rationale for Selection:**
We are extending an existing, functional application. Rewriting from scratch would waste valuable domain logic (Mood Decay models, TickTick integration concepts). The current stack (Django + Vue) is robust and well-suited for the "Hybrid" requirements.

**Architectural Decisions Ratified:**

**Language & Runtime:**
*   **Backend:** Python 3.12+ (Django 5.2)
*   **Frontend:** TypeScript 5.9 (Vue 3.5)

**Styling Solution:**
*   **Tailwind CSS v4** + **Shadcn-Vue (Reka UI)**.
*   This aligns perfectly with the "Glass Menagerie" design direction, allowing for rapid custom utility creation (`bg-glass`, `text-glow`).

**Build Tooling:**
*   **Vite 7** for lightning-fast frontend HMR.
*   **Poetry** / `pip` for Backend dependency management.

**Testing Framework:**
*   **Frontend:** Vitest + Vue Test Utils.
*   **Backend:** `pytest` (Standard Django practice).

**Code Organization:**
*   **Monorepo:** `GatchaLife-frontend` and `GatchaLife-backend` co-located.
*   **API Pattern:** REST (Django Rest Framework) + Client SDK generation (`openapi-typescript-codegen`).

**Development Experience:**
*   **Hot Reload:** Vite provides instant feedback for UI changes.
*   **Type Safety:** Strict TypeScript configuration in frontend ensures robust client code.

**Note:** The primary architectural addition will be the **Android Widget Native Bridge**, which is currently missing from the foundation.

## Core Architectural Decisions

### Data Architecture
*   **Strategy:** **Hard Schema Reset** (Greenfield subset)
*   **Decision:** We will **drop** the legacy `Happiness`/`Energy` fields and create a fresh `Mana` system.
*   **Data Policy:** Legacy Tamagotchi stats will be discarded. User/Auth data preserved.
*   **Rationale:** "Destroy all legacy data." This simplifies the backend significantly (no complex migration scripts) and allows us to build the "Mood Decay" logic cleanly from scratch without fighting legacy constraints.

### Widget State Sync
*   **Strategy:** **High-Latency Polling (Pull-Only)**
*   **Interval:** 15 Minutes (Android WorkManager minimum).
*   **Rationale:** User accepted trade-off of "30-60s Latency" for "Implementation Simplicity" and Battery life. Real-time push is deprioritized for MVP.

### Asset Delivery
*   **Strategy:** **Contextual Pre-Caching**
*   **Implementation:** "Equip" action triggers a background download of **all 5 mood variants** for the active companion to local storage.
*   **Rationale:** Mitigates the "White Box" risk on the Widget if the user is offline when mood changes.

### Decision Priority Analysis

**Critical Decisions (Block Implementation):**
1.  **Schema Definition:** Must define the new `CompanionState` model before any backend work.
2.  **Worker Setup:** Must configure Celery Beat for the "Mood Decay" ticker.
3.  **Bridge Design:** Must define the Capacitor Plugin interface for the Widget.

**Deferred Decisions (Post-MVP):**
*   **FCM Push:** Real-time updates via Firebase deferred until polling proves insufficient.

## Implementation Patterns & Consistency Rules

### Critical Pattern: The "Codegen" Contract
To maintain velocity in a single-developer "Hobby" project, we avoid writing manual API clients.
*   **Source of Truth:** Django `drf-yasg` / `drf-spectacular` generates `openapi.json`.
*   **Client Generation:** `npm run api:sync` (using `openapi-typescript-codegen`) generates strict TypeScript interfaces and services.
*   **Rule:** Frontend never manually types API responses. Examples: `models.CompanionState`.

### Naming Conventions (Pragmatic Bridge)
*   **Backend (Python):** `snake_case` everywhere.
*   **Frontend (TS):** `camelCase` for variables/functions.
*   **The Interface Gap:** Frontend will **accept** `snake_case` properties from API objects (e.g., `companion.mood_level`) to avoid the complexity/overhead of a runtime casing middleware. "Don't overdo it."

### API Response Format
*   **Standard DRF:** We stick to standard Django Rest Framework responses.
    *   List: `{ count: 10, next: ..., results: [...] }`
    *   Detail: `{ id: 1, ... }`
*   **No Custom Envelopes:** Unless metadata is strictly required, avoiding custom definitions allows the Codegen to work out-of-the-box without custom parsers.

### Error Handling Pattern
*   **"The Polite Fail":** UI components wrap data fetching in `try/catch`.
*   **User Feedback:** On error, show a generic "Toast" (e.g., "Connection weak...") and allow retry. do not expose 500 tracebacks to the UI.

### Widget <-> App Code Sharing
### Widget <-> App Code Sharing
*   **Shared Types:** The Native Widget (if writing Java/Kotlin) cannot import TS types. We will treat the Widget as a **separate client** that manually implements the minimal data fetch logic, keeping implementation simple. Use the API Docs as the reference.

## Project Structure & Boundaries

### Complete Project Directory Structure

```
GatchaLife/
├── GatchaLife-frontend/         # Vue 3 + Vite Monorepo
│   ├── src/
│   │   ├── api/                 # [GENERATED] TypeScript API Client (Do Not Edit)
│   │   ├── components/
│   │   │   ├── ui/              # [NEW] Shadcn/Tailwind "Glass" Components
│   │   │   └── widgets/         # [NEW] Widget Preview Components
│   │   ├── stores/              # Pinia State Stores (Auth, Companion, UI)
│   │   ├── views/               # Page Views (Sanctuary, Gatcha, Forge)
│   │   └── App.vue              # Main App Shell
│   └── package.json
│
├── GatchaLife-backend/          # Django 5 + Celery
│   ├── gatchalife/              # Core App Bundle
│   │   ├── character/           # Companion Models (Legacy + New State)
│   │   ├── gamification/        # Economy & Stat Logic
│   │   ├── ticktick/            # External Task Ingestion (n8n Webhooks)
│   │   └── generated_image/     # AI Asset Management
│   ├── celerybeat-schedule      # Periodic Task Schedule
│   └── manage.py
│
└── android/                     # [MISSING] Native Android Studio Project
    └── app/src/main/java/.../widget/  # Kotlin Widget Provider Code
```

### Architectural Boundaries

**API Boundaries:**
*   **Frontend <-> Backend:** Strict HTTP/JSON via `src/api` client. No ad-hoc `fetch` calls.
*   **Widget <-> Backend:** `WorkManager` polling via `Retrofit` (Kotlin) fetching standard JSON endpoints.
*   **TickTick <-> Backend:** One-way Webhooks via `ticktick.views.WebhookView`.

**Component Boundaries:**
*   **UI Components:** purely presentational. They take props and emit events. They DO NOT touch the API directly.
*   **Views/Pages:** Connected components. They fetch data via `stores` and pass it down to UI components.
*   **Stores:** The only layer that talks to `src/api`.

### Requirements to Structure Mapping

**Feature Mapping:**
*   **"Mana" System:** `GatchaLife-backend/gatchalife/character/models.py` (New `CompanionState` model).
*   **"Glass Menagerie" UI:** `GatchaLife-frontend/src/components/ui/*.vue` (Tailwind overrides).
*   **Widget Sync:** `android/.../WidgetWorker.kt` (New Kotlin file).

**Cross-Cutting Concerns:**
*   **Assets:** `GatchaLife-backend/gatchalife/generated_image/` (manages S3/Local file paths).

## Architecture Validation Results

### Coherence Validation ✅
*   **Decision Compatibility:** Technology stack (Django/Vue) and patterns (Codegen) are internally consistent and well-suited for a single-developer hobby project.
*   **Pattern Consistency:** Implementation patterns (Pragmatic casing, Standard DRF responses) support rapid implementation without over-engineering.
*   **Structure Alignment:** The proposed directory structure explicitly handles both existing layers and the upcoming Native/Widget additions.

### Requirements Coverage Validation ✅
*   **Epic/Feature Coverage:**
    *   **Mana System:** Architected via `CompanionState` model and Hard Schema Reset.
    *   **Widget Sync:** Architected via `WorkManager` (Kotlin) polling the Django API.
    *   **TickTick Integration:** Robustly handled via n8n webhooks and asynchronous Celery tasks.
*   **Non-Functional Requirements:**
    *   **Performance:** Pre-caching strategy for AI assets ensures snappy UI/Widget updates.
    *   **Battery:** Polling (15m) strategy prioritizes device longevity over instant push.

### Implementation Readiness Validation ✅
*   **Overall Status:** READY FOR IMPLEMENTATION
*   **Confidence Level:** High
*   **First Implementation Priority:** Initialize the Android Native project structure in the `android/` directory.

### Architecture Completeness Checklist
- [x] Project context and technical constraints identified
- [x] Critical decisions (Data, Sync, Assets) documented
- [x] Implementation patterns and consistency rules established
- [x] Complete directory structure mapped
- [x] All PRD/UX requirements architecturally supported

## Architecture Completion Summary

### Workflow Completion
**Architecture Decision Workflow:** COMPLETED ✅
**Total Steps Completed:** 8
**Date Completed:** 2026-01-11
**Document Location:** `_bmad-output/planning-artifacts/architecture.md`

### Final Architecture Deliverables
*   **📋 Complete Architecture Document:** All decisions (Data, Sync, Assets) documented with verified versions.
*   **🏗️ Implementation Ready Foundation:** Django 5 + Vue 3 + Celery 5.3 verified as the project core.
*   **📚 AI Agent Implementation Guide:** Specific patterns established for Codegen and Casing to prevent conflict.

### Implementation Handoff
**For AI Agents:** This architecture document is your complete guide for implementing GatchaLife. Follow all decisions, patterns, and structures exactly as documented.

**First Implementation Priority:** 
Initialize the **Android Native Project** (Capacitor) to create the bridge for the Widget implementation.

**Development Sequence:**
1.  Initialize Android Native wrapper.
2.  Implement the `CompanionState` schema and Mana decay logic in the backend.
3.  Implement the Shadcn-Vue "Glass" component system in the frontend.
4.  Develop the Android Widget provider fetching from the unified API.

---
**Architecture Status:** READY FOR IMPLEMENTATION ✅






