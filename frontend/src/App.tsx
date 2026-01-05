import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'
import NationMap from './components/NationMap'
import SimulationDashboard from './components/SimulationDashboard'
import HistoryCharts from './components/HistoryCharts'

// ... interfaces ...
interface HistoryData {
  tick: number;
  state_id?: string | null;
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
  const [policy, setPolicy] = useState<Record<string, boolean>>({
    consider_trust: true,
    consider_fear: true,
    consider_happiness: true,
    consider_wealth: true
  })
  const [settings, setSettings] = useState<Record<string, boolean>>({
    enable_hope_mechanic: true,
    enable_trust_decay: true,
    enable_happiness_influence: true,
    enable_memory_loss: true,
    enable_ideology_shift: true
  })
  const [mediaInfo, setMediaInfo] = useState<any[]>([])



  const fetchState = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/simulation/state')
      setSimState(response.data)

      // Also fetch history
      const historyRes = await axios.get('http://localhost:8000/api/simulation/history')
      setHistory(historyRes.data)


      // Fetch Policy
      const policyRes = await axios.get('http://localhost:8000/api/simulation/policy')
      setPolicy(policyRes.data)

      // Fetch Settings
      const settingsRes = await axios.get('http://localhost:8000/api/simulation/settings')
      setSettings(settingsRes.data)

      // Fetch Media Info
      const mediaRes = await axios.get('http://localhost:8000/api/simulation/media')
      setMediaInfo(mediaRes.data)

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
            <button
              className="clear-btn"
              onClick={async () => {
                if (window.confirm("Are you sure you want to clear all simulation history?")) {
                  await axios.post('http://localhost:8000/api/simulation/history/clear');
                  setHistory([]);
                  fetchState();
                }
              }}
              style={{ backgroundColor: '#c62828', marginLeft: '10px' }}
            >
              Clear History
            </button>
          </div>

          <div className="policy-controls" style={{ margin: '20px 0', padding: '15px', background: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}>
            <h3>Political Considerations (Emotion Toggles)</h3>
            <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
              {Object.entries(policy).map(([key, value]) => (
                <label key={key} style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                  <input
                    type="checkbox"
                    checked={value}
                    onChange={async () => {
                      const newPolicy = { ...policy, [key]: !value };
                      setPolicy(newPolicy);
                      await axios.post('http://localhost:8000/api/simulation/policy', newPolicy);
                    }}
                    style={{ marginRight: '8px' }}
                  />
                  {key.replace('consider_', '').charAt(0).toUpperCase() + key.replace('consider_', '').slice(1)}
                </label>
              ))}
            </div>
            <p style={{ fontSize: '0.9em', color: '#aaa', marginTop: '10px' }}>
              Turning these off makes leaders ignore these factors in their reward logic.
            </p>
          </div>

          <div className="citizen-mechanics" style={{ margin: '20px 0', padding: '15px', background: 'rgba(100,200,255,0.05)', borderRadius: '8px' }}>
            <h3>Citizen Mechanics (Simulation Settings)</h3>
            <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
              {Object.entries(settings).map(([key, value]) => (
                <label key={key} style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                  <input
                    type="checkbox"
                    checked={value}
                    onChange={async () => {
                      const newSettings = { ...settings, [key]: !value };
                      setSettings(newSettings);
                      await axios.post('http://localhost:8000/api/simulation/settings', newSettings);
                    }}
                    style={{ marginRight: '8px' }}
                  />
                  {key.replace('enable_', '').split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
                </label>
              ))}
            </div>
            <p style={{ fontSize: '0.9em', color: '#aaa', marginTop: '10px' }}>
              Control citizen behavior: Hope (risk-taking), Trust Decay, Memory Loss (10% forget), Ideology Shift.
            </p>
          </div>

          <div className="media-ownership" style={{ margin: '20px 0', padding: '15px', background: 'rgba(150,50,200,0.05)', borderRadius: '8px' }}>
            <h3>Media Landscape</h3>
            <div style={{ display: 'flex', gap: '15px', flexWrap: 'wrap' }}>
              {mediaInfo.map(media => (
                <div key={media.id} style={{ padding: '10px', background: '#333', borderRadius: '5px', minWidth: '200px' }}>
                  <div style={{ fontWeight: 'bold' }}>Media {media.id.slice(0, 6)}</div>
                  <div style={{ fontSize: '0.9em', color: '#aaa' }}>Owner: {media.ownership}</div>
                  <div style={{ fontSize: '0.9em' }}>Bias: <span style={{ color: media.bias > 0 ? '#4caf50' : '#f44336' }}>{media.bias.toFixed(2)}</span></div>
                  <div style={{ fontSize: '0.9em' }}>Credibility: {(media.credibility * 100).toFixed(0)}%</div>
                </div>
              ))}
            </div>
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

          <HistoryCharts history={history} states={simState.nation.states} />


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
