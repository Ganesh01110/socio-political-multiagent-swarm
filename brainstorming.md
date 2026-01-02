# Sworm System - Brainstorming & Architecture

## 1. Concept Overview
"Sworm" is a socio-political simulation where agents (people) interact within a hierarchical structure (Nation -> State -> Individual). The simulation visualizes the emergence of leadership, corruption, and economic dynamics governed by AI-driven behaviors.

**Visual Hierarchy:**
-   **Nation:** The entire visible screen/viewport.
-   **State:** Specialized regions or partitions of the screen.
-   **Agents:**
    -   🔵 **General People:** The workforce.
    -   🟢 **Leaders:** Elected by general people per state.
    -   🟡 **Supreme Leader:** Elected by state leaders.

## 2. Simulation Dynamics
-   **Election Cycle:** Periodic voting based on "Opinion" or "Trust" scores.
-   **Economy:**
    -   **Supreme Leader** allocates the national budget to **Leaders** for specific tasks.
    -   **Leaders** distribute funds to **General People** to execute tasks.
    -   **Corruption:** At each step, an agent can choose to "siphon" funds (Corruption) or pass them down (Honesty).
    -   **Propaganda:** Leaders can spend funds to artificially boost their "Trust" score without honesty.
-   **Game Loop:** Setup -> Election -> Task Allocation -> Action/Corruption -> Outcome -> Feedback (Train AI).

## 3. AI & Logic Integration
We can integrate multiple paradigms to make the behaviors emergent and complex:

-   **Reinforcement Learning (RL):**
    -   Agents (Leaders/People) treat "Wealth" and "Re-election" as rewards.
    -   Actions: *Distribute Fund*, *Embezzle*, *Invest in Propaganda*.
    -   Agents learn policies: e.g., "If approval is low, reduce corruption to survive election" or "If approval is high, embezzle more".
-   **Supervised Learning:**
    -   Predict the probability of a Supreme Leader being overthrown based on current economic indicators (Inflation, Happiness).
-   **Unsupervised Learning (Clustering):**
    -   Group agents into "factions" or "parties" based on their voting patterns and honesty levels (e.g., The "Corrupt Elites" vs The "Honest Workers").
-   **Fuzzy Logic:**
    -   Rule-based decision making for simpler agents or initial bootstrapping.
    -   *Rules:* "If (Honesty is HIGH) and (Fund is LOW) then (Decreased Trust)".

## 4. Technical Architecture (SOLID & Agile)

### Frontend (The "Nation" View)
-   **Tech:** React (Vite) + Typescript.
-   **Visualization:** **PixiJS** or **React Three Fiber**. (Canvas is needed for performant rendering of many "swarming" agents).
-   **Communication:** WebSockets (Socket.io) for real-time state updates from the backend.

### Backend (The "Brain")
-   **Tech:** Python (FastAPI). Python is the natural choice for ML/AI integration.
-   **Structure:**
    -   `Engine`: Main loop handling time steps.
    -   `AgentManager`: Instantiates and tracks agents.
    -   `Brain`: Pluggable AI modules (RL Models, Neural Networks).
-   **Database:**
    -   **ORM:** SQLAlchemy (Async).
    -   **DB Support:** PostgreSQL (Production/Docker), MariaDB (User's Local).
        -   *Strategy:* Use abstract models and connection strings in `.env` to switch easily.
    -   **Migrations:** Alembic.

### Infrastructure
-   **Docker:** Containerize Backend (Python + Libraries) and Database. Frontend can run locally or in container.
-   **Compatibility:** Check OS/Hardware for ML acceleration (CUDA or CPU-based for lighter models).

## 5. Development Plan (Agile)
Break down into Sprints:
1.  **MVP Core:** Simple hierarchy, random movement, basic voting (random).
2.  **Econ & Logic:** Implement funds, task allocation, reliable database logging.
3.  **Basic Brain:** Introduce Fuzzy Logic or simple Heuristics for corruption.
4.  **AI Integration:** Replace Heuristics with RL agents (Q-Learning or PPO).
5.  **Visualization Polish:** Better assets, charts for "Honesty Index", etc.

## 6. Questions for Refinement
-   **Scale:** How many agents? (100? 1000? 10,000?). This defines if we use simple DOM nodes or WebGL.
-   **Persistence:** Do we need to replay history? (Database schema design implication).
-   **Interactivity:** Does the user interact (God mode) or just watch?
