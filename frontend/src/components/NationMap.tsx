import { Stage, Container, Graphics } from '@pixi/react';
import React, { useCallback } from 'react';

// Define Prop Interfaces
interface Agent {
    id: string;
    type: string;
    x: number;
    y: number;
    wealth?: number;
    last_action?: number; // 0=Invest, 1=Steal, 2=Maintain, 3=Propaganda
    faction?: string;
}

interface NationMapProps {
    agents: Agent[];
    width?: number;
    height?: number;
}

const NationMap: React.FC<NationMapProps> = ({ agents, width = 800, height = 600 }) => {

    // Draw Agents in one batch for performance
    const drawAllAgents = useCallback((g: any) => {
        g.clear();

        agents.forEach(agent => {
            let color = 0x2196F3; // Default Blue (Citizen)

            if (agent.type === 'leader') {
                color = 0x4CAF50; // Green
            } else if (agent.type === 'supreme_leader') {
                color = 0xFFFF00; // Yellow
            } else if (agent.type === 'media') {
                color = 0x9C27B0; // Purple
            } else if (agent.type === 'external') {
                color = 0x9E9E9E; // Grey
            } else if (agent.type === 'citizen') {
                if (agent.faction === 'Environmentalist') color = 0x8BC34A;
                else if (agent.faction === 'Technocrat') color = 0x9C27B0;
                else if (agent.faction === 'Industrialist') color = 0x0D47A1;
            }

            let radius = 5;
            let alpha = 1.0;

            if (agent.type === 'external') {
                radius = 15;
                alpha = 0.6;
            } else if (agent.wealth) {
                radius = 5 + (agent.wealth / 10);
                if (agent.wealth < 5) alpha = 0.5;
            }

            // Draw Base Agent with border for clarity
            g.lineStyle(1, 0x333333, 0.6);
            g.beginFill(color, alpha);
            g.drawCircle(agent.x, agent.y, radius);
            g.endFill();
            g.lineStyle(0);

            // Visualize Propaganda (Action 3) - Golden Ring
            if (agent.last_action === 3) {
                g.lineStyle(2, 0xFFD700, 0.8);
                g.drawCircle(agent.x, agent.y, radius + 5);
                g.lineStyle(0);
            }
        });
    }, [agents]);

    return (
        <Stage width={width} height={height} options={{ backgroundColor: 0x1099bb, antialias: true }}>
            <Container>
                <Graphics draw={drawAllAgents} />
            </Container>
        </Stage>
    );
};

export default NationMap;
