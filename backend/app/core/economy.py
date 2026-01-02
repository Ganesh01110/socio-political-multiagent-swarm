from typing import List, Dict, Tuple
from app.models.agents import StateLeaderAgent, CitizenAgent, SupremeLeaderAgent
from app.models.world import Nation, State
import numpy as np
import random

class EconomyService:
    def __init__(self):
        pass

    def distribute_national_budget(self, supreme_leader: SupremeLeaderAgent, nation: Nation, state_leaders: List[StateLeaderAgent]):
        total_budget = 1000.0
        supreme_leader.total_budget = total_budget
        
        per_state_budget = total_budget / len(state_leaders) if state_leaders else 0
        for leader in state_leaders:
            leader.budget_allocated = per_state_budget

    def process_state_economy(self, leader: StateLeaderAgent, citizens: List[CitizenAgent], inflation: float, unemployment: float) -> float:
        """
        Executes the economic consequences of the leader's action.
        Returns the step reward for the leader.
        """
        if not citizens:
            return 0.0

        action = leader.last_action
        
        # 1. Execute Action Effects
        initial_budget = leader.budget_allocated
        funds_for_people = initial_budget
        personal_gain = 0
        trust_change = 0
        happiness_modifier = 0
        
        if action == 1: # STEAL / BLACK ECONOMY
            personal_gain = initial_budget * 0.5
            funds_for_people = initial_budget * 0.4 # More goes to black economy
            trust_change -= 10
            happiness_modifier -= 2
        elif action == 0: # INVEST
            funds_for_people = initial_budget
            if leader.wealth > 10:
                funds_for_people += 10
                leader.wealth -= 10
            trust_change += 5
            happiness_modifier += 1
        elif action == 2: # MAINTAIN
            personal_gain = initial_budget * 0.1
            funds_for_people = initial_budget * 0.9
            trust_change += 0
        elif action == 3: # PROPAGANDA
            funds_for_people = initial_budget * 0.7
            trust_change += 15 # Short term trust boost
            happiness_modifier -= 1 # Long term structural damage
            
        # Economic Risk Taking (Hope)
        for citizen in citizens:
            if random.random() < citizen.hope:
                 citizen.wealth += random.uniform(0, 2) # Risk pays off
            else:
                 citizen.wealth -= random.uniform(0, 1) # Loss

        leader.wealth += personal_gain
        leader.corruption_level = personal_gain

        # 2. Distribute to Citizens with Inflation/Unemployment effects
        per_citizen = (funds_for_people / len(citizens)) * (1.0 - inflation)
        for citizen in citizens:
            citizen.wealth += per_citizen
            citizen.trust_score = max(0, min(100, citizen.trust_score + trust_change))
            
            # Unemployment impact
            if random.random() < unemployment:
                 citizen.wealth *= 0.8 # Loss of income
                 citizen.happiness -= 5
            
            fair_share = (initial_budget / len(citizens)) * 0.8
            if per_citizen < fair_share:
                citizen.happiness -= 2
            else:
                citizen.happiness += 1
                
            citizen.happiness = max(0, min(100, citizen.happiness + happiness_modifier))

        # 3. Calculate Reward (Strategic Layer)
        # Reward is a mix of personal wealth, trust, and state stability
        avg_happiness = sum(c.happiness for c in citizens) / len(citizens)
        step_reward = personal_gain + (trust_change * 2) + (avg_happiness / 10.0)
        
        return step_reward
