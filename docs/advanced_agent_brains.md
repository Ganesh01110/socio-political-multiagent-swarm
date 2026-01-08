# Advanced Agent Brains & Economic Feedback Loops

## Why?
The core goal of this upgrade was to transform the Sworm System from a simple agent simulation into a complex socio-political laboratory.
- **Non-Linear Dynamics**: Human society isn't deterministic. By adding `Ideology` and `Cognitive Bias`, we ensure that the same economic conditions can lead to different social outcomes.
- **Leader Accountability**: In political simulations, leaders shouldn't just exist; they must perform. The new system allows the Supreme Leader to evaluate and "fire" incompetent or corrupt subordinates.
- **Economic Realism**: Economic metrics like inflation and unemployment serve as the "environment" that constraints agent choices, creating a realistic pressure-cooker for social simulation.

## What?
This implementation introduces a hierarchical decision-making architecture:

### 1. The Brain Stack (Strategy Pattern)
Individual agents are assigned a **Policy** based on their role:
- **ANN (Neural Network)**: Standard intelligence for all citizens and state leaders (16 hidden nodes). Ensures "human-level" baseline intelligence equality.
- **DQN (Deep Q-Learning)**: Long-horizon strategic planning reserved for the Supreme Leader only.
- **Hybrid Brain**: (Legacy) Multi-layered architecture for complex agents, utilizing Random Forests for perception and kNN for social clustering.

**Intelligence Equality**: To simulate realistic human society, all citizens and state leaders now use the same ANN architecture. This prevents "super-intelligent" leaders from dominating and creates more emergent, unpredictable dynamics.


### 2. Socio-Economic Feedback Loops
- **The Triangle of Instability**: Inflation, Unemployment, and Inequality now interact in a closed loop, affecting agent happiness and trust.
- **Inheritance & Taxation**: Agents have finite lifespans. Upon death, they pass on wealth minus a configurable **Inheritance Tax (1-60%)**.
- **Corruption Efficiency**: Variable settings determine the ROI of corrupt leadership actions, balancing greed with state stability.
- **Variable Population**: Natural growth cycles with **1 to 3 children** per dying agent prevent static demographic stagnation.
- **Narrative Warfare & Mastery**: Media agents manipulate public truth. Users can override ownership-based bias with global stances: **Neutral**, **State Ally**, or **Anti-State**, triggering specific disinformation headlines in the feed.
- **Regime Stability (Coups)**: Implements non-electoral leader removal. Triggers when `avg_trust < 20` and `protest_intent > 0.6`. Deposed leaders face a major RL learning penalty (-500).


### 4. Fuzzy Logic Morality
The system now includes a **Fuzzy Inference System (FIS)** for moral reasoning:
- **Shades of Gray**: Decisions aren't binary. Agents evaluate their `moral_resistance` based on a fuzzy combination of Greed, Trust, and External Pressure (Inflation/Unemployment).
- **Behavioral Filtering**: High moral resistance can "overrule" corrupt strategic choices (like stealing funds), forcing agents toward pro-social behaviors even when a purely greedy strategy would yield higher personal utility.

## How?
The system is built on a modular Python back-end:

### Core Files
- **[`brain_stack.py`](../backend/app/ml/brain_stack.py)**: The engine of the strategy pattern.
- **[`engine.py`](../backend/app/core/engine.py)**: The orchestration layer that triggers decisions, propagates influence, and updates global economics.
- **[`economy.py`](../backend/app/core/economy.py)**: Translates agent actions into macroeconomic shifts.
- **[`social.py`](../backend/app/core/social.py)**: Manages ideological clusters and peer-to-peer influence.

### Running a Test
You can verify the entire stack, including the economic oscillations and brain selection, by running:
```powershell
# Set PYTHONPATH and run the verification script
$env:PYTHONPATH="backend"
python verify_advanced_strategies.py
```

### Key Metrics Tracked
- **Trust Scores**: Public perception of leadership.
- **Corruption Level**: Funds diverted by leaders.
- **Ideological Proximity**: How "echo chambers" form based on shared vectors.
- **Protest Intent**: Propensity of agents to join social movements.

---

## 5. Social Circles & Threshold Influence (Tipping Points)
The latest upgrade introduces a **Social Graph** layer:
- **Explicit Connections**: Agents are no longer solely influenced by spatial proximity. They have specific `social_links` representing friends, colleagues, or political networks.
- **The 50% Rule (Tipping Point)**: Implements threshold-based collective behavior. If more than 50% of an agent's circle shares a specific state (e.g., trust < 30), the agent's trust drops exponentially faster. This creates realistic "cascading failures" in public trust.
- **Political Consequences**: 
    - **Coup d'état**: If aggregate national trust falls below a critical threshold while protest intent is high, a coup can occur, replacing the leader outside of the election cycle.
    - **Fear & Pressure**: Voting logic now accounts for peer pressure from social circles and fear induced by propaganda.
    - **Unemployment Factor**: If active, high per-state unemployment adds a heavy penalty to the incumbent's re-election probability (calculates as `- (unemployment_rate * 400)` points).
    - **Dynamic Cronyism**: Social networks are no longer static. Wealthy citizens (Top 10%) have a 40% chance of forming links with leaders, while old links can decay over time. 
    - **Cronyism in Voting**: Agents in a leader's social circle who have been economically favored vote for the incumbent with 95% probability.


## 6. Simulation Control Toggles
The latest version introduces **runtime control** over citizen mechanics:

### Citizen Variable Toggles
- **Hope Mechanic**: Controls whether hope affects economic risk-taking
- **Trust Decay**: Natural erosion of trust over time (-0.5 per tick)
- **Happiness Influence**: Whether happiness affects productivity and voting
- **Memory Loss**: 10% of citizens periodically forget past grievances (resets trust/happiness every 20 ticks)
- **Ideology Shift**: Beliefs gradually shift toward peer average based on social pressure

### Dynamic Media Ownership
- **Ownership Types**: Industrialist, Politician Ally, Common Citizen, External Factor, Independent
- **Bias Calculation**: Media bias changes based on who owns it
  - Politician-owned media: Strongly pro-establishment (+0.8 bias)
  - Industrialist-owned: Pro-business (+0.4 to +0.6)
  - Common citizen-owned: Populist/anti-establishment (-0.3 to -0.8)
- **Narrative Propagation**: Media influences citizen trust, fear, and protest intent based on bias



---

## Pros & Cons

### ✅ Advantages
- **Emergent Complexity**: Realistic social phenomena like polarization and echo chambers emerge naturally from agent interactions.
- **Modular Scalability**: The Strategy Pattern allows researchers to plug in new AI models (e.g., Transformers, Fuzzy Logic) without changing the core engine.
- **Dynamic Feedback**: Economic loops (Inflation/Unemployment) create a "living" environment where agent decisions have tangible consequences.

### ❌ Disadvantages
- **Computational Cost**: Running dozens of RL agents and ML models in parallel increases CPU/Memory overhead compared to simple rule-based scripts.
- **Explainability**: Identifying exactly *why* a Hybrid Brain chose a specific action can be challenging due to the ensemble of models involved.
- **Sensitivity**: Small changes in initial synthetic distributions (e.g., slightly lower education) can lead to drastically different societal outcomes (Butterly Effect).

---

## 🔮 Future Ideas & Integration
- **Cultural Evolution**: Using Federated Learning concepts to allow agents to "pass down" successful decision-making patterns to the next generation.
- **LLM-Reasoning**: Integrating LLMs to generate natural language explanations for agent decisions.
- **Global Trade Layer**: Expanding the economy to include resource trading between different state simulations.

