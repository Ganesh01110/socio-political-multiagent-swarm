# Advanced Agent Brains & Economic Feedback Loops

## Why?
The core goal of this upgrade was to transform the Sworm System from a simple agent simulation into a complex socio-political laboratory.
- **Non-Linear Dynamics**: Human society isn't deterministic. By adding `Ideology` and `Cognitive Bias`, we ensure that the same economic conditions can lead to different social outcomes.
- **Leader Accountability**: In political simulations, leaders shouldn't just exist; they must perform. The new system allows the Supreme Leader to evaluate and "fire" incompetent or corrupt subordinates.
- **Economic Realism**: Economic metrics like inflation and unemployment serve as the "environment" that constraints agent choices, creating a realistic pressure-cooker for social simulation.

## What?
This implementation introduces a hierarchical decision-making architecture:

### 1. The Brain Stack (Strategy Pattern)
Individual agents no longer have hardcoded logic. Instead, they are assigned a **Policy**:
- **RuleBased**: High-efficiency logic for general citizens.
- **ANN (Neural Network)**: Adaptive logic for influencers and activists.
- **DQN (Deep Q-Learning)**: Long-horizon strategic planning for state and supreme leaders.
- **Hybrid Brain**: A multi-layered architecture for complex agents, utilizing Random Forests for perception and kNN for social clustering.

### 2. Socio-Economic Feedback Loops
- **The Triangle of Instability**: Inflation, Unemployment, and Inequality now interact in a closed loop, affecting agent happiness and trust.
- **Narrative Warfare**: Media agents operate with `disinformation_rate` and `algorithmic_amplification` to manipulate the simulation's "truth."

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
- **Fuzzy Logic Morality**: Implementing a "Conscience" layer where agents evaluate the ethical weight of their actions beyond pure utility.
- **Cultural Evolution**: Using Federated Learning concepts to allow agents to "pass down" successful decision-making patterns to the next generation.
- **LLM-Reasoning**: Integrating LLMs to generate natural language explanations for agent decisions (e.g., *"I chose to protest because my trust in the leader is low and my neighbors are unhappy"*).
- **Global Trade Layer**: Expanding the economy to include resource trading between different state simulations.
