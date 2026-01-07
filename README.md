# Sworm System: Multi-Agent Socio-Political Simulation

[![CI/CD Pipeline](https://github.com/Ganesh01110/socio-political-multiagent-swarm/actions/workflows/main.yml/badge.svg)](https://github.com/Ganesh01110/socio-political-multiagent-swarm/actions/workflows/main.yml)

## 🌟 Vision
The **Sworm System** is a sophisticated multi-agent simulation designed to explore the emergent dynamics of hierarchical social structures. It models the flow of power, resources, and influence from individual citizens up to a Supreme Lead, mediated by media institutions and external global events. 

By combining **Hierarchical Strategy Patterns (DQN, ANN, Rule-Based)** for agents with **Economic Feedback Loops (Inflation/Unemployment)** and **Fuzzy Logic Morality**, the system creates a living laboratory for political economy and social engineering.

---

## 🏗️ Architecture (Agent Hierarchy)

| Level | Agent | Visualization | Responsibility |
| :--- | :--- | :--- | :--- |
| **L4** | **External Factors** | ⚫ Grey | Global events (Pandemics, Booms, Disasters) |
| **L3** | **Media / Institutions** | 🟣 Purple | Influence public perception and trust scores |
| **L2** | **Supreme Leader** | 🟡 Yellow | Resource allocation and national policy |
| **L1** | **State Leaders** | 🟢 Green | Local management and re-election focused RL |
| **L0** | **Citizens** | 🔵 Blue | Wealth generation, voting, and ideology spread |

---

## 🚀 Tech Stack

- **Backend:** FastAPI (Python), SQLAlchemy, Pydantic
- **AI/ML:** PyTorch (DQN), Scikit-Learn (Random Forest, Tree, kNN), Scikit-Fuzzy (Morality FIS)
- **State Logic:** Unified ANN Intelligence (16-node MLP) for Citizens & Leaders, DQN for Supreme Leader
- **Database:** MariaDB (XAMPP compatible) / SQLite with per-state history tracking
- **Frontend:** React, TypeScript, PixiJS (High-performance Swarm Rendering)
- **Dynamics:** 
  - Social Circle Graphing with Threshold Influence (Tipping Points)
  - Political Coup Mechanics & Cronyism in Elections
  - Dynamic Media Ownership (Industrialist, Politician, Citizen, External)
  - Simulation Control Toggles (Hope, Trust Decay, Memory Loss, Ideology Shift)
- **DevOps:** Docker, Docker Compose, GitHub Actions (CI/CD)



---

## 🛠️ Getting Started

### Prerequisites
- Python 3.11+
- Node.js 20+
- (Optional) XAMPP MariaDB for persistent data

### Quick Start (Local)
1. **Clone the Repo:**
   ```bash
   git clone https://github.com/Ganesh01110/socio-political-multiagent-swarm.git
   cd socio-political-multiagent-swarm
   ```
2. **Backend Setup:**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # Or .venv\Scripts\activate
   pip install -r requirements.txt
   python -m uvicorn app.main:app --reload
   ```
3. **Frontend Setup:**
   ```bash
   cd frontend
   npm ci
   npm run dev
   ```

### Running Tests
```bash
cd backend
pytest -v
```


### Quick Start (Docker)
```bash
docker-compose up --build
```

---

## 📖 Documentation
Detailed guides are available in the `docs/` folder:
- [Advanced Agent Brains & Economic Loops](./docs/advanced_agent_brains.md) (Why? What? How?)
- [Installation & Requirements](./docs/installation_requirements.md)
- [Project Brainstorming](./brainstorming.md)

---

## 🤝 Roadmap & Milestones
- [x] **Phase 1-5:** Core mechanics, Elections, and Economy.
- [x] **Phase 7-8:** AI Upgrades (DQN) and Social Complexity (Factions/Generations).
- [x] **Phase 9-11:** Hierarchy Expansion (Media/External) and DevOps.
- [x] **Phase 12:** Advanced Agent Brains with Hybrid Strategies, Fuzzy Logic, and Social Graphing.
- [x] **Phase 13:** Simulation Control Toggles & Dynamic Media Ownership (Complete).
  - Unified ANN intelligence for realistic human-level equality
  - Citizen mechanics toggles (Hope, Trust Decay, Memory Loss, Ideology Shift)
  - Media ownership based on social connections with dynamic bias
  - Cronyism in elections and policy-aware leader rewards
- [ ] **Phase 14:** Geo-Political Expansion and International Trade (Planned).



---

**Developed by [Ganesh Sahu](mailto:ganeshsahu0108@gmail.com)**
