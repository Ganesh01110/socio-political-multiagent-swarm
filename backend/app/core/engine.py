import uuid
from typing import Dict, List
from app.models.world import Nation, State
from app.models.agents import BaseAgent, CitizenAgent, StateLeaderAgent, SupremeLeaderAgent, AgentType
from app.core.election import ElectionService
from app.core.economy import EconomyService
from app.core.social import InfluenceService
from app.core.supreme import SupremeLeaderService
from app.db.database import SessionLocal, engine, Base
from app.db.models import SimulationHistory
from app.core.llm import LLMFeedbackService
import random

class TickScheduler:
    def __init__(self):
        self.current_tick = 0

    def tick(self):
        self.current_tick += 1
        return self.current_tick

class SimulationEngine:
    def __init__(self):
        self.scheduler = TickScheduler()
        self.is_running = False
        self.nation: Nation = None
        self.agents: Dict[str, BaseAgent] = {}
        self.election_service = ElectionService()
        self.economy_service = EconomyService()
        self.social_service = InfluenceService()
        self.supreme_service = SupremeLeaderService(self.election_service)
        self.llm_service = LLMFeedbackService()
        self.last_election_results = []
        
        # Create Tables with error handling
        try:
            print(f"DEBUG: Initializing Database Connection...")
            # Mask password in logs
            log_url = str(engine.url).split("@")[-1] if "@" in str(engine.url) else str(engine.url)
            print(f"DEBUG: Connecting to: ...@{log_url}")
            
            Base.metadata.create_all(bind=engine)
            self.db_session = SessionLocal()
            print("DEBUG: Database initialized and tables created successfully.")
        except Exception as e:
            print(f"CRITICAL ERROR: Failed to initialize database: {e}")
            self.db_session = None # Graceful failure
        
        self.initialize_world()

    def initialize_world(self):
        # Create States
        states = []
        for i in range(3):
            state_id = str(uuid.uuid4())
            state = State(
                id=state_id,
                name=f"State {i+1}",
                population=50  # Increased for social complexity
            )
            states.append(state)
            
            # Create Leader
            leader_id = str(uuid.uuid4())
            leader = StateLeaderAgent(
                id=leader_id,
                honesty=random.random(),
                greed=random.random(),
                competence=random.random(),
                state_id=state_id,
                x=random.random() * 800, # Random X within bounds
                y=random.random() * 600  # Random Y within bounds
            )
            self.agents[leader_id] = leader
            state.leader_id = leader_id

            # Create Citizens
            factions = ["Industrialist", "Environmentalist", "Technocrat", "Neutral"]
            weights = [1, 7, 7, 6] # 1 Industrialist to 20 Others (7+7+6=20)
            
            for j in range(state.population):
                citizen_id = str(uuid.uuid4())
                faction = random.choices(factions, weights=weights)[0]
                
                citizen = CitizenAgent(
                    id=citizen_id,
                    honesty=random.random(),
                    greed=random.random(),
                    competence=random.random(),
                    state_id=state_id,
                    happiness=50 + random.randint(-10, 10),
                    faction=faction,
                    faction_loyalty=random.uniform(30, 70),
                    age=random.randint(0, 80), # Start with diverse ages
                    lifespan=random.randint(80, 120),
                    x=random.random() * 800,
                    y=random.random() * 600
                )
                self.agents[citizen_id] = citizen

        # Create Nation
        self.nation = Nation(
            id=str(uuid.uuid4()),
            name="Sworm Nation",
            states=states
        )

        # Create Supreme Leader
        sl_id = str(uuid.uuid4())
        sl = SupremeLeaderAgent(
            id=sl_id,
            honesty=random.random(),
            greed=random.random(),
            competence=random.random(),
            tenure_remaining=10
        )
        self.agents[sl_id] = sl
        self.nation.supreme_leader_id = sl_id

        # Phase 9: Create Media Agents (L3 - Purple)
        from app.models.agents import MediaAgent, ExternalFactorAgent
        for i in range(3):
            m_id = str(uuid.uuid4())
            media = MediaAgent(
                id=m_id,
                honesty=random.random(),
                greed=random.uniform(0.1, 0.4),
                competence=random.uniform(0.6, 0.9),
                credibility=random.uniform(0.5, 0.8),
                bias=random.uniform(-0.5, 0.5),
                x=random.random() * 800,
                y=random.random() * 600
            )
            self.agents[m_id] = media

        # Phase 9: Create External Factor Agent (L4 - Grey)
        wf_id = str(uuid.uuid4())
        world_agent = ExternalFactorAgent(
            id=wf_id,
            honesty=1.0,
            greed=0.0,
            competence=1.0,
            x=400,
            y=300
        )
        self.agents[wf_id] = world_agent

    def start(self):
        self.is_running = True

    def stop(self):
        self.is_running = False

    def advance(self):
        # Allow manual ticks even if stopped (for now)
        # if not self.is_running:
        #    return None
        
        tick = self.scheduler.tick()
        
        # Phase 2: Economy & Election Trigger
        
        # 1. Economy Cycle
        # Get Supreme Leader
        sl = self.agents.get(self.nation.supreme_leader_id)
        
        # Get State Leaders
        state_leaders = [
            self.agents.get(s.leader_id) for s in self.nation.states 
            if s.leader_id in self.agents
        ]
        
        # Distribute Nation -> States
        if sl:
            self.economy_service.distribute_national_budget(sl, self.nation, state_leaders)

        # Distribute State -> Citizens
        for state in self.nation.states:
            leader = self.agents.get(state.leader_id)
            if not leader:
                continue

            citizens = [
                a for a in self.agents.values() 
                if a.type == AgentType.CITIZEN and a.state_id == state.id
            ]
            
            self.economy_service.process_state_economy(leader, citizens)

            # Generate LLM Feedback (Phase 7)
            if tick % 5 == 0:
                 is_propaganda = (leader.last_action == 3)
                 feedback = self.llm_service.generate_feedback({
                     "leader_name": f"Leader {leader.id[:4]}",
                     "state_name": state.name
                 }, is_propaganda=is_propaganda)
                 leader.recent_feedback = feedback
                 
                 # Also Add to last_election_results/news feed for visibility
                 self.last_election_results.insert(0, {
                     "outcome": "Social Feedback",
                     "winner_name": "Citizens" if not is_propaganda else "State Media",
                     "state_id": state.name,
                     "reason": feedback
                 })
                 # Keep news feed short
                 if len(self.last_election_results) > 10:
                     self.last_election_results.pop()

        # Trigger Election every 50 ticks
        if tick % 50 == 0:
            self.run_elections()

        # Social Dynamics (Every tick)
        self.social_service.propagate_influence(list(self.agents.values()))
        
        # Generational Turnover (Age & Replace)
        self._process_generational_turnover()

        # Phase 9: Media & World Events
        self._process_media_narratives()
        self._process_world_events(tick)

        # Supreme Leader Actions (Tax & Enforcement)
        sl = self.agents.get(self.nation.supreme_leader_id)
        state_leaders = [
            self.agents.get(s.leader_id) for s in self.nation.states 
            if s.leader_id in self.agents
        ]
        
        if sl:
            # 1. Collect Taxes (Every 10 ticks)
            if tick % 10 == 0:
                self.supreme_service.collect_taxes(sl, state_leaders)
            
            # 2. Evaluate & Fire (Every 25 ticks)
            # Pass a dict of State Objects keyed by ID for easy access
            state_dict = {s.id: s for s in self.nation.states}
            if tick % 25 == 0:
                fired_events = self.supreme_service.evaluate_leaders(state_dict, self.agents, tick)
                # If anyone fired, add to news?
                for event in fired_events:
                     self.last_election_results.append({
                         "outcome": "Leader Executed",
                         "winner_name": "Appointed Leader",
                         "state_id": "Unknown", # Need to fetch state name if needed
                         "reason": event["reason"]
                     })

        # Calculate Global Metrics
        all_citizens = [a for a in self.agents.values() if a.type == AgentType.CITIZEN]
        metrics = {
            "avg_happiness": 0,
            "avg_wealth": 0,
            "avg_trust": 0,
            "sl_budget": sl.total_budget if sl else 0
        }
        
        if all_citizens:
             metrics["avg_happiness"] = sum(c.happiness for c in all_citizens) / len(all_citizens)
             metrics["avg_wealth"] = sum(c.wealth for c in all_citizens) / len(all_citizens)
             metrics["avg_trust"] = sum(c.trust_score for c in all_citizens) / len(all_citizens)

        # ---------------------------------------------
        # PERSIST DATA (Phase 6)
        # ---------------------------------------------
        if self.db_session:
            try:
                history_record = SimulationHistory(
                    tick=tick,
                    avg_happiness=metrics["avg_happiness"],
                    avg_wealth=metrics["avg_wealth"],
                    avg_trust=metrics["avg_trust"],
                    sl_budget=metrics["sl_budget"]
                )
                self.db_session.add(history_record)
                self.db_session.commit()
            except Exception as e:
                print(f"DB Error during save: {e}")
                self.db_session.rollback()
        else:
            print("DEBUG: Skipping DB persistence (no active session)")

        return {
            "tick": tick,
            "nation": self.nation,
            "agents": list(self.agents.values()),
            "last_election_results": self.last_election_results,
            "metrics": metrics
        }

    def run_elections(self):
        self.last_election_results = []
        for state in self.nation.states:
            current_leader = self.agents.get(state.leader_id)
            if not current_leader:
                continue

            # Get citizens for this state
            citizens = [
                a for a in self.agents.values() 
                if a.type == AgentType.CITIZEN and a.state_id == state.id
            ]

            winner_id, details = self.election_service.conduct_state_election(
                state.id, current_leader, citizens
            )

            if winner_id == "challenger":
                # Replace Leader
                new_leader = self.election_service.create_new_leader(state.id)
                
                # Remove old leader
                del self.agents[current_leader.id]
                
                # Add new leader
                self.agents[new_leader.id] = new_leader
                state.leader_id = new_leader.id
                
                details["outcome"] = "Incumbent Defeated"
                details["winner_name"] = "New Leader"
                
                # TERMINAL PUNISHMENT
                brain = self.economy_service.get_brain(leader_id)
                if hasattr(current_leader, 'last_dqn_state') and current_leader.last_dqn_state is not None:
                    brain.remember(current_leader.last_dqn_state, current_leader.last_action, -100.0, current_leader.last_dqn_state, True)
                    brain.learn()

            else:
                details["outcome"] = "Incumbent Re-elected"
                details["winner_name"] = "Incumbent"

                # TERMINAL REWARD (Bonuses)
                brain = self.economy_service.get_brain(leader_id)
                if hasattr(current_leader, 'last_dqn_state') and current_leader.last_dqn_state is not None:
                    brain.remember(current_leader.last_dqn_state, current_leader.last_action, +100.0, current_leader.last_dqn_state, True)
                    brain.learn()
            
            self.last_election_results.append(details)

    def _process_generational_turnover(self):
        """Ages citizens and replaces those who reach their lifespan."""
        dead_citizens = []
        new_citizens = {}
        
        for agent_id, agent in self.agents.items():
            if agent.type == AgentType.CITIZEN:
                agent.age += 1
                if agent.age >= agent.lifespan:
                    dead_citizens.append(agent_id)
                    
                    # Create Descendant
                    child_id = str(uuid.uuid4())
                    # Inherit 50% of wealth
                    inherited_wealth = agent.wealth * 0.5
                    # Mutate loyalty slightly
                    new_loyalty = max(0, min(100, agent.faction_loyalty + random.uniform(-10, 10)))
                    
                    child = CitizenAgent(
                        id=child_id,
                        honesty=max(0, min(1.0, agent.honesty + random.uniform(-0.1, 0.1))),
                        greed=max(0, min(1.0, agent.greed + random.uniform(-0.1, 0.1))),
                        competence=max(0, min(1.0, agent.competence + random.uniform(-0.1, 0.1))),
                        state_id=agent.state_id,
                        happiness=50,
                        wealth=inherited_wealth,
                        faction=agent.faction, # Inherit faction
                        faction_loyalty=new_loyalty,
                        age=0,
                        lifespan=random.randint(80, 120),
                        x=agent.x, # Born at same location
                        y=agent.y
                    )
                    new_citizens[child_id] = child
                    
                    # Notify News (Every 10 deaths to avoid spam)
                    if len(dead_citizens) % 10 == 0:
                        self.last_election_results.insert(0, {
                            "outcome": "Generational Turnover",
                            "winner_name": "New Generation",
                            "state_id": agent.state_id[:10],
                            "reason": f"A new generation has inherited the future."
                        })
        
        # Remove dead, add new
        for d_id in dead_citizens:
            del self.agents[d_id]
        
        self.agents.update(new_citizens)

    def _process_media_narratives(self):
        """Media agents influence trust in their proximity."""
        media_agents = [a for a in self.agents.values() if a.type == AgentType.MEDIA]
        citizens = [a for a in self.agents.values() if a.type == AgentType.CITIZEN]
        
        for media in media_agents:
            # Decide on a narrative based on bias
            # Positive bias pushes pro-leader narrative
            narrative_force = media.bias * media.credibility
            
            for citizen in citizens:
                dist = ((citizen.x - media.x)**2 + (citizen.y - media.y)**2)**0.5
                if dist < media.reach:
                    # Influence trust
                    citizen.trust_score = max(0, min(100, citizen.trust_score + narrative_force))
                    # Occasionally update happiness too
                    if random.random() < 0.1:
                        citizen.happiness = max(0, min(100, citizen.happiness + narrative_force))

    def _process_world_events(self, tick: int):
        """Randomly triggers global events that affect all agents."""
        world_agent = next((a for a in self.agents.values() if a.type == AgentType.EXTERNAL), None)
        if not world_agent:
            return

        # Check for event cooldown or duration
        if world_agent.active_event and tick % 20 == 0:
             world_agent.active_event = None # Event Ends
             self.last_election_results.insert(0, {
                 "outcome": "Global Event Ended",
                 "winner_name": "Stability",
                 "state_id": "World",
                 "reason": "The global crisis/boom has stabilized."
             })

        if not world_agent.active_event and tick % 40 == 0 and random.random() < 0.4:
            events = [
                ("Economic Recession", -10, "Happiness and wealth are declining globally."),
                ("Technological Boom", 15, "Efficiency increases wealth for all."),
                ("Natural Disaster", -15, "Infrastructure damage reduces happiness."),
                ("Scientific Discovery", 10, "Improved quality of life improves stability.")
            ]
            evt_name, severity, reason = random.choice(events)
            world_agent.active_event = evt_name
            world_agent.event_severity = severity
            
            self.last_election_results.insert(0, {
                "outcome": "Global Event",
                "winner_name": evt_name,
                "state_id": "World",
                "reason": reason
            })

        # Apply active event effects
        if world_agent.active_event:
            impact = world_agent.event_severity / 10.0
            for agent in self.agents.values():
                if agent.type == AgentType.CITIZEN:
                    agent.happiness = max(0, min(100, agent.happiness + impact))
                    if impact > 0:
                        agent.wealth += impact
                    else:
                        agent.wealth = max(0, agent.wealth + impact)

    def get_state(self):
        # Calculate Global Metrics for consistency
        all_citizens = [a for a in self.agents.values() if a.type == AgentType.CITIZEN]
        sl = self.agents.get(self.nation.supreme_leader_id)
        metrics = {
            "avg_happiness": 0,
            "avg_wealth": 0,
            "avg_trust": 0,
            "sl_budget": sl.total_budget if sl else 0
        }
        
        if all_citizens:
             metrics["avg_happiness"] = sum(c.happiness for c in all_citizens) / len(all_citizens)
             metrics["avg_wealth"] = sum(c.wealth for c in all_citizens) / len(all_citizens)
             metrics["avg_trust"] = sum(c.trust_score for c in all_citizens) / len(all_citizens)

        return {
            "tick": self.scheduler.current_tick,
            "nation": self.nation,
            "agents": list(self.agents.values()),
            "last_election_results": self.last_election_results,
            "metrics": metrics
        }

# Global Instance
simulation_instance = SimulationEngine()
