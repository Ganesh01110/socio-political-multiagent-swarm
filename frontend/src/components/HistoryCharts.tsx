import { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface HistoryData {
    tick: number;
    state_id?: string | null;
    avg_happiness: number;
    avg_wealth: number;
    avg_trust: number;
    sl_budget: number;
}

interface State {
    id: string;
    name: string;
}

interface Props {
    history: HistoryData[];
    states: State[];
}

const HistoryCharts = ({ history, states }: Props) => {
    const [activeStateId, setActiveStateId] = useState<string | null>(null);

    const filteredData = history.filter(d =>
        activeStateId === null ? (d.state_id === null || d.state_id === undefined) : d.state_id === activeStateId
    );

    const activeName = activeStateId === null ? "National" : states.find(s => s.id === activeStateId)?.name || "State";

    return (
        <div className="history-charts" style={{ width: '100%', minHeight: 450, marginTop: '20px', backgroundColor: '#222', padding: '20px', borderRadius: '10px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <h3 style={{ color: 'white', margin: 0 }}>{activeName} Trends Over Time</h3>
                <div className="tabs" style={{ display: 'flex', gap: '5px' }}>
                    <button
                        onClick={() => setActiveStateId(null)}
                        style={{
                            padding: '5px 10px',
                            backgroundColor: activeStateId === null ? '#2196f3' : '#444',
                            border: 'none',
                            borderRadius: '4px',
                            color: 'white',
                            cursor: 'pointer'
                        }}
                    >
                        National
                    </button>
                    {states.map(state => (
                        <button
                            key={state.id}
                            onClick={() => setActiveStateId(state.id)}
                            style={{
                                padding: '5px 10px',
                                backgroundColor: activeStateId === state.id ? '#2196f3' : '#444',
                                border: 'none',
                                borderRadius: '4px',
                                color: 'white',
                                cursor: 'pointer'
                            }}
                        >
                            {state.name}
                        </button>
                    ))}
                </div>
            </div>

            <ResponsiveContainer width="100%" height={350}>
                <LineChart data={filteredData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                    <XAxis dataKey="tick" stroke="#ccc" />
                    <YAxis stroke="#ccc" />
                    <Tooltip contentStyle={{ backgroundColor: '#333', borderColor: '#555', color: '#fff' }} />
                    <Legend />
                    <Line type="monotone" dataKey="avg_happiness" stroke="#ff4081" name="Happiness" dot={false} strokeWidth={2} />
                    <Line type="monotone" dataKey="avg_trust" stroke="#2196f3" name="Trust" dot={false} strokeWidth={2} />
                    <Line type="monotone" dataKey="avg_wealth" stroke="#4caf50" name="Wealth" dot={false} strokeWidth={2} />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default HistoryCharts;

