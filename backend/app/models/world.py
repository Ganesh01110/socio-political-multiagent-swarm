from pydantic import BaseModel
from typing import List, Dict, Optional

class State(BaseModel):
    id: str
    name: str
    population: int
    leader_id: Optional[str] = None
    economy_index: int = 100
    trust_index: int = 100
    budget: float = 0.0

class Nation(BaseModel):
    id: str
    name: str
    states: List[State]
    supreme_leader_id: Optional[str] = None
    total_budget: float = 0.0
