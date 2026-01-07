from typing import List, Dict
import math
import numpy as np
from app.models.agents import CitizenAgent, AgentType

class InfluenceService:
    def __init__(self):
        pass

    def propagate_influence(self, all_agents: Dict[str, any]):
        """
        Agents influence their social circle.
        Implements Threshold Influence: 
        If > 50% of the circle has low trust, others are likely to follow.
        """
        agent_list = list(all_agents.values())
        citizens = [a for a in agent_list if a.type == AgentType.CITIZEN]
        base_learning_rate = 0.2

        for agent in citizens:
            if not agent.social_links: continue
            
            # Get data from peers
            peers = [all_agents[link_id] for link_id in agent.social_links if link_id in all_agents]
            if not peers: continue

            # 1. Threshold Check (Social Tipping Point)
            # Count peers with trust < 30
            disaffected_peers = [p for p in peers if p.trust_score < 30]
            disaffection_ratio = len(disaffected_peers) / len(peers)

            if disaffection_ratio > 0.5:
                # Rapid contagion of distrust
                agent.trust_score = max(0, agent.trust_score - 5.0)
                agent.protest_intent = min(1.0, agent.protest_intent + 0.1)
            else:
                # Normal gradual influence
                avg_peer_trust = sum(p.trust_score for p in peers) / len(peers)
                trust_diff = avg_peer_trust - agent.trust_score
                agent.trust_score = max(0, min(100, agent.trust_score + trust_diff * base_learning_rate))
                agent.protest_intent = max(0, agent.protest_intent - 0.05)

            # 2. Ideological Conversion (Groupthink)
            avg_peer_ideology = np.mean([p.ideology for p in peers], axis=0)
            agent.ideology = [
                max(-1.0, min(1.0, i + (pi - i) * 0.05))
                for i, pi in zip(agent.ideology, avg_peer_ideology)
            ]

            # 3. Fear/Pressure Effect from Media (Proximity to Media Agents)
            # This is already handled in engine._process_media_narratives, 
            # but we could link it here too if needed.

        # Memory Decay
        for agent in citizens:
            agent.trust_score *= (1.0 - agent.memory_decay * 0.01)

