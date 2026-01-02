from typing import List, Dict
import random
from app.models.agents import SupremeLeaderAgent, StateLeaderAgent, CitizenAgent
from app.core.election import ElectionService

class SupremeLeaderService:
    def __init__(self, election_service: ElectionService):
        self.election_service = election_service

    def collect_taxes(self, supreme_leader: SupremeLeaderAgent, state_leaders: List[StateLeaderAgent]):
        """
        Reclaims unused budget from State Leaders.
        For now, a simple 'Flat Tax' on remaining wealth? 
        Or just reclaiming budget allocation for next round?
        Let's say SL collects 10% of every Leader's personal wealth as 'Tribute'.
        """
        total_collected = 0.0
        for leader in state_leaders:
            tax = leader.wealth * 0.10
            leader.wealth -= tax
            total_collected += tax
        
        # Add to SL budget (symbolic for now, or used for next round distribution)
        supreme_leader.total_budget += total_collected

    def evaluate_leaders(self, nation_state_dict: Dict, agents: Dict, current_tick: int):
        """
        Checks if any leader is too corrupt or incompetent.
        If so, FIRES them (replaces with new leader).
        """
        state_ids = list(nation_state_dict.keys())
        fired_events = []

        for state_id in state_ids:
            leader_id = nation_state_dict[state_id].leader_id
            leader = agents.get(leader_id)
            if not leader: continue
                
            # Evaluation Metrics (Long horizon reward)
            # SL fires if:
            # 1. Trust < 20 (Public outcry)
            # 2. Corruption > 75 (SL feels threatened or greedy)
            # 3. Performance score < 30
            
            reasons = []
            if leader.trust_score < 20.0:
                reasons.append("Low Trust")
            if leader.corruption_level > 75.0:
                reasons.append("Extreme Corruption")
            if leader.performance_score < 30.0:
                reasons.append("Poor Performance")

            if reasons:
                # YOU ARE FIRED!
                new_leader = self.election_service.create_new_leader(state_id)
                del agents[leader_id]
                agents[new_leader.id] = new_leader
                nation_state_dict[state_id].leader_id = new_leader.id
                
                fired_events.append({
                    "tick": current_tick,
                    "type": "fired",
                    "old_leader": leader_id,
                    "new_leader_id": new_leader.id,
                    "reason": ", ".join(reasons)
                })
                
        return fired_events
