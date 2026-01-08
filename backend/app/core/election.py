import random
from typing import List, Dict, Tuple
from app.models.agents import BaseAgent, StateLeaderAgent, CitizenAgent, AgentType
import uuid

class ElectionService:
    def __init__(self):
        pass

    def conduct_state_election(self, state_id: str, current_leader: StateLeaderAgent, agents: Dict[str, BaseAgent]) -> Tuple[str, Dict]:
        """
        Conducts an election. Social pressure and cronyism now play major roles.
        """
        citizens = [a for a in agents.values() if isinstance(a, CitizenAgent) and a.state_id == state_id]
        if not citizens:
            return current_leader.id, {"winner": "incumbent", "votes": 0}

        # Calculate average state wealth for cronyism check
        avg_wealth = sum(c.wealth for c in citizens) / len(citizens)
        
        counts = {"incumbent": 0, "challenger": 0}

        for citizen in citizens:
            # 1. Cronyism Logic (Favoritism)
            is_crony = citizen.id in current_leader.social_links
            favored = citizen.wealth > (avg_wealth * 1.2) # 20% richer than average
            
            # Check for "Principles Over Profit" (Drastic Ideological difference)
            ideology_diff = abs(citizen.ideology - current_leader.ideology)
            principled_dissent = ideology_diff > 0.7

            vote = "challenger"
            if is_crony and favored and not principled_dissent:
                # Highly likely to vote incumbent due to personal benefit
                if random.random() < 0.95:
                    vote = "incumbent"
            else:
                # 2. Regular Voting Logic (Trust, Fear, Social Pressure)
                # Influence of social circle (Peer Pressure)
                peers = [agents[pid] for pid in citizen.social_links if pid in agents]
                peer_trust_avg = sum(p.trust_score for p in peers) / len(peers) if peers else citizen.trust_score
                
                # Effective trust is a blend of personal experience and peer pressure
                effective_trust = (citizen.trust_score * 0.6) + (peer_trust_avg * 0.4)
                
                # Fear impact: High fear increases incumbent vote (compliance)
                fear_bias = citizen.fear * 30 
                
                incumbent_score = effective_trust + fear_bias
                
                # Phase 16: Unemployment Impact
                if agents.get("sim_settings", {}).get("enable_unemployment_election_impact", False):
                    # state_unemployment can be found on state object if passed, let's assume it's available or look it up
                    # For now, subtract a baseline if we find it
                    state_unemployment = getattr(citizen, 'state_unemployment', 0.05) # Assume injected
                    incumbent_score -= (state_unemployment * 400) # 10% unemployment = -40 points
                
                challenger_score = random.uniform(30, 80)
                
                if incumbent_score > challenger_score:
                    vote = "incumbent"

            
            counts[vote] += 1

        winner = "incumbent" if counts["incumbent"] >= counts["challenger"] else "challenger"
        
        return (current_leader.id if winner == "incumbent" else f"new_leader_{state_id}"), {
            "winner": winner,
            "counts": counts,
            "total": len(citizens)
        }

    def check_for_coup(self, state_id: str, current_leader: StateLeaderAgent, citizens: List[CitizenAgent]) -> bool:
        """
        Checks if conditions are met for a coup.
        Triggers if Avg Trust < 20 AND Avg Protest Intent > 0.7
        """
        if not citizens: return False
        
        avg_trust = sum(c.trust_score for c in citizens) / len(citizens)
        avg_protest = sum(c.protest_intent for c in citizens) / len(citizens)
        
        # Coup threshold
        if avg_trust < 20.0 and avg_protest > 0.7:
            # Random chance to succeed
            return random.random() < 0.3
        
        return False


    def create_new_leader(self, state_id: str) -> StateLeaderAgent:
        """Generates a new random leader agent to replace the loser."""
        return StateLeaderAgent(
            id=str(uuid.uuid4()),
            state_id=state_id,
            type=AgentType.LEADER,
            honesty=random.random(),
            greed=random.random(),
            competence=random.random(),
            trust_score=50.0, # Fresh start
            x=random.random() * 800,
            y=random.random() * 600
        )
