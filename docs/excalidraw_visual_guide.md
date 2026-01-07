# SWORM SYSTEM - Excalidraw Visual Documentation
Copy-paste these text blocks into Excalidraw to create your visual architecture diagram

---

## MAIN TITLE BOX
```
SWORM SYSTEM
Multi-Agent Socio-Political Simulation
Exploring Emergent Dynamics of Power, Resources & Influence
```

---

## WHY - THE VISION

```
WHY THIS PROJECT?

Traditional simulations treat agents as identical units.
Real societies have:
• Power hierarchies
• Information asymmetry
• Economic feedback loops
• Social tipping points

GOAL: Create a living laboratory for political economy
where realistic social phenomena emerge naturally from
agent interactions.
```

---

## WHAT - THE SYSTEM

```
WHAT IS IT?

A hierarchical multi-agent simulation modeling:
✓ 5 Agent Types (Citizens → Supreme Leader)
✓ Economic Feedback (Inflation/Unemployment)
✓ Social Dynamics (Trust, Fear, Ideology)
✓ Political Systems (Elections, Coups, Cronyism)
✓ Media Influence (Dynamic Ownership & Bias)
✓ Behavioral Controls (10+ Runtime Toggles)

Tech Stack:
• Backend: FastAPI + PyTorch + Scikit-Learn
• Frontend: React + TypeScript + PixiJS
• AI: ANN (16-node MLP) + DQN + Fuzzy Logic
```

---

## HOW - THE ARCHITECTURE

```
HOW IT WORKS - AGENT HIERARCHY

Level 4: EXTERNAL FACTORS (Grey)
└─ Global events: Pandemics, Economic Booms, Disasters

Level 3: MEDIA INSTITUTES (Purple)
└─ Ownership: Industrialist/Politician/Citizen/External
└─ Bias: -1.0 (anti-establishment) to +1.0 (pro-govt)
└─ Influence: Trust, Fear, Protest Intent

Level 2: SUPREME LEADER (Yellow)
└─ AI: Deep Q-Learning (DQN)
└─ Role: National budget allocation
└─ Power: Fire incompetent state leaders

Level 1: STATE LEADERS (Green)
└─ AI: Standard Neural Network (ANN)
└─ Actions: Invest, Steal, Maintain, Propaganda
└─ Constraints: Re-election pressure, Cronyism

Level 0: CITIZENS (Blue)
└─ AI: Standard Neural Network (ANN)
└─ Behavior: Vote, Protest, Generate Wealth
└─ Mechanics: Memory Loss (10%), Trust Decay, Ideology Shift
```

---

## SIMULATION LOOP - TICK SEQUENCE

```
EVERY TICK (Simulation Step):

1. TAX COLLECTION
   Supreme Leader → State Leaders (Budget Extraction)

2. RESOURCE ALLOCATION
   Supreme Leader → States (Performance-based Distribution)

3. AGENT DECISIONS (Neural Networks)
   State Leaders choose: Invest/Steal/Maintain/Propaganda
   Citizens decide: Support/Protest/Comply

4. ECONOMIC EXECUTION
   Money flows: Leader → Citizens
   Effects: Wealth changes, Trust impacts

5. SOCIAL INFLUENCE (Threshold Dynamics)
   If >50% of friends distrust leader → Rapid trust drop
   Ideology shifts toward peer average (10% per tick)

6. MEDIA PROPAGATION
   Ownership determines bias
   Narratives affect: Trust, Fear, Protest Intent

7. SIMULATION MECHANICS (If Enabled)
   • Memory Loss: 10% forget grievances (every 20 ticks)
   • Trust Decay: Natural erosion (-0.5 per tick)
   • Ideology Shift: Peer pressure convergence

8. POLITICAL CHECKS
   Coup Check: Trust <20 + Protest >0.7 → Leader replaced
   Election (every 50 ticks): Cronyism vs Ideology

9. SAVE METRICS
   National + Per-State history to database
```

---

## KEY SYSTEMS - DETAILED BREAKDOWN

### SYSTEM 1: UNIFIED INTELLIGENCE
```
UNIFIED INTELLIGENCE SYSTEM

WHY: Prevent "super-intelligent" leaders from dominating
     Simulate human-level equality

WHAT: All citizens & state leaders use same ANN
      (16 hidden nodes, 7 inputs → 4 outputs)
      Only Supreme Leader has DQN (long-horizon planning)

HOW: Strategy Pattern
     • ANNPolicy for Citizens & State Leaders
     • DQNPolicy for Supreme Leader only
     
RESULT: Emergent, unpredictable dynamics
        More realistic power struggles
```

### SYSTEM 2: POLICY-AWARE REWARDS
```
POLICY-AWARE REWARD SYSTEM

WHY: Leaders should be able to ignore/consider
     different aspects of public opinion

WHAT: 4 Emotion Toggles (Runtime Control)
      ✓ Consider Trust
      ✓ Consider Fear
      ✓ Consider Happiness
      ✓ Consider Wealth

HOW: Leader reward = f(personal_gain, trust_change,
                       happiness, fear, wealth)
     Each factor can be enabled/disabled via API

RESULT: Researchers can isolate specific motivations
        Study how ignoring public welfare affects stability
```

### SYSTEM 3: CRONYISM IN ELECTIONS
```
CRONYISM MECHANICS

WHY: Real elections involve patronage networks
     Money buys loyalty (usually)

WHAT: Favored citizens vote for incumbent
      • "Favored" = In leader's social circle
                  + Wealth >120% of average
      • 95% probability to vote incumbent
      
      OVERRIDE: "Principled Dissent"
      • If ideology differs by >0.7
      • Principles > Profit

HOW: Election logic checks:
     1. Is voter in leader's social_links?
     2. Has voter been economically favored?
     3. Is ideological difference extreme?
     
RESULT: Realistic patronage vs ideology tension
```

### SYSTEM 4: DYNAMIC MEDIA OWNERSHIP
```
DYNAMIC MEDIA OWNERSHIP

WHY: Media isn't neutral
     Ownership shapes editorial stance

WHAT: 5 Ownership Types
      • Industrialist (Pro-business, +0.4 to +0.6 bias)
      • Politician Ally (Pro-govt, +0.8 bias)
      • Common Citizen (Populist, -0.3 to -0.8 bias)
      • External Factor (Unpredictable, -0.8 to +0.8)
      • Independent (Neutral, -0.2 to +0.2)

HOW: Ownership determined by social_links
     Priority: Politician > Industrialist > Citizen
     Bias affects: Trust, Fear, Protest Intent
     
RESULT: Fourth estate with realistic conflicts of interest
```

### SYSTEM 5: SIMULATION CONTROL TOGGLES
```
CITIZEN MECHANICS TOGGLES

WHY: Isolate and study specific social dynamics
     Enable/disable behaviors for research

WHAT: 5 Runtime Controls
      ✓ Hope Mechanic (Economic risk-taking)
      ✓ Trust Decay (Natural erosion -0.5/tick)
      ✓ Happiness Influence (Productivity impact)
      ✓ Memory Loss (10% forget every 20 ticks)
      ✓ Ideology Shift (Peer pressure 10%/tick)

HOW: simulation_settings dictionary
     Checked every tick in engine.advance()
     API: GET/POST /api/simulation/settings
     
RESULT: Configurable social laboratory
        Test "what if" scenarios
```

### SYSTEM 6: SOCIAL GRAPH & TIPPING POINTS
```
THRESHOLD-BASED INFLUENCE

WHY: Social change isn't gradual
     Tipping points cause rapid shifts

WHAT: Explicit social_links between agents
      50% Rule: If >50% of friends share state
                → Individual rapidly adopts that state
      
      Example: If >50% of friends distrust leader
               → Your trust drops exponentially

HOW: propagate_influence() checks peer states
     Counts friends in each state
     Triggers cascade if threshold exceeded
     
RESULT: Realistic "echo chambers"
        Sudden societal shifts
        Cascading trust failures
```

---

## DATA FLOW DIAGRAM

```
DATA FLOW - API TO DATABASE

Frontend (React)
    ↓ HTTP Requests
FastAPI Endpoints
    ↓ /api/simulation/tick
SimulationEngine
    ↓ advance()
    ├─→ EconomyService (Budget distribution)
    ├─→ SocialService (Influence propagation)
    ├─→ MediaService (Narrative propagation)
    ├─→ ElectionService (Voting & Coups)
    └─→ SupremeLeaderService (Tax & Fire leaders)
    ↓ _save_history()
SQLite Database
    ├─→ National metrics (state_id = NULL)
    └─→ Per-state metrics (state_id = "state_0", etc.)
    ↑ Query
Frontend Charts (Tabbed: National vs States)
```

---

## TECHNOLOGY STACK LAYERS

```
TECH STACK - LAYERED VIEW

┌─────────────────────────────────────┐
│  FRONTEND LAYER                     │
│  • React + TypeScript               │
│  • PixiJS (Agent Rendering)         │
│  • Recharts (Analytics)             │
│  • Axios (API Client)               │
└─────────────────────────────────────┘
           ↕ HTTP/REST
┌─────────────────────────────────────┐
│  API LAYER                          │
│  • FastAPI (Python)                 │
│  • Pydantic (Validation)            │
│  • CORS Middleware                  │
└─────────────────────────────────────┘
           ↕ Function Calls
┌─────────────────────────────────────┐
│  BUSINESS LOGIC LAYER               │
│  • SimulationEngine (Orchestration) │
│  • Services: Economy, Social, Media │
│  • Strategy Pattern (Brain Stack)   │
└─────────────────────────────────────┘
           ↕ Model I/O
┌─────────────────────────────────────┐
│  AI/ML LAYER                        │
│  • PyTorch (DQN for Supreme Leader) │
│  • ANN (16-node MLP for others)     │
│  • Scikit-Fuzzy (Morality FIS)      │
│  • Scikit-Learn (Hybrid models)     │
└─────────────────────────────────────┘
           ↕ ORM
┌─────────────────────────────────────┐
│  PERSISTENCE LAYER                  │
│  • SQLAlchemy (ORM)                 │
│  • SQLite / MariaDB                 │
│  • Per-state history tracking       │
└─────────────────────────────────────┘
```

---

## AGENT DECISION INPUTS/OUTPUTS

```
NEURAL NETWORK I/O

STATE VECTOR (7 Inputs):
[0] Trust Score (0-1)
[1] Wealth (0-1, normalized)
[2] Happiness (0-1)
[3] Budget Allocated (0-1, normalized)
[4] Inflation Rate (0-1)
[5] Unemployment Rate (0-1)
[6] Inequality (Gini-like, 0-1)

↓ Neural Network (16 hidden nodes)

ACTION OUTPUT (4 Actions):
[0] Invest (Boost citizen wealth, +Trust)
[1] Steal (Personal gain, -Trust)
[2] Maintain (Status quo)
[3] Propaganda (Media manipulation, +Fear)

LEARNING:
• Policy Gradient (ANN)
• Experience Replay (DQN)
• Fuzzy Morality Override (High resistance → Force prosocial)
```

---

## MONEY TRANSACTION FLOWS

```
ECONOMIC TRANSACTIONS

Supreme Leader (National Budget)
    ↓ Tax (% of state budgets)
State Leaders (State Budgets)
    ↓ Allocation based on performance
State Leaders
    ↓ Action-based distribution
    ├─→ INVEST: High transfer → Citizens (+Trust)
    ├─→ STEAL: Low transfer → Citizens, High → Leader (-Trust)
    ├─→ MAINTAIN: Moderate transfer
    └─→ PROPAGANDA: Budget → Media (+Fear, ±Trust)
Citizens (Wealth)
    ↓ Generate small amounts per tick
    ↓ Vote based on Trust + Fear + Social Pressure
Elections (Every 50 ticks)
    → Leader Replacement (if lost)
    → Cronyism: Favored vote incumbent (95%)
```

---

## POLITICAL CONSEQUENCES

```
POLITICAL STABILITY MECHANICS

NORMAL STATE:
Trust >30, Protest <0.5
→ Stable governance

WARNING STATE:
Trust 20-30, Protest 0.5-0.7
→ Social unrest, media amplification

COUP THRESHOLD:
Trust <20 AND Protest >0.7
→ 30% chance of coup per check (every 10 ticks)
→ Leader replaced outside election cycle

ELECTION (Every 50 ticks):
Regular voting + Cronyism
→ Favored citizens (wealth >120% avg) vote incumbent
→ Override if ideology differs >0.7
→ Fear increases incumbent votes
→ Social pressure from peer circle
```

---

## VISUAL LAYOUT SUGGESTIONS FOR EXCALIDRAW

```
SUGGESTED DIAGRAM LAYOUT:

TOP SECTION:
├─ Title Box (Center)
├─ WHY-WHAT-HOW (3 columns)

MIDDLE SECTION (Main Architecture):
├─ Agent Hierarchy (Left side, vertical stack)
│  └─ External → Media → Supreme → State → Citizens
├─ Simulation Loop (Center, circular flow)
├─ Tech Stack (Right side, layered boxes)

BOTTOM SECTION:
├─ Key Systems (6 boxes in 2 rows)
│  Row 1: Intelligence | Rewards | Cronyism
│  Row 2: Media | Toggles | Social Graph
├─ Data Flow (Horizontal pipeline)
├─ Money Flow (Vertical cascade)

CONNECTIONS:
• Use arrows to show data flow
• Color-code by agent type (match legend)
• Group related systems with rounded rectangles
• Add icons: 💰 (money), 🗳️ (vote), 📊 (data), 🧠 (AI)
```

---

## COLOR SCHEME RECOMMENDATIONS

```
EXCALIDRAW COLOR PALETTE:

Agent Types:
• Citizens: #2196F3 (Blue)
• State Leaders: #4CAF50 (Green)
• Supreme Leader: #FFEB3B (Yellow)
• Media: #9C27B0 (Purple)
• External: #757575 (Grey)

Systems:
• AI/ML: #FF5722 (Deep Orange)
• Economy: #4CAF50 (Green)
• Social: #2196F3 (Blue)
• Political: #F44336 (Red)
• Data: #607D8B (Blue Grey)

Backgrounds:
• Headers: Light grey (#F5F5F5)
• Important: Light yellow (#FFF9C4)
• Warning: Light red (#FFCDD2)
```

---

## QUICK FACTS FOR CALLOUT BOXES

```
📊 SCALE
• 5 Agent Types
• 100+ Citizens per simulation
• 3 Media Outlets
• 5 States + 1 Supreme Leader
• 50-tick election cycles

🧠 AI MODELS
• ANN: 16 hidden nodes
• DQN: Experience replay buffer
• Fuzzy Logic: 3-input morality FIS
• 7 state inputs → 4 action outputs

⚙️ CONTROLS
• 4 Policy Toggles (Leaders)
• 5 Citizen Mechanics Toggles
• Runtime API configuration
• Per-state analytics

🎯 EMERGENT BEHAVIORS
• Echo chambers
• Cascading trust failures
• Coup d'états
• Patronage networks
• Media bias effects
```

---

## COPY-PASTE READY SUMMARY BOX

```
SWORM SYSTEM - ONE-SENTENCE SUMMARY

A multi-agent socio-political simulation where 100+ AI-driven
citizens interact with leaders, media, and external events to
produce emergent social phenomena like coups, cronyism, and
tipping points—all controllable via runtime toggles for
research and experimentation.

Built with: FastAPI + React + PyTorch + ANN/DQN
Features: 5 agent types, 10+ toggles, dynamic media ownership
Result: Living laboratory for political economy
```
