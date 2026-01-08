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
  state_metrics: Record<string, any>;
  settings: Record<string, any>;
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
  const [settings, setSettings] = useState<Record<string, any>>({
    enable_hope_mechanic: true,
    enable_trust_decay: true,
    enable_happiness_influence: true,
    enable_memory_loss: true,
    enable_ideology_shift: true,
    inheritance_tax_rate: 0.5,
    corruption_efficiency: 0.5,
    show_social_graph: false
  })
  const [highlightType, setHighlightType] = useState<'all' | 'politician' | 'regular'>('all')
  const [mediaInfo, setMediaInfo] = useState<any[]>([])


  const fetchState = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/simulation/state')
      setSimState(response.data)

      if (response.data.settings) {
        setSettings(response.data.settings)
      }

      // Fetch history
      const historyRes = await axios.get('http://localhost:8000/api/simulation/history')
      setHistory(historyRes.data)

      // Fetch Policy
      const policyRes = await axios.get('http://localhost:8000/api/simulation/policy')
      setPolicy(policyRes.data)

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
    const interval = setInterval(fetchState, 1000)
    return () => clearInterval(interval)
  }, [])

  const updateSetting = async (key: string, value: any) => {
    const newSettings = { ...settings, [key]: value };
    setSettings(newSettings);
    await axios.post('http://localhost:8000/api/simulation/settings', newSettings);
  };

  return (
    <div className="app-container">
      {/* Sidebar Controls - 15% */}
      <aside className="sidebar">
        <h2>Sworm Sim 2.0</h2>

        <div className="control-group">
          <h3>Simulation Control</h3>
          <button className="sidebar-btn" onClick={async () => {
            const res = await axios.post('http://localhost:8000/api/simulation/tick');
            setSimState(res.data);
          }}>Manual Tick</button>

          <button className="sidebar-btn clear" onClick={async () => {
            if (window.confirm("Clear all history?")) {
              await axios.post('http://localhost:8000/api/simulation/history/clear');
              setHistory([]);
              fetchState();
            }
          }}>Clear History</button>
        </div>

        <div className="control-group">
          <h3>View Filters</h3>
          <label className="sidebar-label">
            <input
              type="radio" name="highlight" value="all"
              checked={highlightType === 'all'}
              onChange={() => setHighlightType('all')}
            /> All Citizens
          </label>
          <label className="sidebar-label">
            <input
              type="radio" name="highlight" value="politician"
              checked={highlightType === 'politician'}
              onChange={() => setHighlightType('politician')}
            /> Politicians
          </label>
          <label className="sidebar-label">
            <input
              type="radio" name="highlight" value="regular"
              checked={highlightType === 'regular'}
              onChange={() => setHighlightType('regular')}
            /> Regular People
          </label>
        </div>


        <div className="control-group">
          <h3>Advanced Metrics</h3>
          <label className="sidebar-label">
            <span>Inheritance Tax: <strong>{(settings.inheritance_tax_rate * 100).toFixed(0)}%</strong></span>
            <input
              type="range" min="0.01" max="0.60" step="0.01"
              value={settings.inheritance_tax_rate}
              onChange={(e) => updateSetting('inheritance_tax_rate', parseFloat(e.target.value))}
            />
          </label>

          <label className="sidebar-label">
            <span>Corruption Eff.: <strong>{(settings.corruption_efficiency * 100).toFixed(0)}%</strong></span>
            <input
              type="range" min="0" max="1.0" step="0.05"
              value={settings.corruption_efficiency}
              onChange={(e) => updateSetting('corruption_efficiency', parseFloat(e.target.value))}
            />
          </label>

          <label className="toggle-switch">
            <input
              type="checkbox"
              checked={settings.show_social_graph}
              onChange={(e) => updateSetting('show_social_graph', e.target.checked)}
            />
            Show Social Graph
          </label>
        </div>

        <div className="control-group">
          <h3>Emotion Toggles</h3>
          {Object.entries(policy).map(([key, value]) => (
            <label key={key} className="toggle-switch">
              <input
                type="checkbox"
                checked={value}
                onChange={async () => {
                  const newPolicy = { ...policy, [key]: !value };
                  setPolicy(newPolicy);
                  await axios.post('http://localhost:8000/api/simulation/policy', newPolicy);
                }}
              />
              {key.replace('consider_', '').charAt(0).toUpperCase() + key.replace('consider_', '').slice(1)}
            </label>
          ))}
        </div>

        <div className="control-group">
          <h3>Mechanics</h3>
          {Object.entries(settings).map(([key, value]) => {
            if (typeof value !== 'boolean') return null;
            if (key === 'show_social_graph') return null;
            return (
              <label key={key} className="toggle-switch">
                <input
                  type="checkbox"
                  checked={value}
                  onChange={() => updateSetting(key, !value)}
                />
                {key.replace('enable_', '').split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
              </label>
            );
          })}
        </div>
      </aside>

      {/* Main Content Area - 85% */}
      <main className="main-content">
        {error && <div className="error-banner">{error}</div>}

        {simState ? (
          <>
            <div style={{ display: 'flex', gap: '20px' }}>
              <div className="stats-container" style={{ flex: 1 }}>
                <h2>Cycle: {simState.tick} | {simState.nation.name}</h2>
                <SimulationDashboard metrics={simState.metrics} />
              </div>

              <div className="media-mini-pane" style={{ flex: 1, background: '#111', padding: '15px', borderRadius: '12px' }}>
                <h3>Media Landscape</h3>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                  {mediaInfo.map(m => (
                    <div key={m.id} style={{ fontSize: '0.8rem', padding: '8px', background: '#222', borderRadius: '5px' }}>
                      <strong>{m.id.slice(0, 4)}</strong>: {m.ownership} | <span style={{ color: m.bias > 0 ? '#4caf50' : '#f44336' }}>{m.bias.toFixed(1)}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="simulation-viewport">
              <NationMap
                agents={simState.agents}
                stateMetrics={simState.state_metrics}
                showSocialGraph={settings.show_social_graph}
                highlightType={highlightType}
              />
            </div>

            <div className="news-feed">
              <ul>
                {simState.last_election_results.map((res: any, idx: number) => (
                  <li key={idx}>
                    <strong>{res.state_id?.slice(0, 8)}</strong>: {res.reason || res.outcome}
                  </li>
                ))}
              </ul>
            </div>

            <div className="state-metrics-grid">
              {Object.entries(simState.state_metrics).map(([id, data]: [string, any]) => (
                <div key={id} className="state-metric-card" style={{ borderLeftColor: data.color }}>
                  <h4>{data.name}</h4>
                  <div className="metric_val">Population: <strong>{data.population}</strong></div>
                  <div className="metric_val">Politician Wealth: <strong>{data.leader_wealth.toFixed(0)}</strong></div>
                  <div className="metric_val">Avg Citizen Wealth: <strong>{data.avg_wealth_citizens.toFixed(1)}</strong></div>
                </div>
              ))}
            </div>

            <HistoryCharts history={history} states={simState.nation.states} />
          </>
        ) : (
          <div className="loading-state">Initialising Simulation Engines...</div>
        )}
      </main>
    </div>
  )
}

export default App
