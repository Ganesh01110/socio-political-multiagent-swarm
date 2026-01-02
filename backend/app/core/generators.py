import random
import numpy as np
from typing import List, Dict, Any
from app.models.agents import CitizenAgent, StateLeaderAgent, MediaAgent, AgentType
import uuid

class ScenarioGenerator:
    @staticmethod
    def generate_distribution(count: int, dist_type: str = "normal") -> List[float]:
        if dist_type == "normal":
            return np.clip(np.random.normal(0.5, 0.2, count), 0, 1).tolist()
        elif dist_type == "skewed_low":
            return np.clip(np.random.beta(2, 5, count), 0, 1).tolist()
        elif dist_type == "skewed_high":
            return np.clip(np.random.beta(5, 2, count), 0, 1).tolist()
        return [random.random() for _ in range(count)]

    @staticmethod
    def create_scenario(name: str):
        """Predefined scenarios for initialization."""
        scenarios = {
            "economic_crisis": {
                "avg_wealth": 5.0,
                "unemployment": 0.2,
                "inflation": 0.1,
                "avg_trust": 20.0
            },
            "technological_utopia": {
                "avg_wealth": 50.0,
                "unemployment": 0.02,
                "inflation": 0.01,
                "avg_trust": 80.0
            },
            "polarization": {
                "ideology_variance": 0.8,
                "media_bias_variance": 0.9
            }
        }
        return scenarios.get(name, {})

def initialize_agents_with_dist(state_id: str, count: int) -> List[CitizenAgent]:
    """Creates a synthetic distribution of citizens."""
    education_dist = ScenarioGenerator.generate_distribution(count, "normal")
    ideology_eco = ScenarioGenerator.generate_distribution(count, "normal")
    ideology_soc = ScenarioGenerator.generate_distribution(count, "normal")
    
    citizens = []
    for i in range(count):
        citizens.append(CitizenAgent(
            id=str(uuid.uuid4()),
            state_id=state_id,
            education=education_dist[i],
            ideology=[ideology_eco[i] * 2 - 1, ideology_soc[i] * 2 - 1], # Scale to -1 to 1
            honesty=random.random(),
            greed=random.random(),
            competence=random.random(),
            happiness=random.uniform(40, 60),
            wealth=random.uniform(5, 15),
            x=random.random() * 800,
            y=random.random() * 600
        ))
    return citizens

def initialize_media_with_dist(count: int) -> List[MediaAgent]:
    media_list = []
    for i in range(count):
        media_list.append(MediaAgent(
            id=str(uuid.uuid4()),
            ownership="Corporate" if random.random() < 0.7 else "State",
            disinformation_rate=random.uniform(0.01, 0.2),
            algorithmic_amplification=random.uniform(1.0, 2.5),
            credibility=random.uniform(0.4, 0.8),
            bias=random.uniform(-0.6, 0.6),
            honesty=random.random(),
            greed=random.random(),
            competence=random.random(),
            x=random.random() * 800,
            y=random.random() * 600
        ))
    return media_list
