import { Stage, Container, Graphics } from '@pixi/react';
import React, { useCallback } from 'react';

// Define Prop Interfaces
interface Agent {
    id: string;
    type: string;
    x: number;
    y: number;
    wealth?: number;
    last_action?: number;
    faction?: string;
    state_id?: string;
    social_links?: string[];
}

interface NationMapProps {
    agents: Agent[];
    stateMetrics: Record<string, any>;
    showSocialGraph: boolean;
    highlightType: 'all' | 'politician' | 'regular';
    width?: number;
    height?: number;
}

const NationMap: React.FC<NationMapProps> = ({ agents, stateMetrics, showSocialGraph, highlightType, width = 1200, height = 700 }) => {



    const drawAllAgents = useCallback((g: any) => {
        g.clear();

        // 1. Draw Social Graph Lines first (so they are under agents)
        if (showSocialGraph && stateMetrics) {
            const agentMap = new Map(agents.map(a => [a.id, a]));

            agents.forEach(agent => {
                const stateColor = agent.state_id ? (stateMetrics[agent.state_id]?.color || "#2196F3") : "#2196F3";
                const hexColor = parseInt(stateColor.replace('#', ''), 16);

                if (agent.social_links) {
                    agent.social_links.forEach(targetId => {
                        const target = agentMap.get(targetId);
                        if (target) {
                            g.lineStyle(1, hexColor, 0.4);
                            g.moveTo(agent.x, agent.y);
                            g.lineTo(target.x, target.y);
                        }
                    });
                }
            });
            g.lineStyle(0);
        }

        // 2. Draw Agents
        agents.forEach(agent => {
            let color = 0x2196F3; // Default Blue (Citizen)
            const stateColor = (agent.state_id && stateMetrics && stateMetrics[agent.state_id])
                ? (stateMetrics[agent.state_id].color || "#2196F3")
                : "#2196F3";
            const hexStateColor = parseInt(stateColor.replace('#', ''), 16);


            const isPolitician = agent.type === 'leader' || agent.type === 'supreme_leader';
            const isRegular = agent.type === 'citizen';

            if (agent.type === 'leader') {
                color = 0xFF5722; // Distinct Orange-Red for Politicians
            } else if (agent.type === 'supreme_leader') {

                color = 0xFFFF00;
            } else if (agent.type === 'media') {
                color = 0x9C27B0;
            } else if (agent.type === 'external') {
                color = 0x9E9E9E;
            } else if (isRegular) {
                color = hexStateColor;
            }

            let radius = 5;
            let alpha = 1.0;

            // Apply Highlighting Dimming
            if (highlightType === 'politician' && !isPolitician) {
                alpha = 0.1;
            } else if (highlightType === 'regular' && !isRegular) {
                alpha = 0.1;
            }

            if (agent.type === 'supreme_leader') {
                radius = 22; // Even bigger Supreme Leader
            } else if (agent.type === 'external') {

                radius = 15;
                alpha = alpha * 0.6;
            } else if (agent.wealth !== undefined) {
                radius = 5 + (agent.wealth / 10);
                if (agent.wealth < 5) alpha = alpha * 0.5;
            }


            // Draw Base Agent
            g.lineStyle(agent.type === 'leader' ? 3 : 1, agent.type === 'leader' ? 0xFFFFFF : 0x333333, 0.6);
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
    }, [agents, stateMetrics, showSocialGraph, highlightType]);


    return (
        <Stage width={width} height={height} options={{ backgroundColor: 0x111111, antialias: true }}>
            <Container>
                <Graphics draw={drawAllAgents} />
            </Container>
        </Stage>
    );
};

export default NationMap;
