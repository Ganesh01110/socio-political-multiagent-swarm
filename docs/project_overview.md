# Sworm System: Project Overview

## Description
The Sworm System is a sophisticated socio-economic simulation designed to study the interplay between individual citizen behavior, local leadership strategies, and top-down national governance. 

By combining **Reinforcement Learning (RL)** with agent-based modeling, the system simulates a world where leaders must learn to survive re-election cycles while fulfilling their own greed or investing in their people.

## Key Components

### 1. The Sworm Economy
Money is the lifeblood of the simulation. It originates from the Supreme Leader and trickles down through State Leaders to the Citizens. 
- **Corruption (Stealing):** Leaders can siphone budget for personal gain, governed by a dynamic **Corruption Efficiency** setting.
- **Inheritance Tax:** During generational turnover, a portion of an agent's wealth is reclaimed by the state (adjustable 1-60%).


### 2. Multi-Layered AI Brain Stack
Agents are no longer limited to simple Q-Learning. The system uses a **Strategy Pattern** for hierarchical intelligence:
- **DQN / Reinforcement Learning:** Strategic planning for leaders.
- **Ensemble ML (RF/KNN):** Behavioral modeling for complex citizens.
- **Fuzzy Logic Morality:** A "gray area" reasoning layer that filters decisions through an ethical lens (Guilt, Trust, Pressure).

### 3. Social Influence & Narrative Warfare
Citizens aren't just isolated dots; they are social animals. 
- **Dynamic Social Graphs:** Connections evolve as links decay (losing touch) and new links form (cronyism). Wealthy citizens actively seek connections to leaders.
- **Visual Networking:** Real-time rendering of social bonds color-coded by state.
- **Narrative Warfare & Media Mastery:** Media Agents manipulate clusters using disinformation. Users can force media into **Neutral**, **State Ally**, or **Anti-State** stances, with specific disinformation headlines (e.g., "Secret wealth stashes") appearing in the news feed.
- **Regime Stability (Coups):** Beyond elections, extreme inequality and low trust can trigger a **Coup d'état**, forcibly removing leaders.


### 4. Global Economics & Governance
The simulation features macro-economic loops:
- **Macro Loops:** Inflation, Unemployment, and Inequality create a feedback cycle. High unemployment now directly penalizes incumbents during election cycles if the **Unemployment Multiplier** is active.
- **Demographic Turnover:** Agents have finite lifespans and produce **1 to 3 offspring**, creating natural population shifts.
- **Guardian System:** The Supreme Leader taxes and evaluates state leaders, firing those who threaten national stability or public trust.

