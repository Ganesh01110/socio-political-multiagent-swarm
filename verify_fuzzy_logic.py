from app.core.engine import SimulationEngine
from app.models.agents import AgentType
from app.ml.brain_stack import HybridPolicy
import numpy as np

def test_fuzzy_morality():
    engine = SimulationEngine()
    print("Testing Fuzzy Morality Integration...")
    
    # Run for 50 ticks and observe moral resonance
    for i in range(50):
        res = engine.advance()
        if i % 10 == 0:
            metrics = res["metrics"]
            # Sample an agent's moral resistance
            sample_agent = list(engine.agents.values())[10]
            print(f"Tick {res['tick']} | Infl: {metrics['inflation']:.3f} | Avg Morality: {np.mean([a.moral_resistance for a in engine.agents.values()]):.3f} | Sample Agent Morality: {sample_agent.moral_resistance:.3f}")

    # Specific check for HybridPolicy behavior
    print("\nChecking HybridPolicy decision modification...")
    for agent_id, policy in engine.agent_policies.items():
        if isinstance(policy, HybridPolicy):
            # Test a mock state that would typically trigger 'Steal' (Action 1)
            # state: [trust, wealth, happiness, budget, inflation, unemployment, inequality]
            mock_untrustworthy_state = np.array([0.1, 0.1, 0.1, 100.0, 0.2, 0.2, 0.8])
            
            # We want to see if it SOMETIMES returns 0 (Maintain) despite the strategic layer
            # But since policies are random/untrained, we just check if it runs without error
            action = policy.decide(mock_untrustworthy_state)
            print(f"Agent {agent_id[:4]} decided Action {action} for untrustworthy state. Resistance was: {policy.morality_evaluator.calculate_moral_resistance(0.8, 10, 0.5):.3f}")
            break

if __name__ == "__main__":
    test_fuzzy_morality()
