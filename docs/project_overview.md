# Sworm System: Project Overview

## Description
The Sworm System is a sophisticated socio-economic simulation designed to study the interplay between individual citizen behavior, local leadership strategies, and top-down national governance. 

By combining **Reinforcement Learning (RL)** with agent-based modeling, the system simulates a world where leaders must learn to survive re-election cycles while fulfilling their own greed or investing in their people.

## Key Components

### 1. The Sworm Economy
Money is the lifeblood of the simulation. It originates from the Supreme Leader and trickles down through State Leaders to the Citizens. Corruption (stealing) at the leader level directly impacts citizen happiness and trust.

### 2. Multi-Layered AI Brain Stack
Agents are no longer limited to simple Q-Learning. The system uses a **Strategy Pattern** for hierarchical intelligence:
- **DQN / Reinforcement Learning:** Strategic planning for leaders.
- **Ensemble ML (RF/KNN):** Behavioral modeling for complex citizens.
- **Fuzzy Logic Morality:** A "gray area" reasoning layer that filters decisions through an ethical lens (Guilt, Trust, Pressure).

### 3. Social Influence & Narrative Warfare
Citizens aren't just isolated dots; they are social animals. Trust spreads through proximity and ideological alignment. **Media Agents** can actively manipulate these clusters using disinformation campaigns and algorithmic amplification.

### 4. Global Economics & Governance
The simulation features macro-economic loops:
- **Macro Loops:** Inflation, Unemployment, and Inequality create a feedback cycle with social happiness.
- **Guardian System:** The Supreme Leader taxes and evaluates state leaders, firing those who threaten national stability or public trust.
