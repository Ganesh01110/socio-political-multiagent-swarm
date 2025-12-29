import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'
import NationMap from './components/NationMap'
import SimulationDashboard from './components/SimulationDashboard'
import HistoryCharts from './components/HistoryCharts'

// ... interfaces ...
interface HistoryData {
  tick: number;
  avg_happiness: number;
  avg_wealth: number;
  avg_trust: number;
  sl_budget: number;
}

// Add missing interfaces
interface Agent {
  id: string;
  type: string;
  x: number;
  y: number;
  wealth: number;
  trust_score: number;
  recent_feedback?: string;
  state_id?: string;
  faction?: string;
  age?: number;
}

interface SimulationState {
  tick: number;
  nation: {
    name: string;
    states: any[];
  };
  agents: Agent[];
  last_election_results: any[];
  metrics: any;
}

function App() {
  const [simState, setSimState] = useState<SimulationState | null>(null)
  const [history, setHistory] = useState<HistoryData[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchState = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/simulation/state')
      setSimState(response.data)

      // Also fetch history
      const historyRes = await axios.get('http://localhost:8000/api/simulation/history')
      setHistory(historyRes.data)

      setError(null)
    } catch (err) {
      setError('Failed to connect to backend. Is it running?')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchState()
    const interval = setInterval(fetchState, 1000) // Poll every second
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="container">
      <h1>Sworm System</h1>

      {error && <div className="error">{error}</div>}

      {loading && !simState && <div>Loading Simulation...</div>}

      {simState && (
        <div className="dashboard-container">
          <div className="stats-container">
            <h2>Tick: {simState.tick}</h2>
            <h3>Nation: {simState.nation.name}</h3>
            {simState.metrics && <SimulationDashboard metrics={simState.metrics} />}
          </div>

          <div className="controls">
            <button onClick={async () => {
              const res = await axios.post('http://localhost:8000/api/simulation/tick');
              setSimState(res.data);
            }}>
              Manual Tick
            </button>
          </div>

          <div className="simulation-view">
            <NationMap agents={simState.agents} />
            <div className="legend">
              <span className="legend-item"><span className="dot" style={{ backgroundColor: '#0D47A1' }}></span> Industrialist</span>
              <span className="legend-item"><span className="dot" style={{ backgroundColor: '#8BC34A' }}></span> Environmentalist</span>
              <span className="legend-item"><span className="dot" style={{ backgroundColor: '#9C27B0' }}></span> Technocrat</span>
              <span className="legend-item"><span className="dot" style={{ backgroundColor: '#2196F3' }}></span> Neutral</span>
              <span className="legend-item"><span className="dot" style={{ backgroundColor: '#4CAF50' }}></span> Leader</span>
              <span className="legend-item"><span className="dot" style={{ backgroundColor: '#FFFF00' }}></span> Supreme Leader</span>
            </div>
          </div>

          <HistoryCharts history={history} />

          <div className="news-feed">
            <h3>News Feed</h3>
            {simState.last_election_results && simState.last_election_results.length > 0 ? (
              <ul>
                {simState.last_election_results.map((res: any, idx: number) => {
                  const isSocial = res.outcome === "Social Feedback";
                  return (
                    <li key={idx} className={res.winner_name === "New Leader" ? "news-alert" : isSocial ? "social-news" : ""}>
                      <span className="news-tag">{res.state_id?.slice(0, 10)}:</span>
                      {isSocial ? (
                        <span className="news-msg">"{res.reason}" — <em>{res.winner_name}</em></span>
                      ) : (
                        <span className="news-msg">{res.outcome} ({res.incumbent_votes} vs {res.challenger_votes})</span>
                      )}
                    </li>
                  );
                })}
              </ul>
            ) : <p>No recent news.</p>}
          </div>

          <div className="state-list">
            {simState.nation.states.map(state => (
              <div key={state.id} className="state-card">
                <h4>{state.name}</h4>
                <p>Population: {state.population}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default App
