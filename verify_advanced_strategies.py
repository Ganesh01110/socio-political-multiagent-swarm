from app.core.engine import SimulationEngine
from app.models.agents import AgentType
from app.ml.brain_stack import RuleBasedPolicy, DQNPolicy, ANNPolicy
import time

def test_simulation():
    engine = SimulationEngine()
    print("Initial Metrics:", engine.get_state()["metrics"])
    
    # Run for 100 ticks
    for i in range(100):
        res = engine.advance()
        if i % 20 == 0:
            metrics = res["metrics"]
            print(f"Tick {res['tick']} | Happiness: {metrics['avg_happiness']:.2f} | Wealth: {metrics['avg_wealth']:.2f} | Inflation: {metrics['inflation']:.4f} | Inequality: {metrics['inequality']:.4f}")

    # Verify Brain Selection
    print("\nVerifying Brain Selection:")
    for agent_id, policy in list(engine.agent_policies.items()):
        agent = engine.agents.get(agent_id)
        if not agent:
            continue
        if agent.type == AgentType.SUPREME_LEADER:
            print(f"SL Brain: {type(policy).__name__}")
        elif agent.type == AgentType.LEADER:
             pass 
# Too many to print
             
    # Check if we have logs or news events for Narrative Warfare
    news = engine.last_election_results
    narrative_events = [n for n in news if n["outcome"] == "Narrative Warfare"]
    print(f"\nNarrative Warfare Events Detected: {len(narrative_events)}")
    for event in narrative_events[:2]:
        print(f" - {event['reason']} by {event['winner_name']}")

if __name__ == "__main__":
    test_simulation()
