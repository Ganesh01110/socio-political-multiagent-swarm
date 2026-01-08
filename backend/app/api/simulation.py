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

@router.get("/policy")
async def get_policy():
    return simulation_instance.policy_settings

@router.post("/policy")
async def update_policy(settings: dict):
    simulation_instance.policy_settings.update(settings)
    return {"status": "policy_updated", "current": simulation_instance.policy_settings}

@router.get("/settings")
async def get_settings():
    return simulation_instance.simulation_settings

@router.post("/settings")
async def update_settings(settings: dict):
    simulation_instance.simulation_settings.update(settings)
    return {"status": "settings_updated", "current": simulation_instance.simulation_settings}

@router.get("/media")
async def get_media_info():
    media_agents = [a for a in simulation_instance.agents.values() if a.type == "media"]
    return [{
        "id": m.id,
        "ownership": m.ownership,
        "owner_id": m.owner_id,
        "bias": m.bias,
        "credibility": m.credibility
    } for m in media_agents]

@router.get("/history")

async def get_history(state_id: str = None, db: Session = Depends(get_db)):
    """
    Returns history, optionally filtered by state_id.
    """
    query = db.query(SimulationHistory)
    if state_id and state_id != "all":
        query = query.filter(SimulationHistory.state_id == state_id)
    elif state_id == None:
        # If no state_id provided, default to all history so frontend can filter
        # but we could also keep it as national if we want to be strict.
        # Given current frontend logic, returning all is better for performance.
        pass 

        
    history = query.order_by(SimulationHistory.tick).all()
    return history


@router.post("/history/clear")
async def clear_history(db: Session = Depends(get_db)):
    """
    Clears all simulation history.
    """
    db.query(SimulationHistory).delete()
    db.commit()
    # Reset tick counter in engine
    simulation_instance.scheduler.current_tick = 0
    return {"status": "history_cleared"}

