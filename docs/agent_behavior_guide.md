# Sworm System: Agent Behavior & Transaction Guide

This document explains the step-by-step logic, financial transactions, and AI model architecture for each agent role in the simulation.

## 🔄 The Simulation Loop (Tick-by-Tick)

In every **Tick**, the following sequence occurs:

1.  **Tax Collection**: The **Supreme Leader** collects a percentage of wealth from all **State Leaders**.
2.  **Resource Allocation**: The Supreme Leader distributes the national budget to the States based on their performance and needs.
3.  **Local Decision (RL)**: Each **State Leader** looks at their state's metrics (Trust, Wealth, Happiness) and chooses an action: *Invest*, *Steal*, *Maintain*, or *Propaganda*.
4.  **Economic Execution**:
    -   Funds flow from the Leader to the **Citizens**.
    -   If the leader *Steals*, money moves to their personal vault; Citizens get less.
    -   If the leader *Invests*, Citizens receive a wealth boost.
5.  **Social Influence**: Citizens talk to their neighbors (**Social Links**). If most friends are unhappy or distrust the leader, the individual's trust also drops (**Tipping Point**).
6.  **Simulation Mechanics** (if enabled via toggles):
    -   **Memory Loss**: 10% of citizens periodically forget past grievances (trust/happiness reset)
    -   **Trust Decay**: Natural erosion of trust over time
    -   **Ideology Shift**: Beliefs change based on peer pressure
7.  **Media Influence**: Media outlets propagate narratives based on their ownership (Industrialist, Politician Ally, Common Citizen, External Factor, or Independent). Bias affects citizen trust and protest intent.
8.  **Political Check**: The system checks for **Protests** or **Coups**. If conditions are met, the leader is replaced.
9.  **Election (Every 50 Ticks)**: Citizens vote. Incumbents benefit from **Cronyism** (favored circle) and **Fear**, but lose to **Ideological Dissent**.


---

## 👥 Agent Specifications

### 1. Common People (Citizens)
-   **Inputs (NN State)**: `[Personal Trust, Personal Wealth, Avg Happiness, State Budget, Inflation, Unemployment, Inequality]`
-   **Decision Logic**: Standard Neural Brain (ANN).
-   **Expected Behavior**:
    -   Generate small amounts of wealth.
    -   Vote based on `Trust` and `Fear`.
    -   If `Wealth` < 10 and `Trust` < 30,participate in **Protests**.
-   **Outputs (NN Action)**: `[Protest, Comply, Support, Ignore]`

### 2. State Leader
-   **Inputs (NN State)**: `[Global Trust, State Wealth, Avg Happiness, Allocated Budget, Inflation, Unemployment, Inequality]`
-   **Decision Logic**: Standard Neural Brain (ANN) focusing on **Greed vs. Survival**.
-   **Considerations (Toggles)**:
    -   `Trust`: Reward for high approval.
    -   `Fear`: Reward for compliance/intimidation.
    -   `Happiness/Wealth`: Reward for citizen prosperity.
-   **Expected Behavior**:
    -   *Steal* when re-election is guaranteed (High Trust).
    -   *Propaganda* when Trust is falling.
    -   *Invest* to recover from economic depression.
-   **Outputs (NN Action)**: `[Invest (0), Steal (1), Maintain (2), Propaganda (3)]`

### 3. Supreme Leader
-   **Decision Logic**: Deep Q-Learning (DQN) for long-horizon planning.
-   **Expected Behavior**: 
    -   Redistributes national wealth to stabilize the economy.
    -   Fires State Leaders whose trust falls below 20%.
-   **Transactions**: Moving large chunks of `National Budget` to `State Budgets`.

### 4. Media Institute (Level 3 Agent)
-   **Ownership Types**: INDUSTRIALIST, POLITICIAN_ALLY, COMMON_CITIZEN, EXTERNAL_FACTOR, INDEPENDENT
-   **Ownership Determination**: Based on social connections. Politicians have priority, then industrialists (wealthy citizens), then common citizens.
-   **Bias Calculation**:
    -   Politician-owned: +0.8 (strongly pro-establishment)
    -   Industrialist-owned: +0.4 to +0.6 (pro-business, varies with owner happiness)
    -   Common citizen-owned: -0.3 to -0.8 (populist, anti-establishment if trust is low)
    -   External factor: -0.8 to +0.8 (unpredictable)
    -   Independent: -0.2 to +0.2 (neutral)
-   **Expected Behavior**: 
    -   Pro-establishment media boosts citizen trust and fear
    -   Anti-establishment media reduces trust and increases protest intent
    -   Disinformation randomly shifts perceptions

### 5. Simulation Control Toggles
The simulation supports runtime toggles for citizen mechanics:
-   **Hope Mechanic**: When enabled, hope affects economic risk-taking behavior
-   **Trust Decay**: Natural erosion of trust over time (-0.5 per tick)
-   **Happiness Influence**: Whether happiness affects productivity
-   **Memory Loss**: 10% of citizens periodically forget past grievances (every 20 ticks)
-   **Ideology Shift**: Beliefs gradually shift toward peer average (10% per tick)


---

## 💰 Money Transaction Flow

| Source | Target | Trigger | Effect |
| :--- | :--- | :--- | :--- |
| **State Leader** | **Citizens** | *Invest Action* | High wealth transfer, high Trust boost. |
| **State Leader** | **Personal Vault** | *Steal Action* | High personal wealth, high Trust penalty. |
| **Supreme Leader** | **State Leader** | *Tick 1* | Allocates operating budget. |
| **Citizens** | **State Leader** | *Tax* | Small deductions (re-circulated). |

## 🧠 Model Detail: The Standard Brain (ANN)
To ensure all agents have a "human-level" baseline of intelligence without lagging your PC:
-   **Architecture**: Multi-Layer Perceptron (7 inputs -> 16 hidden nodes -> 4 outputs).
-   **Performance**: Uses vectorization. Handling 1,000 agents with this model is equivalent to a single matrix multiplication, which is nearly instant on modern CPUs.
