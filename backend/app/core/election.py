import random
from typing import List, Dict, Tuple
from app.models.agents import BaseAgent, StateLeaderAgent, CitizenAgent, AgentType
import uuid

class ElectionService:
    def __init__(self):
        pass

    def conduct_state_election(self, state_id: str, current_leader: StateLeaderAgent, citizens: List[CitizenAgent]) -> Tuple[str, Dict]:
        """
        Conducts an election for a state.
        Returns: (Winner ID, Election Details)
        """
        if not citizens:
            return current_leader.id, {"reason": "no_citizens"}

        # 1. Calculate Challenger Score (Random for now, simulating an opponent)
        # Challenger has default trust of 50
        challenger_trust = 50.0 
        challenger_score = challenger_trust + random.uniform(-10, 10)

        # 2. Calculate Incumbent Score
        # Sum of citizen trust in the leader
        incumbent_votes = 0
        challenger_votes = 0

        for citizen in citizens:
            # Voting Logic:
            # Probability to vote for incumbent = SIGMOID(Trust - 50)
            # Simplified: If Trust > 50, mostly vote incumbent.
            
            # Noise factor
            perception = current_leader.trust_score + random.uniform(-5, 5)
            
            if perception >= challenger_score:
                incumbent_votes += 1
            else:
                challenger_votes += 1

        total_votes = incumbent_votes + challenger_votes
        
        details = {
            "incumbent_id": current_leader.id,
            "incumbent_votes": incumbent_votes,
            "challenger_votes": challenger_votes,
            "total_votes": total_votes,
            "state_id": state_id
        }

        if incumbent_votes >= challenger_votes:
            return current_leader.id, details
        else:
            return "challenger", details

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
