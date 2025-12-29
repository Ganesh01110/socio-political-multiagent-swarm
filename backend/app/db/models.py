from sqlalchemy import Column, Integer, Float
from .database import Base

class SimulationHistory(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    tick = Column(Integer, index=True)
    avg_happiness = Column(Float)
    avg_wealth = Column(Float)
    avg_trust = Column(Float)
    sl_budget = Column(Float)
