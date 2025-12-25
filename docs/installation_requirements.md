# Project Installation & Requirements Guide

This document provides a comprehensive list of requirements and step-by-step instructions to set up and run the Sworm System project locally.

## 1. Prerequisites

Before starting, ensure you have the following installed on your system:

- **Python 3.10 or higher**: [Download Python](https://www.python.org/downloads/)
- **Node.js 18 or higher**: [Download Node.js](https://nodejs.org/)
- **pip** (Python package manager, usually bundled with Python)
- **npm** (Node package manager, usually bundled with Node.js)

---

## 2. Backend Setup (FastAPI)

The backend handles the simulation logic, AI (DQN) training, and database persistence.

### Requirements
The following Python packages are required (defined in `backend/requirements.txt`):
- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `pydantic`: Data validation
- `sqlalchemy`: Database ORM
- `aiosqlite`: Asynchronous SQLite support
- `websockets`: Real-time communication (optional next steps)
- `torch`: Deep Learning framework for DQNAgents
- `numpy`: Numerical processing

### Installation Steps
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment (highly recommended):
   ```bash
   python -m venv .venv
   ```
3. Activate the virtual environment:
   - **Windows**: `.venv\Scripts\activate`
   - **macOS/Linux**: `source .venv/bin/activate`
4. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Backend
```bash
python -m uvicorn app.main:app --reload --port 8000
```
The API will be available at `http://localhost:8000`.

---

## 3. Frontend Setup (React + Vite)

The frontend provides the visualization of the simulation using PixiJS and Recharts.

### Requirements
The following Node packages are required:
- `react`, `react-dom`: Core UI framework
- `pixi.js`, `@pixi/react`: High-performance WebGL rendering for agents
- `axios`: API communication
- `recharts`: Historical data visualization
- `vite`: Fast build tool/dev server

### Installation Steps
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```

### Running the Frontend
```bash
npm run dev
```
The app will typically be available at `http://localhost:5173`.

---

## 4. Database Configuration
By default, the simulation uses **SQLite** (`sworm_history.db`). 

To use **MariaDB** or **PostgreSQL**, set the `DATABASE_URL` environment variable before running the server:

### Windows (PowerShell)
```powershell
$env:DATABASE_URL="mariadb+mariadbconnector://user:password@localhost:3306/koko"
python -m uvicorn app.main:app --reload
```

### Linux/Mac
```bash
export DATABASE_URL="mariadb+mariadbconnector://user:password@localhost:3306/koko"
python -m uvicorn app.main:app --reload
```
- **File Path**: The database file `sworm_history.db` will be automatically created in the `backend` folder when you first run the simulation.
- **Verification**: You can use tools like [DB Browser for SQLite](https://sqlitebrowser.org/) to inspect the historical metrics if needed.

---

## 5. Deployment Checklist (Verification)

To ensure the project is running correctly:
1. **Check Backend Healthy**: Visit `http://localhost:8000/api/simulation/state` - it should return a JSON object of the world.
2. **Check Frontend Loaded**: Open the frontend URL - you should see the "Sworm System" title.
3. **Check AI Integration**: Ensure `torch` is correctly installed by running `python -c "import torch; print(torch.__version__)"`.
4. **Manual Tick**: Click the "Manual Tick" button on the UI and check if the "Tick" count increments and dots move.
