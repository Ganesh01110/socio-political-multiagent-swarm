from typing import List, Dict
import math
import numpy as np
from app.models.agents import CitizenAgent, AgentType

class InfluenceService:
    def __init__(self):
        pass

    def propagate_influence(self, all_agents: List[CitizenAgent]):
        """
        Citizens influence their neighbors' Trust Scores and Ideology.
        Includes:
        - Education clusters (higher education = less prone to disinformation)
        - Ideological similarity (Echo chambers)
        """
        citizens = [a for a in all_agents if a.type == AgentType.CITIZEN]
        influence_radius = 60.0 
        base_learning_rate = 0.1

        for i, agent_a in enumerate(citizens):
            for j, agent_b in enumerate(citizens):
                if i == j: continue
                
                dist = math.sqrt((agent_a.x - agent_b.x)**2 + (agent_a.y - agent_b.y)**2)
                
                if dist < influence_radius:
                    # Ideological Similarity (Cosine Similarity approx)
                    ideology_a = np.array(agent_a.ideology)
                    ideology_b = np.array(agent_b.ideology)
                    sim = np.dot(ideology_a, ideology_b) / (np.linalg.norm(ideology_a)*np.linalg.norm(ideology_b) + 0.001)
                    
                    # Echo Chamber Effect: Higher influence if ideologies are similar
                    # If similarity is low, they might even diverge (polarization)
                    influence_weight = base_learning_rate * (sim if sim > 0 else 0.5)
                    
                    # Education Effect: Higher education agents are harder to influence but more influential
                    edu_factor = agent_a.education / (agent_b.education + 0.1)
                    total_lp = influence_weight * edu_factor
                    
                    # Influence Trust
                    diff_trust = agent_a.trust_score - agent_b.trust_score
                    agent_b.trust_score = max(0, min(100, agent_b.trust_score + diff_trust * total_lp))
                    
                    # Influence Ideology (Converge toward peer)
                    if sim > 0:
                        agent_b.ideology = [
                            max(-1.0, min(1.0, b + (a - b) * total_lp * 0.5))
                            for a, b in zip(agent_a.ideology, agent_b.ideology)
                        ]
                    
                    # Confirmation Bias (Memory Decay)
                    # Past influences decay unless reinforced
                    agent_b.trust_score *= (1.0 - agent_b.memory_decay * 0.1)
