# Swarm Governance Simulation System – Low Level Design (LLD)

---

## 1. System Overview

The system is a **multi-agent, hierarchical swarm simulation** representing a nation with political, social, and economic dynamics. Agents operate in discrete time steps (ticks) and interact via elections, resource allocation, propaganda, and learning mechanisms. The system supports **visual simulation (frontend)** and **decision-making logic (backend + AI modules)**.

---

## 2. High-Level Component Breakdown

```
Frontend (UI / Visualization)
        ↓ WebSocket / REST
Backend API Layer
        ↓
Simulation Core Engine
        ↓
Agent System + AI Modules
        ↓
State Management & Persistence
```

---

## 3. Core Backend Modules

### 3.1 Simulation Engine

**Responsibility:**

* Drives the entire system using time-based ticks
* Coordinates updates across agents, elections, learning, and environment

**Key Classes:**

* `SimulationEngine`
* `TickScheduler`
* `EventBus`

**Methods:**

* `start()`
* `pause()`
* `advanceTick()`
* `emitEvent(eventType, payload)`

---

### 3.2 World Model

Represents the spatial and political structure.

**Entities:**

* `Nation`
* `State`
* `District` (optional)

**Nation**

```ts
id
name
states: State[]
metrics: NationalMetrics
supremeLeaderId
```

**State**

```ts
id
name
population
leaderId
economyIndex
trustIndex
```

---

## 4. Agent System

### 4.1 BaseAgent (Abstract)

```ts
id
type
honesty
greed
competence
trustScore
influenceRadius
memory: Event[]
```

**Common Methods:**

* `perceive(environmentState)`
* `decide()`
* `act()`
* `learn()`

---

### 4.2 CitizenAgent (Blue)

```ts
wealth
happiness
politicalAlignment
propagandaSusceptibility
stateId
```

**Responsibilities:**

* Vote in elections
* Spread opinions
* React to propaganda & economy

---

### 4.3 StateLeaderAgent (Green)

```ts
stateId
budgetAllocated
corruptionLevel
performanceScore
reElectionProbability
policyModel (RL Policy)
```

**Responsibilities:**

* Allocate funds within state
* Influence citizens
* Compete in elections

---

### 4.4 SupremeLeaderAgent (Yellow)

```ts
totalBudget
nationalPolicyModel
powerIndex
tenureRemaining
```

**Responsibilities:**

* Allocate budgets to states
* Shape national policies
* Control propaganda intensity

---

### 4.5 Media / Institution Agent (Purple)

```ts
bias
reach
credibility
```

**Responsibilities:**

* Propaganda diffusion
* Narrative shaping

---

## 5. Election System

### 5.1 ElectionService

**Methods:**

* `conductCitizenElection(stateId)`
* `conductLeaderElection()`

**Logic:**

* Probabilistic voting based on trust, economy, propaganda
* Delayed feedback effects

---

## 6. Economy & Resource Allocation

### 6.1 EconomyService

```ts
calculateGrowth(state)
distributeFunds(state, allocationMap)
```

Growth depends on:

* Budget usage
* Corruption leakage
* Leader competence

---

## 7. Corruption System

### 7.1 CorruptionModel

```ts
actualCorruption
perceivedCorruption
detectionProbability
```

* Hidden variable
* Detection is noisy & delayed

---

## 8. Propaganda & Influence System

### 8.1 InfluenceGraph

* Graph of agents
* Weighted edges represent influence strength

### 8.2 PropagandaService

```ts
spreadMessage(sourceAgent, message, budget)
```

Uses diffusion models (GNN-ready).

---

## 9. Learning Modules

### 9.1 Reinforcement Learning (Leaders)

**State:**

* Trust
* Economy
* Corruption

**Action:**

* Budget allocation vector

**Reward:**

```
reward = α*growth + β*trust - γ*corruption
```

---

### 9.2 Supervised Learning

Used for:

* Vote prediction
* Corruption risk estimation

---

### 9.3 Unsupervised Learning

Used for:

* Opinion clustering
* Ideology emergence

---

### 9.4 Fuzzy Logic Engine

```text
IF honesty is low AND propaganda is high
THEN public_trust decreases moderately
```

Used for:

* Trust dynamics
* Moral ambiguity

---

## 10. State Management & Storage

### 10.1 In-Memory State

* Current tick state
* Agent snapshots

### 10.2 Persistent Storage (PostgreSQL)

Tables:

* agents
* elections
* budgets
* metrics
* events

---

## 11. Backend API Layer

### REST Endpoints

```
GET /simulation/state
POST /simulation/start
POST /simulation/pause
GET /metrics
```

### WebSocket

* Real-time agent updates
* Tick-based diffs

---

## 12. Frontend LLD

### Components

* NationMap
* StateView
* AgentLayer (Canvas/WebGL)
* MetricsDashboard
* ControlPanel

### Features

* Color-coded agents
* Time speed control
* Policy sliders
* Election visualization

---

## 13. SOLID Compliance

* **S**: Agent behaviors separated from learning
* **O**: New agent types added without modifying core
* **L**: All agents extend BaseAgent
* **I**: Voting, Governing, Influencing interfaces
* **D**: Learning strategies injected

---

## 14. Agile Breakdown (Development-Ready)

### Sprint 1

* Core engine
* Agents
* Visualization

### Sprint 2

* Elections
* Economy

### Sprint 3

* RL leaders
* Metrics

### Sprint 4

* Propaganda
* Unsupervised dynamics

---

## 15. Extension Hooks

* External shocks (war, disaster)
* Multiple nations
* International diplomacy
* Human-in-the-loop control

---

## 16. Development Plans (plan.md Files)

Below are phase-wise `plan.md` documents intended to be used **directly by AI agents** for implementation.

---

# plan-phase-1.md – Core Simulation & Visualization (MVP)

## Goal

Build a **fully visible, deterministic simulation** without ML to validate system dynamics and UI.

## Scope

* Nation → State structure
* Citizen & Leader agents (rule-based)
* Tick-based simulation
* Frontend visualization

## Tasks

### Backend

* [ ] Setup SimulationEngine with tick scheduler
* [ ] Implement BaseAgent, CitizenAgent, StateLeaderAgent
* [ ] Create Nation & State models
* [ ] Rule-based budget allocation
* [ ] Simple election logic
* [ ] In-memory state store

### Frontend

* [ ] Nation map view
* [ ] Color-coded agents (blue, green, yellow placeholders)
* [ ] Time control (play/pause/speed)
* [ ] Basic metrics dashboard

## Deliverables

* Running simulation with visible agents
* Deterministic outcomes
* No ML dependencies

## Exit Criteria

* Elections complete without errors
* States show different outcomes

---

# plan-phase-2.md – Elections, Economy & Metrics

## Goal

Introduce **realistic incentives** and measurable outcomes.

## Scope

* Economic growth model
* Trust & happiness dynamics
* Corruption (hidden variable)

## Tasks

### Backend

* [ ] EconomyService implementation
* [ ] CorruptionModel (actual vs perceived)
* [ ] Trust calculation engine
* [ ] Metrics aggregation service
* [ ] Historical event logging

### Frontend

* [ ] Economy & trust graphs
* [ ] Election result visualization
* [ ] State comparison dashboard

## Deliverables

* Measurable differences between states
* Metrics driving elections

## Exit Criteria

* Poor leadership leads to election loss
* Corruption impacts trust indirectly

---

# plan-phase-3.md – Reinforcement Learning Leaders

## Goal

Enable **adaptive leadership behavior** using RL.

## Scope

* RL for state leaders
* Fixed citizen behavior

## Tasks

### ML

* [ ] Define state–action–reward schema
* [ ] Implement policy-based RL (PPO / DQN)
* [ ] Training loop per episode
* [ ] Policy persistence

### Backend

* [ ] RLPolicy interface
* [ ] Inject policy into StateLeaderAgent
* [ ] Reward feedback loop

### Frontend

* [ ] Toggle RL vs rule-based leaders
* [ ] Show learning curves

## Deliverables

* Leaders improve over time
* Different learned strategies emerge

## Exit Criteria

* RL leaders outperform rule-based leaders

---

# plan-phase-4.md – Social Dynamics & Emergence

## Goal

Simulate **opinion formation, propaganda, and emergent ideologies**.

## Scope

* Influence graph
* Media agents
* Unsupervised clustering

## Tasks

### Backend

* [ ] InfluenceGraph implementation
* [ ] PropagandaService
* [ ] Opinion diffusion model

### ML

* [ ] K-means / community detection
* [ ] Ideology labeling

### Frontend

* [ ] Opinion heatmaps
* [ ] Media influence visualization

## Deliverables

* Opinion clusters emerge naturally
* Propaganda affects perception

## Exit Criteria

* Visible polarization patterns

---

# plan-phase-5.md – Advanced AI & Ethics Layer

## Goal

Introduce **moral ambiguity and high-order learning**.

## Scope

* Fuzzy logic
* GNN-based influence
* Supreme leader RL

## Tasks

### ML

* [ ] Fuzzy inference engine
* [ ] GNN for influence spread
* [ ] Supreme leader policy learning

### Backend

* [ ] Multi-level reward balancing
* [ ] Ethical trade-off metrics

### Frontend

* [ ] Ethics sliders
* [ ] Democracy & stability indices

## Deliverables

* Non-linear, realistic political behavior
* Ethical trade-offs visible

## Exit Criteria

* System shows multiple stable/unstable regimes

---

# plan-phase-6.md – Scale, Experiments & Research Mode

## Goal

Turn system into a **research & experimentation platform**.

## Scope

* Multi-nation support
* External shocks
* Scenario replay

## Tasks

* [ ] Multi-nation simulation
* [ ] Disaster & war events
* [ ] Replay & export system
* [ ] Parameter sweeps

## Deliverables

* Experiment-ready platform

## Exit Criteria

* Deterministic replay works
* Large-scale simulations stable

---

## 17. Global AI-Agent Prompts (STRICT RULES)

The following prompts **must be given to every AI agent** involved in this project. These are **non-negotiable system-level constraints** to ensure architectural consistency, correctness, and long-term scalability.

---

# GLOBAL SYSTEM PROMPT (APPLIES TO ALL AGENTS)

> You are an AI software engineer working on a **multi-agent swarm governance simulation**.
>
> You MUST strictly follow the provided **LLD and plan.md for the current phase**.
>
> You are NOT allowed to:
>
> * Invent new architectures
> * Skip layers
> * Merge responsibilities
> * Introduce frameworks without justification
>
> All implementations MUST:
>
> * Be modular
> * Be testable
> * Be deterministic unless explicitly stated otherwise
> * Preserve backward compatibility

---

# PROMPT 1 – ARCHITECTURE GUARDRAIL AGENT

## Role

Ensure **SOLID compliance and clean separation of concerns**.

## Rules

* One class = one responsibility
* Agents must NOT directly call ML models
* Learning strategies MUST be injected
* Simulation engine must remain framework-agnostic

## You MUST reject code that:

* Couples UI with logic
* Hardcodes learning behavior
* Breaks BaseAgent abstraction

---

# PROMPT 2 – BACKEND IMPLEMENTATION AGENT

## Role

Implement backend services strictly from LLD.

## Rules

* Follow naming exactly as in LLD
* Do NOT add endpoints not specified
* All state changes must go through SimulationEngine
* Time progression ONLY via ticks

## Output Requirements

* Clean folder structure
* Clear interfaces
* Inline comments explaining decisions

---

# PROMPT 3 – AGENT BEHAVIOR AGENT

## Role

Implement agent decision logic.

## Rules

* No randomness without seed
* Citizens are rule-based unless phase >= 4
* Leaders delegate decisions to policy modules

## You MUST

* Keep hidden vs visible state separate
* Log all agent actions as events

---

# PROMPT 4 – ML / LEARNING AGENT

## Role

Implement learning components ONLY when enabled by plan.md.

## Rules

* No ML in Phase 1
* RL only affects leaders
* Training must be reproducible
* State, action, reward must be logged

## You MUST NOT

* Modify agent core logic
* Add black-box learning without explainability

---

# PROMPT 5 – FRONTEND / VISUALIZATION AGENT

## Role

Build visual layer that reflects backend state.

## Rules

* Frontend is read-only with respect to simulation state
* Use WebSocket for real-time updates
* Never recompute logic in UI

## You MUST

* Preserve color coding
* Keep UI stateless where possible

---

# PROMPT 6 – DATA & METRICS AGENT

## Role

Ensure observability and analytics.

## Rules

* Every major event must emit a metric
* Metrics must be phase-aware
* No silent state changes

---

# PROMPT 7 – INTEGRATION & REVIEW AGENT

## Role

Validate system-wide correctness.

## Checklist

* Does code match LLD?
* Does phase scope remain intact?
* Are abstractions respected?
* Are results reproducible?

## Authority

This agent may REJECT any contribution.

---

## 18. Project-Wide Non-Functional Constraints

* Deterministic simulation by default
* Event-driven state updates
* No circular dependencies
* Explicit configuration for randomness
* Logs > assumptions

---

## END OF LLD

This completes the system-level LLD with execution-ready phase plans.



I’ve added a **strict, project-wide set of AI-agent prompts** to the LLD canvas.

### Why these prompts matter

These are not “helpful hints” — they act as **constitutional rules** for every agent that touches the project. If you use them correctly:

* ❌ Agents won’t invent architectures
* ❌ ML won’t leak into early phases
* ❌ Frontend won’t reimplement logic
* ❌ RL won’t silently mutate agent behavior
* ✅ The system will stay **modular, explainable, and evolvable**

This is exactly how **large agentic codebases** are kept sane.

---

### How you should actually use these

For every AI interaction, prepend **two layers**:

1. **Global System Prompt** (always)
2. **Role-Specific Prompt** (Backend / ML / Frontend / Review)

Then append:

* Current **phase plan.md**
* Relevant **LLD section**

This forces the agent to reason *inside* your system, not around it.

---

### Recommended next artifacts (high leverage)

Pick one:

1. **Repo & folder structure** aligned with these prompts
2. **Phase-1 concrete tasks broken into tickets**
3. **Database schema + event log format**
4. **Exact RL tensor definitions (Phase 3)**
5. **Code review checklist for Integration Agent**

If you want maximum control, say:

> **“Create repository folder structure enforced by these agent prompts”**

You’re now operating at a level where **AI becomes a workforce, not a helper**.
