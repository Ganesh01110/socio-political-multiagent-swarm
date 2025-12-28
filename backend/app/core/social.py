from typing import List, Dict
import math
from app.models.agents import CitizenAgent

class InfluenceService:
    def __init__(self):
        pass

    def propagate_influence(self, citizens: List[CitizenAgent]):
        """
        Simulates social interaction.
        Citizens influence their neighbors' Trust Scores.
        Simple logic: Compare locations, if close -> average trust.
        """
        # Optimization: In a real large scale, use K-D Tree or Grid.
        # For N=30, O(N^2) is fine.
        
        influence_radius = 50.0 # Pixel distance
        learning_rate = 0.1 # How much they influence each other

        for i, agent_a in enumerate(citizens):
            for j, agent_b in enumerate(citizens):
                if i == j: 
                    continue
                
                # Calculate Distance
                dist = math.sqrt((agent_a.x - agent_b.x)**2 + (agent_a.y - agent_b.y)**2)
                
                if dist < influence_radius:
                    # Interact!
                    # Agent A influences Agent B slightly
                    diff = agent_a.trust_score - agent_b.trust_score
                    
                    # If Agent A is more "vocal" (e.g. extremest), they might influence more.
                    # For now, simple averaging.
                    change = diff * learning_rate
                    
                    agent_b.trust_score += change
                    
                    # Clamp
                    agent_b.trust_score = max(0, min(100, agent_b.trust_score))
