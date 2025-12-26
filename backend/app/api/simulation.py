from fastapi import APIRouter
from app.core.engine import simulation_instance
from app.db.database import get_db
from app.db.models import SimulationHistory
from sqlalchemy.orm import Session
from fastapi import Depends

router = APIRouter()

@router.post("/start")
async def start_simulation():
    simulation_instance.start()
    return {"status": "started"}

@router.post("/stop")
async def stop_simulation():
    simulation_instance.stop()
    return {"status": "stopped"}

@router.post("/tick")
async def advance_tick():
    state = simulation_instance.advance()
    return state

@router.post("/election")
async def force_election():
    simulation_instance.run_elections()
    return {"status": "election_triggered", "results": simulation_instance.last_election_results}

@router.get("/state")
async def get_state():
    return simulation_instance.get_state()
@router.get("/brain")
async def get_brain():
    return simulation_instance.economy_service.brain.q_table

@router.get("/history")
async def get_history(db: Session = Depends(get_db)):
    """
    Returns the full history of metrics.
    """
    history = db.query(SimulationHistory).order_by(SimulationHistory.tick).all()
    return history
