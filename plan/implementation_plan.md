# Implementation Plan - Phase 1 Initialization

## Goal
Initialize the project repository and set up the core infrastructure for the Sworm System (Phase 1 MVP).

## Proposed Changes

### 1. Folder Structure
Create a standard monorepo-style structure:
```
/backend
    /app
        /core       # Engine, Ticks, EventBus
        /models     # Nation, State, Agents
        /api        # Routes, WebSockets
    main.py
    requirements.txt
/frontend
    /src
        /components
        /simulation # Canvas/PixiJS logic
    package.json
/ml             # Placeholder for later phases
/database       # Placeholder for SQL schema
```

### 2. Backend Initialization (Python/FastAPI)
-   **File:** `backend/requirements.txt`
    -   Dependencies: `fastapi`, `uvicorn`, `pydantic`, `sqlalchemy` (async), `websockets`.
-   **File:** `backend/app/main.py`
    -   Basic FastAPI app with CORS and a Hello World endpoint.
-   **File:** `backend/app/core/engine.py`
    -   Skeleton `SimulationEngine` class.

### 3. Frontend Initialization (React/Vite)
-   **Command:** `npm create vite@latest frontend -- --template react-ts`
-   **Dependencies:** `pixi.js` (or `@pixi/react`), `axios`, `socket.io-client`, `tailwindcss`.
-   **File:** `frontend/src/App.tsx`
    -   Basic layout shell.

## Verification Plan

### Automated Tests
-   **Backend:** Run `pytest` (once added) or simply run the server `uvicorn app.main:app --reload` and check `http://localhost:8000/docs`.
-   **Frontend:** Run `npm run dev` and check `http://localhost:5173`.

### Manual Verification
1.  Start Backend.
2.  Start Frontend.
3.  Verify they can communicate (e.g., fetch a simple JSON object from backend).
