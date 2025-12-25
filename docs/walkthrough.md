# Sworm System Simulation - Final Walkthrough

The simulation has evolved into a complex ecosystem with Reinforcement Learning leaders, social dynamics, top-down governance, and persistent analytics.

## Key Accomplishments

### 1. Core Simulation & Economics
- **Multi-Agent System:** Visualized using PixiJS, with Citizens (Blue), State Leaders (Green), and the Supreme Leader (Yellow).
- **Wealth Distribution:** Money flows from the Nation to States and then to Citizens.
- **Dynamic Voting:** Citizens vote every 50 ticks based on their trust in the incumbent leader.

### 2. Reinforcement Learning Leaders
- Leaders learn to balance **Greed** vs **Survival** using a Q-Learning agent.
- Actions: Invest, Steal, Maintain, Propaganda.
- Rewards: Positive for re-election, negative for defeat.

### 3. Social Dynamics & Propaganda
- **Influence Propagation:** Citizens influence their neighbors' trust levels, causing social "proof" and clustering.
- **Propaganda:** Leaders can spend budget to artificially boost trust in their state, visualized with a golden ring.

### 4. Supreme Leader & Metrics
- **Top-Down Control:** The Supreme Leader reclaimed taxes and fired incompetent leaders (low trust).
- **Metrics Dashboard:** Real-time tracking of Global Happiness, Avg Trust, and Wealth.

### 5. Persistence & Analytics
- **Database:** All metrics are persisted to a SQLite database (`sworm_history.db`).
- **Trend Charts:** Integrated `recharts` to show historical trends of Happiness, Trust, and Wealth.

## How to Run & Verify

### Backend
1. `cd backend`
2. `pip install -r requirements.txt`
3. `python -m uvicorn app.main:app --reload --port 8000`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

### Verification Steps
1. Open the frontend (usually `http://localhost:5173`).
2. Click **Manual Tick** repeatedly.
3. Observe the **Golden Rings** (Propaganda) appearing around leaders.
4. Watch the **National Trends Chart** at the bottom to see how happiness and trust fluctuate over time.
5. Check the **News Feed** for election results and "Leader Executed" alerts.
