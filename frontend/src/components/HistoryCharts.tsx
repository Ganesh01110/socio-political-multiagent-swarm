import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface HistoryData {
    tick: number;
    avg_happiness: number;
    avg_wealth: number;
    avg_trust: number;
    sl_budget: number;
}

interface Props {
    history: HistoryData[];
}

const HistoryCharts = ({ history }: Props) => {
    return (
        <div className="history-charts" style={{ width: '100%', height: 400, marginTop: '20px', backgroundColor: '#222', padding: '20px', borderRadius: '10px' }}>
            <h3 style={{ color: 'white', marginBottom: '20px' }}>National Trends Over Time</h3>
            <ResponsiveContainer width="100%" height="90%">
                <LineChart data={history} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
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
