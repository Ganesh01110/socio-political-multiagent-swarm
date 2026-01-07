"""
Basic API tests for the Sworm System backend.
Run with: pytest
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test that the root endpoint returns a welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Sworm System" in response.json()["message"]


def test_get_simulation_state():
    """Test getting the current simulation state."""
    response = client.get("/api/simulation/state")
    assert response.status_code == 200
    data = response.json()
    assert "tick" in data
    assert "nation" in data
    assert "agents" in data


def test_simulation_tick():
    """Test advancing the simulation by one tick."""
    # Get initial state
    initial_response = client.get("/api/simulation/state")
    initial_tick = initial_response.json()["tick"]
    
    # Advance one tick
    tick_response = client.post("/api/simulation/tick")
    assert tick_response.status_code == 200
    
    # Verify tick increased
    new_tick = tick_response.json()["tick"]
    assert new_tick == initial_tick + 1


def test_get_policy_settings():
    """Test getting policy settings."""
    response = client.get("/api/simulation/policy")
    assert response.status_code == 200
    data = response.json()
    assert "consider_trust" in data
    assert "consider_fear" in data
    assert "consider_happiness" in data
    assert "consider_wealth" in data


def test_update_policy_settings():
    """Test updating policy settings."""
    new_settings = {
        "consider_trust": False,
        "consider_fear": True
    }
    response = client.post("/api/simulation/policy", json=new_settings)
    assert response.status_code == 200
    assert response.json()["status"] == "policy_updated"


def test_get_simulation_settings():
    """Test getting simulation settings."""
    response = client.get("/api/simulation/settings")
    assert response.status_code == 200
    data = response.json()
    assert "enable_hope_mechanic" in data
    assert "enable_trust_decay" in data
    assert "enable_memory_loss" in data


def test_get_media_info():
    """Test getting media ownership information."""
    response = client.get("/api/simulation/media")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Should have media agents
    if len(data) > 0:
        media = data[0]
        assert "ownership" in media
        assert "bias" in media
        assert "credibility" in media


def test_get_history():
    """Test getting simulation history."""
    response = client.get("/api/simulation/history")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_history_by_state():
    """Test getting history filtered by state_id."""
    response = client.get("/api/simulation/history?state_id=state_0")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_clear_history():
    """Test clearing simulation history."""
    response = client.post("/api/simulation/history/clear")
    assert response.status_code == 200
    assert response.json()["status"] == "history_cleared"
    
    # Verify history is empty
    history_response = client.get("/api/simulation/history")
    assert len(history_response.json()) == 0
