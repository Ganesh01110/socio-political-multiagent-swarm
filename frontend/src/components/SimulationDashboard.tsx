import React from 'react';

interface Metrics {
    avg_happiness: number;
    avg_wealth: number;
    avg_trust: number;
    sl_budget: number;
}

interface Props {
    metrics: Metrics;
}

const SimulationDashboard: React.FC<Props> = ({ metrics }) => {
    if (!metrics) return null;

    return (
        <div className="stats-grid">
            <div className="nation-metrics">
                <h3>Nation Metrics</h3>
                <div style={{ display: 'flex', justifyContent: 'space-around', gap: '20px' }}>
                    <div className="metric-box">
                        <strong>Avg Happiness</strong>
                        <div className="bar-container">
                            <div className="bar-fill" style={{ width: `${metrics.avg_happiness}%`, background: '#ff4081' }}></div>
                        </div>
                        {metrics.avg_happiness.toFixed(1)}%
                    </div>

                    <div className="metric-box">
                        <strong>Avg Trust</strong>
                        <div className="bar-container">
                            <div className="bar-fill" style={{ width: `${metrics.avg_trust}%`, background: '#2196f3' }}></div>
                        </div>
                        {metrics.avg_trust.toFixed(1)}%
                    </div>

                    <div className="metric-box">
                        <strong>Avg Wealth</strong>
                        <p>${metrics.avg_wealth.toFixed(2)}</p>
                    </div>

                    <div className="metric-box">
                        <strong>Supreme Leader Budget</strong>
                        <p style={{ color: '#ffd700', fontSize: '1.2em' }}>${metrics.sl_budget.toFixed(2)}</p>
                    </div>
                </div>
            </div>

            <div className="agent-identity-guide">
                <h4>Agent Identity Guide</h4>
                <div className="guide-grid">
                    <div className="guide-group">
                        <h5>Roles & Institutions</h5>
                        <div className="legend-item"><span className="dot" style={{ backgroundColor: '#4CAF50' }}></span> State Leader</div>
                        <div className="legend-item"><span className="dot" style={{ backgroundColor: '#FFFF00' }}></span> Supreme Leader</div>
                        <div className="legend-item"><span className="dot" style={{ backgroundColor: '#9C27B0' }}></span> Media / Institution (L3)</div>
                        <div className="legend-item"><span className="dot" style={{ backgroundColor: '#9E9E9E' }}></span> External Factors (L4)</div>
                    </div>
                    <div className="guide-group">
                        <h5>Ideologies (Citizens)</h5>
                        <div className="legend-item"><span className="dot" style={{ backgroundColor: '#0D47A1' }}></span> Industrialist</div>
                        <div className="legend-item"><span className="dot" style={{ backgroundColor: '#8BC34A' }}></span> Environmentalist</div>
                        <div className="legend-item"><span className="dot" style={{ backgroundColor: '#9C27B0' }}></span> Technocrat</div>
                        <div className="legend-item"><span className="dot" style={{ backgroundColor: '#2196F3' }}></span> Neutral</div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SimulationDashboard;
