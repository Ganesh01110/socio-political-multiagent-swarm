"""
Media ownership and influence service.
Determines who controls media and how it shapes public opinion.
"""
import random
from typing import Dict, List
from app.models.agents import MediaAgent, CitizenAgent, StateLeaderAgent, BaseAgent, AgentType

class MediaOwnership:
    INDUSTRIALIST = "INDUSTRIALIST"
    POLITICIAN_ALLY = "POLITICIAN_ALLY"
    COMMON_CITIZEN = "COMMON_CITIZEN"
    EXTERNAL_FACTOR = "EXTERNAL_FACTOR"
    INDEPENDENT = "INDEPENDENT"

class MediaService:
    def __init__(self):
        pass
    
    def determine_ownership(self, media: MediaAgent, all_agents: Dict[str, BaseAgent]) -> None:
        """
        Determines media ownership based on social connections.
        Priority: Politician > Industrialist > Common Citizen > External
        """
        if not media.social_links:
            media.ownership = MediaOwnership.INDEPENDENT
            media.owner_id = None
            return
        
        # Check connections
        for link_id in media.social_links:
            if link_id not in all_agents:
                continue
            
            agent = all_agents[link_id]
            
            # Politicians have highest priority
            if isinstance(agent, StateLeaderAgent):
                media.ownership = MediaOwnership.POLITICIAN_ALLY
                media.owner_id = link_id
                return
            
            # Industrialists (wealthy citizens)
            if isinstance(agent, CitizenAgent) and agent.faction == "Industrialist" and agent.wealth > 100:
                media.ownership = MediaOwnership.INDUSTRIALIST
                media.owner_id = link_id
                return
        
        # Check for common citizen ownership
        for link_id in media.social_links:
            if link_id in all_agents and isinstance(all_agents[link_id], CitizenAgent):
                media.ownership = MediaOwnership.COMMON_CITIZEN
                media.owner_id = link_id
                return
        
        # Default to independent
        media.ownership = MediaOwnership.INDEPENDENT
        media.owner_id = None
    
    def calculate_bias(self, media: MediaAgent, all_agents: Dict[str, BaseAgent], override: str = "auto") -> float:
        """
        Calculates media bias based on ownership OR global override.
        Returns: -1.0 (anti-establishment) to +1.0 (pro-establishment)
        """
        if override == "pro_state":
            return 0.9 + random.uniform(-0.05, 0.05)
        elif override == "anti_state":
            return -0.9 + random.uniform(-0.05, 0.05)
        elif override == "neutral":
            return random.uniform(-0.1, 0.1)
            
        # Default 'auto' logic
        if media.ownership == MediaOwnership.POLITICIAN_ALLY and media.owner_id:
            # Strongly pro-incumbent
            return 0.8 + random.uniform(-0.1, 0.1)
        
        elif media.ownership == MediaOwnership.INDUSTRIALIST and media.owner_id:
            owner = all_agents.get(media.owner_id)
            if owner and isinstance(owner, CitizenAgent):
                # Pro-business, varies with owner's happiness
                return 0.4 + (owner.happiness / 200.0)
        
        elif media.ownership == MediaOwnership.COMMON_CITIZEN:
            # Populist, anti-establishment if trust is low
            if media.owner_id and media.owner_id in all_agents:
                owner = all_agents[media.owner_id]
                if isinstance(owner, CitizenAgent):
                    return -0.3 - (owner.trust_score / 100.0) * 0.5
        
        elif media.ownership == MediaOwnership.EXTERNAL_FACTOR:
            # Unpredictable
            return random.uniform(-0.8, 0.8)
        
        # Independent media
        return random.uniform(-0.2, 0.2)

    def get_disinfo_headline(self, bias: float) -> str:
        """Returns a specific piece of 'fake news' based on the current bias."""
        pro_state_lies = [
            "Secret data proves Leader is a genius!",
            "Protesters actually found to be paid foreign actors.",
            "Economy 1000% stronger than reported, say 'experts'.",
            "Neighboring nations envy our glorious leadership.",
            "Leader saves elderly couple from burning building (unverified)."
        ]
        anti_state_lies = [
            "LEAKED: Leader has secret offshore gold stash.",
            "Studies find that current policies cause memory loss.",
            "Leader's 'Close Circle' seen fleeing with suitcases of cash.",
            "Is the Leader a lizard? Our investigative report inside.",
            "Citizens reporting 'ghost agents' stealing their crops."
        ]
        
        if bias > 0.3:
            return random.choice(pro_state_lies)
        elif bias < -0.3:
            return random.choice(anti_state_lies)
        return "Strange lights seen over the capital; citizens confused."

    
    def propagate_narrative(self, media: MediaAgent, citizens: List[CitizenAgent], bias: float) -> None:
        """
        Media influences citizen perceptions based on bias.
        Positive bias -> increases trust/fear
        Negative bias -> decreases trust, increases protest_intent
        """
        for citizen in citizens:
            # Distance-based influence
            distance = ((citizen.x - media.x)**2 + (citizen.y - media.y)**2)**0.5
            if distance > media.reach:
                continue
            
            influence_strength = (1.0 - distance / media.reach) * media.credibility
            
            if bias > 0:  # Pro-establishment
                citizen.trust_score += influence_strength * bias * 5
                citizen.fear += influence_strength * bias * 0.05
                citizen.protest_intent -= influence_strength * bias * 0.1
            else:  # Anti-establishment
                citizen.trust_score += influence_strength * bias * 5  # Negative bias reduces trust
                citizen.protest_intent += influence_strength * abs(bias) * 0.15
            
            # Apply disinformation
            if random.random() < media.disinformation_rate:
                citizen.trust_score += random.uniform(-10, 10)
            
            # Clamp values
            citizen.trust_score = max(0, min(100, citizen.trust_score))
            citizen.fear = max(0, min(1.0, citizen.fear))
            citizen.protest_intent = max(0, min(1.0, citizen.protest_intent))
