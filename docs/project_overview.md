# Sworm System: Project Overview

## Description
The Sworm System is a sophisticated socio-economic simulation designed to study the interplay between individual citizen behavior, local leadership strategies, and top-down national governance. 

By combining **Reinforcement Learning (RL)** with agent-based modeling, the system simulates a world where leaders must learn to survive re-election cycles while fulfilling their own greed or investing in their people.

## Key Components

### 1. The Sworm Economy
Money is the lifeblood of the simulation. It originates from the Supreme Leader and trickles down through State Leaders to the Citizens. Corruption (stealing) at the leader level directly impacts citizen happiness and trust.

### 2. Reinforcement Learning (Q-Learning)
State Leaders are powered by a Q-Learning brain. They observe their current state (Trust and Wealth) and choose actions:
- **Invest:** Boosts citizen wealth/trust at a personal cost.
- **Steal:** Increases personal wealth but tanks trust.
- **Maintain:** A balanced, low-risk approach.
- **Propaganda:** An expensive artificial boost to trust.

### 3. Social Influence
Citizens aren't just isolated dots; they are social animals. Trust spreads through proximity. A single dissenting neighbor can slowly influence an entire cluster of citizens, making social dynamics a critical factor for leader survival.

### 4. Enforcement & Governance
The Supreme Leader acts as a "Guardian of the System." By taxing leaders and firing those who are either too corrupt or hated by the populace, the Supreme Leader maintains national stability.
