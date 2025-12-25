# System Analysis: Pros & Cons

## Advantages (Pros)

1. **Autonomous Learning:** Leaders adapt their strategies based on outcomes. Over time, they "learn" that excessive greed leads to disposal, creating a realistic survival-of-the-fittest governance model.
2. **Emergent Behavior:** Social influence propagation allows for the emergence of "pockets of rebellion" or "loyalty clusters" without being explicitly programmed.
3. **End-to-End Cycle:** The system closes the loop between individual wealth, social trust, and national budget, providing a holistic view of socio-economic health.
4. **Data-Driven:** Every tick is persisted, allowing for historical analysis of how policies affect the long-term trend of happiness and wealth.
5. **Real-time Visualization:** The PixiJS/Recharts integration provides immediate feedback on the simulation's state.

## Disadvantages (Cons)

1. **Simplified State Space:** The current RL implementation uses a discretized state space (LO/MD/HI). This lacks the nuance of continuous variables (e.g., trust at 49% vs 51%).
2. **Deterministic Voting:** The election logic is currently based on a simple majority of trust scores, which doesn't account for voter apathy or external shocks.
3. **Shared Brain:** Currently, all leaders share one "Brain" (Phase 3.1). While this speeds up learning, it prevents diverse "personalities" from emerging among leaders.
4. **Limited Resource Loop:** Wealth currently "vanishes" or "appears" through distributions. A more realistic closed-loop economy (where citizens pay taxes back) is not yet fully implemented.
