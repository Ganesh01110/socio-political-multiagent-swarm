from pydantic import BaseModel, Field
from typing import List, Optional, Any
from enum import Enum
import uuid

class AgentType(str, Enum):
    CITIZEN = "citizen"
    LEADER = "leader"
    SUPREME_LEADER = "supreme_leader"
    MEDIA = "media"
    EXTERNAL = "external"

class BaseAgent(BaseModel):
    id: str
    type: AgentType
    honesty: float
    greed: float
    competence: float
    trust_score: float = 50.0
    x: float = 0.0
    y: float = 0.0
    
    class Config:
        use_enum_values = True

class CitizenAgent(BaseAgent):
    type: AgentType = AgentType.CITIZEN
    wealth: float = 10.0
    happiness: float = 50.0
    state_id: str
    faction: str = "Neutral" # Industrialist, Environmentalist, Technocrat
    faction_loyalty: float = 50.0
    age: int = 0
    lifespan: int = 100 # ticks

class StateLeaderAgent(BaseAgent):
    type: AgentType = AgentType.LEADER
    state_id: str
    budget_allocated: float = 0.0
    corruption_level: float = 0.0
    wealth: float = 0.0 # Personal Wealth
    # RL Fields
    last_state: str = ""
    last_action: int = -1
    last_dqn_state: Optional[Any] = Field(default=None, exclude=True)
    performance_score: float = 50.0
    recent_feedback: str = ""

class SupremeLeaderAgent(BaseAgent):
    type: AgentType = AgentType.SUPREME_LEADER
    total_budget: float = 0.0
    tenure_remaining: int

class MediaAgent(BaseAgent):
    type: AgentType = AgentType.MEDIA
    credibility: float = 0.5
    bias: float = 0.0 # Negative is anti-establishment, Positive is pro-establishment
    reach: float = 150.0

class ExternalFactorAgent(BaseAgent):
    type: AgentType = AgentType.EXTERNAL
    active_event: Optional[str] = None
    event_severity: float = 0.0
