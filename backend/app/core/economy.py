from typing import List, Dict
from app.models.agents import StateLeaderAgent, CitizenAgent, SupremeLeaderAgent
from app.models.world import Nation, State
from app.ml.dqn import DQNAgent
import numpy as np

class EconomyService:
    def __init__(self):
        self.brains: Dict[str, DQNAgent] = {}
        # DQN Specs:
        # State: [trust_score, wealth, happiness, budget_allocated] (4 floats)
        # Actions: 0=Invest, 1=Steal, 2=Maintain, 3=Propaganda (4 actions)
        self.state_size = 4
        self.action_size = 4

    def get_brain(self, leader_id: str) -> DQNAgent:
        if leader_id not in self.brains:
            self.brains[leader_id] = DQNAgent(self.state_size, self.action_size)
        return self.brains[leader_id]

    def distribute_national_budget(self, supreme_leader: SupremeLeaderAgent, nation: Nation, state_leaders: List[StateLeaderAgent]):
        total_budget = 1000.0
        supreme_leader.total_budget = total_budget
        
        per_state_budget = total_budget / len(state_leaders) if state_leaders else 0
        for leader in state_leaders:
            leader.budget_allocated = per_state_budget

    def _get_continuous_state(self, leader: StateLeaderAgent, citizens: List[CitizenAgent]):
        """Returns a normalized vector: [trust, wealth, happiness, budget]."""
        avg_happiness = sum(c.happiness for c in citizens) / len(citizens) if citizens else 50.0
        # Normalize to approx 0-1 range
        return np.array([
            leader.trust_score / 100.0,
            min(1.0, leader.wealth / 200.0),
            avg_happiness / 100.0,
            min(1.0, leader.budget_allocated / 500.0)
        ]).astype(np.float32)

    def process_state_economy(self, leader: StateLeaderAgent, citizens: List[CitizenAgent]):
        if not citizens:
            return

        brain = self.get_brain(leader.id)
        current_state = self._get_continuous_state(leader, citizens)
        
        # 1. Choose Action
        action = brain.choose_action(current_state)
        
        # 2. Execute Action
        initial_budget = leader.budget_allocated
        funds_for_people = initial_budget
        personal_gain = 0
        trust_change = 0
        
        if action == 1: # STEAL
            personal_gain = initial_budget * 0.5
            funds_for_people = initial_budget * 0.5
            trust_change -= 5
        elif action == 0: # INVEST
            funds_for_people = initial_budget
            if leader.wealth > 10:
                funds_for_people += 10
                leader.wealth -= 10
            trust_change += 5
        elif action == 2: # MAINTAIN
            personal_gain = initial_budget * 0.1
            funds_for_people = initial_budget * 0.9
            trust_change += 0
        elif action == 3: # PROPAGANDA
            funds_for_people = initial_budget * 0.8
            trust_change += 10

        leader.wealth += personal_gain
        leader.corruption_level = personal_gain

        # 3. Calculate Reward & Learn
        step_reward = personal_gain + (trust_change * 2) + 1
        
        if hasattr(leader, 'last_dqn_state') and leader.last_dqn_state is not None:
             brain.remember(leader.last_dqn_state, leader.last_action, step_reward, current_state, False)
             brain.learn()

        leader.last_dqn_state = current_state
        leader.last_action = action

        # 4. Distribute to Citizens
        per_citizen = funds_for_people / len(citizens)
        for citizen in citizens:
            citizen.wealth += per_citizen
            citizen.trust_score = max(0, min(100, citizen.trust_score + trust_change))
            
            fair_share = initial_budget / len(citizens)
            if per_citizen < fair_share * 0.8:
                citizen.happiness -= 1
            else:
                citizen.happiness += 1
