# Sworm System - Phase 1 MVP Walkthrough

## Status
-   **Backend:** Initialized (FastAPI), Models Created, Simulation Engine Running.
-   **Frontend:** Initialized (React/Vite), Dependencies Installed.
-   **Infrastructure:** Directory structure set up.

## How to Run

### 1. Start Backend
Open a terminal in `backend/` and run:
```bash
python -m uvicorn app.main:app --reload --port 8000
```
*   API Docs: `http://localhost:8000/docs`
*   Current State: `http://localhost:8000/api/simulation/state`

### 2. Start Frontend
Open a terminal in `frontend/` and run:
```bash
npm run dev
```
*   App: `http://localhost:5173`

## Current Capabilities
-   **Simulation:** Generates a random world with 1 Nation, 3 States, and citizen/leader agents.
-   **API:** Can retrieve the full world state via JSON.
-   **Engine:** Ticks are manual (via `/api/simulation/tick` or internal scheduler).

## Next Steps
-   Connect Frontend to Backend via API/WebSockets.
-   Render the "Nation Map" using PixiJS.
-   Implement Budget/Election mechanics.
