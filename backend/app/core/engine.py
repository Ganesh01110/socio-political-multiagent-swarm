import uuid
from typing import Dict, List
from app.models.world import Nation, State
from app.models.agents import BaseAgent, CitizenAgent, StateLeaderAgent, SupremeLeaderAgent, AgentType, MediaAgent, ExternalFactorAgent
from app.core.election import ElectionService
from app.core.economy import EconomyService
from app.core.social import InfluenceService
from app.core.supreme import SupremeLeaderService
from app.db.database import SessionLocal, engine, Base
from app.db.models import SimulationHistory
from app.core.llm import LLMFeedbackService
from app.core.fuzzy import FuzzyMoralityService
from app.core.media import MediaService

from app.ml.brain_stack import (
    DecisionPolicy, RuleBasedPolicy, ANNPolicy, DQNPolicy, HybridPolicy
)
from app.core.generators import initialize_agents_with_dist, initialize_media_with_dist, ScenarioGenerator
import random
import numpy as np
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SwormSim")

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
        self.agent_policies: Dict[str, DecisionPolicy] = {}
        
        # Economic Feedback Variables
        self.inflation_rate = 0.02
        self.unemployment_rate = 0.05
        self.black_economy_scale = 0.01
        self.black_economy_scale = 0.01
        self.fuzzy_morality_service = FuzzyMoralityService()
        
        # Policy Settings (Emotion Toggles for Leaders)
        self.policy_settings = {
            "consider_trust": True,
            "consider_fear": True,
            "consider_happiness": True,
            "consider_wealth": True
        }

        # Simulation Settings
        self.simulation_settings = {
            "enable_hope_mechanic": True,
            "enable_trust_decay": True,
            "enable_happiness_influence": True,
            "enable_memory_loss": True,
            "enable_ideology_shift": True,
            "inheritance_tax_rate": 0.5, # Default 50%
            "corruption_efficiency": 0.5, # 50% of stolen money reaches leader
            "show_social_graph": False
        }
        
        # State Colors for Network Graph
        self.state_colors = [
            "#2196F3", # Blue
            "#4CAF50", # Green
            "#FF9800", # Orange
            "#E91E63", # Pink
            "#9C27B0"  # Purple
        ]

        
        # Media Service
        self.media_service = MediaService()


        
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

    def _create_policy(self, agent_type: AgentType, role: str = "") -> DecisionPolicy:
        """Strategy based brain selection."""
        # state_size: trust, wealth, happiness, budget, inflation, unemployment, inequality
        state_size = 7 
        action_size = 4 # Default actions
        
        if role == "supreme_leader":
            # Supreme Leader keeps complex DQN for deep strategy
            return DQNPolicy(state_size, action_size, long_horizon=True)
        
        # All other agents (Leaders, Influencers, Citizens) use Standard Neural Brains (ANN)
        # to ensure unified intelligence while remaining performant.
        return ANNPolicy(state_size, action_size, hidden_size=16)


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
            self.agent_policies[leader_id] = self._create_policy(AgentType.LEADER)
            state.leader_id = leader_id

            # Create Citizens with Synthetic Distribution
            citizens = initialize_agents_with_dist(state_id, 50)
            for citizen in citizens:
                self.agents[citizen.id] = citizen
                # Randomly assign some as influencers
                role = "influencer" if random.random() < 0.05 else "citizen"
                self.agent_policies[citizen.id] = self._create_policy(AgentType.CITIZEN, role=role)

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
        self.agent_policies[sl_id] = self._create_policy(AgentType.SUPREME_LEADER, role="supreme_leader")
        self.nation.supreme_leader_id = sl_id

        # Phase 9: Create Media Agents with Distribution
        media_agents = initialize_media_with_dist(3)
        for media in media_agents:
            self.agents[media.id] = media

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

        # Phase 10: Initialize Social Graph
        self._initialize_social_graph()

    def _initialize_social_graph(self):
        """Creates social connections based on proximity and occupation/faction."""
        citizens = [a for a in self.agents.values() if a.type == AgentType.CITIZEN]
        leaders = [a for a in self.agents.values() if a.type == AgentType.LEADER]
        
        # Leaders have larger circles (political network)
        for leader in leaders:
            # Connect to some citizens in their state
            state_citizens = [c for c in citizens if c.state_id == leader.state_id]
            sample_size = min(len(state_citizens), 15)
            connections = random.sample(state_citizens, sample_size)
            for c in connections:
                leader.social_links.append(c.id)
                c.social_links.append(leader.id)

        # Citizens connect to neighbors
        for i, c1 in enumerate(citizens):
            for c2 in citizens[i+1:]:
                if c1.state_id == c2.state_id:
                    dist = ((c1.x - c2.x)**2 + (c1.y - c2.y)**2)**0.5
                    if dist < 80.0 and random.random() < 0.7:
                        c1.social_links.append(c2.id)
                        c2.social_links.append(c1.id)
        
        # Assign memory loss to 10% of citizens
        memory_loss_count = int(len(citizens) * 0.1)
        memory_loss_citizens = random.sample(citizens, memory_loss_count)
        for citizen in memory_loss_citizens:
            citizen.has_memory_loss = True
        
        # Connect media to agents for ownership determination
        media_agents = [a for a in self.agents.values() if a.type == AgentType.MEDIA]
        for media in media_agents:
            # Randomly connect to some leaders and citizens
            potential_owners = leaders + random.sample(citizens, min(5, len(citizens)))
            connections = random.sample(potential_owners, min(3, len(potential_owners)))
            for agent in connections:
                media.social_links.append(agent.id)
            
            # Determine initial ownership
            self.media_service.determine_ownership(media, self.agents)



    def start(self):
        self.is_running = True

    def stop(self):
        self.is_running = False

    def advance(self):
        # Allow manual ticks even if stopped (for now)
        # if not self.is_running:
        #    return None
        
        tick = self.scheduler.tick()
        
        # 1. Calculate Global Economic Metrics (Feedback Loop)
        all_citizens = [a for a in self.agents.values() if a.type == AgentType.CITIZEN]
        if all_citizens:
            avg_wealth = sum(c.wealth for c in all_citizens) / len(all_citizens)
            wealth_sq_diff = sum((c.wealth - avg_wealth)**2 for c in all_citizens)
            inequality = (wealth_sq_diff / len(all_citizens))**0.5 / (avg_wealth + 0.1)
            
            # Simple Feedback: High inequality -> inflation increases, unemployment increases
            self.inflation_rate = max(0.01, self.inflation_rate + (inequality * 0.001) - 0.0005)
            self.unemployment_rate = max(0.02, self.unemployment_rate + (self.inflation_rate * 0.1) - 0.001)
        else:
            inequality = 0.0
        
        # 2. Process Decisions for each agent
        for agent_id, agent in self.agents.items():
            policy = self.agent_policies.get(agent_id)
            if not policy: continue
            
            # Construct State Vector: [trust, wealth, happiness, budget, inflation, unemployment, inequality]
            budget = getattr(agent, 'budget_allocated', 0.0) or getattr(agent, 'total_budget', 0.0)
            state_vec = np.array([
                agent.trust_score / 100.0,
                min(1.0, getattr(agent, 'wealth', 0.0) / 1000.0),
                getattr(agent, 'happiness', 50.0) / 100.0,
                min(1.0, budget / 1000.0),
                self.inflation_rate,
                self.unemployment_rate,
                min(1.0, inequality)
            ])
            
            # Decision
            action = policy.decide(state_vec)
            
            # Execute Action Effects (Stochasticity added)
            if random.random() < agent.cognitive_bias:
                 # Irrational action!
                 action = random.randint(0, 3)
            
            # Store for learning
            agent.last_action = action
            agent.last_state_vec = state_vec 
            
            # 4. Fuzzy Moral Update
            # Agents update their moral bias based on global conditions
            # If trust is high, morality increases; if pressure (inflation/unemployment) is high, it decreases
            pressure = (self.inflation_rate + self.unemployment_rate) * 5.0
            agent.moral_resistance = self.fuzzy_morality_service.calculate_moral_resistance(
                agent.greed, agent.trust_score, pressure
            )

            # Rich Log for Rule-based
            if isinstance(policy, RuleBasedPolicy) and action != 0:
                 logger.info(f"AGENT {agent_id[:4]} (RuleBased) decided to ACTION {action} at tick {tick} | Trust: {agent.trust_score:.2f}, Unemployment: {self.unemployment_rate:.2f}")
        
        # 3. Economy Cycle
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
            
            # Execute economy and get reward
            reward = self.economy_service.process_state_economy(
                leader, citizens, self.inflation_rate, self.unemployment_rate, self.policy_settings, self.simulation_settings
            )


            
            # Learn Step for Leader
            leader_policy = self.agent_policies.get(leader.id)
            if leader_policy and hasattr(leader, 'last_state_vec'):
                # For learning, we need to decide next state vec (simplified: current)
                leader_policy.learn(leader.last_state_vec, leader.last_action, reward, leader.last_state_vec, False)

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

        # Social Dynamics (Every tick)
        self.social_service.propagate_influence(self.agents)
        
        # Apply Simulation Settings Mechanics
        if self.simulation_settings.get("enable_memory_loss", True) and tick % 20 == 0:
            # Memory loss: 10% of citizens forget past grievances
            for citizen in all_citizens:
                if citizen.has_memory_loss:
                    citizen.trust_score = 50.0  # Reset to neutral
                    citizen.happiness = 50.0
                    citizen.fear = 0.0
        
        if self.simulation_settings.get("enable_trust_decay", True):
            # Natural trust erosion over time
            for citizen in all_citizens:
                citizen.trust_score = max(0, citizen.trust_score - 0.5)
        
        if self.simulation_settings.get("enable_ideology_shift", True):
            # Ideology shifts based on social pressure
            for citizen in all_citizens:
                peers = [self.agents[pid] for pid in citizen.social_links if pid in self.agents]
                if peers:
                    avg_ideology = [sum(p.ideology[i] for p in peers) / len(peers) for i in range(2)]
                    # Gradual shift toward peer average
                    citizen.ideology[0] += (avg_ideology[0] - citizen.ideology[0]) * 0.1
                    citizen.ideology[1] += (avg_ideology[1] - citizen.ideology[1]) * 0.1
        
        # Phase 11: Dynamic Social Network Evolution (Cronyism)
        # Every 30 ticks, citizens try to "climb" the social ladder
        if tick % 30 == 0:
            for state in self.nation.states:
                leader = self.agents.get(state.leader_id)
                if not leader: continue
                
                state_citizens = [a for a in self.agents.values() if a.type == AgentType.CITIZEN and a.state_id == state.id]
                if not state_citizens: continue
                
                # 1. Decay: 20% chance to lose touch with a random connection
                for agent in state_citizens + [leader]:
                    if agent.social_links and random.random() < 0.2:
                        idx = random.randint(0, len(agent.social_links) - 1)
                        target_id = agent.social_links.pop(idx)
                        # Remove back-link
                        if target_id in self.agents:
                            target = self.agents[target_id]
                            if agent.id in target.social_links:
                                target.social_links.remove(agent.id)
                
                # 2. Formation: Ambitious citizens seek the Leader's circle
                # Top 10% wealthiest citizens in the state have a chance to connect to the leader
                state_citizens.sort(key=lambda x: x.wealth, reverse=True)
                elite_count = max(1, int(len(state_citizens) * 0.1))
                elites = state_citizens[:elite_count]
                
                for elite in elites:
                    # If not already connected and rich enough
                    if elite.id not in leader.social_links and random.random() < 0.4:
                        leader.social_links.append(elite.id)
                        elite.social_links.append(leader.id)
                        logger.info(f"New connection: Wealthy Citizen {elite.id[:4]} joins Leader {leader.id[:4]}'s circle.")

        
        # Media Influence (Every tick)
        media_agents = [a for a in self.agents.values() if a.type == AgentType.MEDIA]
        for media in media_agents:
            # Update ownership dynamically
            self.media_service.determine_ownership(media, self.agents)
            # Calculate bias based on owner
            bias = self.media_service.calculate_bias(media, self.agents)
            media.bias = bias
            # Propagate narrative to citizens
            self.media_service.propagate_narrative(media, all_citizens, bias)

        
        # Check for Coups (Every 10 ticks)
        if tick % 10 == 0:
            for state in self.nation.states:
                leader = self.agents.get(state.leader_id)
                citizens = [a for a in self.agents.values() if a.type == AgentType.CITIZEN and a.state_id == state.id]
                if leader and self.election_service.check_for_coup(state.id, leader, citizens):
                    # COUP SUCCESSFUL
                    self.last_election_results.insert(0, {
                        "outcome": "COUP D'ÉTAT",
                        "winner_name": "Revolutionary Council",
                        "state_id": state.name,
                        "reason": "The leader was overthrown by a mass protest movement."
                    })
                    # Replace Leader
                    new_leader = self.election_service.create_new_leader(state.id)
                    del self.agents[leader.id]
                    self.agents[new_leader.id] = new_leader
                    state.leader_id = new_leader.id
                    self.agent_policies[new_leader.id] = self._create_policy(AgentType.LEADER)

        # Trigger Election every 50 ticks
        if tick % 50 == 0:
            self.run_elections()

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
                     # Initialize policy for NEW leader
                     new_leader_id = event.get("new_leader_id") # I need to update supreme.py to return this
                     if new_leader_id and new_leader_id in self.agents:
                         self.agent_policies[new_leader_id] = self._create_policy(AgentType.LEADER)
                     
                     # Old policy should be removed if still exists
                     old_leader_id = event.get("old_leader")
                     if old_leader_id in self.agent_policies:
                         del self.agent_policies[old_leader_id]

                     self.last_election_results.append({
                         "outcome": "Leader Executed",
                         "winner_name": "Appointed Leader",
                         "state_id": "Unknown",
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
             metrics["inflation"] = self.inflation_rate
             metrics["unemployment"] = self.unemployment_rate
             
             # Calculate Inequality
             avg_wealth = metrics["avg_wealth"]
             wealth_sq_diff = sum((c.wealth - avg_wealth)**2 for c in all_citizens)
             metrics["inequality"] = (wealth_sq_diff / len(all_citizens))**0.5 / (avg_wealth + 0.1)

             # Protest Level
             metrics["protest_level"] = sum(c.protest_intent for c in all_citizens) / len(all_citizens)


        # ---------------------------------------------
        # PERSIST DATA (Phase 6)
        # ---------------------------------------------
        if self.db_session:
            try:
                # 1. Save Global History
                history_record = SimulationHistory(
                    tick=tick,
                    state_id=None, # Global
                    avg_happiness=metrics["avg_happiness"],
                    avg_wealth=metrics["avg_wealth"],
                    avg_trust=metrics["avg_trust"],
                    sl_budget=metrics["sl_budget"]
                )
                self.db_session.add(history_record)

                # 2. Save Per-State History
                for state in self.nation.states:
                    s_citizens = [a for a in self.agents.values() if a.type == AgentType.CITIZEN and a.state_id == state.id]
                    if s_citizens:
                        s_metrics = {
                            "avg_happiness": sum(c.happiness for c in s_citizens) / len(s_citizens),
                            "avg_wealth": sum(c.wealth for c in s_citizens) / len(s_citizens),
                            "avg_trust": sum(c.trust_score for c in s_citizens) / len(s_citizens)
                        }
                        s_record = SimulationHistory(
                            tick=tick,
                            state_id=state.id,
                            avg_happiness=s_metrics["avg_happiness"],
                            avg_wealth=s_metrics["avg_wealth"],
                            avg_trust=s_metrics["avg_trust"],
                            sl_budget=0 # Not applicable to single states
                        )
                        self.db_session.add(s_record)
                
                self.db_session.commit()
            except Exception as e:

                print(f"DB Error during save: {e}")
                self.db_session.rollback()
        else:
            print("DEBUG: Skipping DB persistence (no active session)")

        # Global stability check
        if metrics.get("protest_level", 0) > 0.6:
            self.last_election_results.insert(0, {
                "outcome": "Mass Protest",
                "winner_name": "Protesters",
                "state_id": "Global",
                "reason": "Widespread social unrest detected due to poor conditions."
            })


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
                state.id, current_leader, citizens, self.agents
            )


            if winner_id == "challenger":
                # Replace Leader
                new_leader = self.election_service.create_new_leader(state.id)
                
                # Remove old leader
                del self.agents[current_leader.id]
                if current_leader.id in self.agent_policies:
                    del self.agent_policies[current_leader.id]
                
                # Add new leader
                self.agents[new_leader.id] = new_leader
                self.agent_policies[new_leader.id] = self._create_policy(AgentType.LEADER)
                state.leader_id = new_leader.id
                
                details["outcome"] = "Incumbent Defeated"
                details["winner_name"] = "New Leader"
                
                # TERMINAL PUNISHMENT
                policy = self.agent_policies.get(current_leader.id)
                if policy and hasattr(current_leader, 'last_state_vec'):
                    policy.learn(current_leader.last_state_vec, current_leader.last_action, -100.0, current_leader.last_state_vec, True)

            else:
                details["outcome"] = "Incumbent Re-elected"
                details["winner_name"] = "Incumbent"

                # TERMINAL REWARD (Bonuses)
                policy = self.agent_policies.get(current_leader.id)
                if policy and hasattr(current_leader, 'last_state_vec'):
                    policy.learn(current_leader.last_state_vec, current_leader.last_action, +100.0, current_leader.last_state_vec, True)
            
            self.last_election_results.append(details)

    def _process_generational_turnover(self):
        """Ages citizens and replaces those who reach their lifespan."""
        dead_citizens = []
        new_citizens = {}
        
        tax_rate = self.simulation_settings.get("inheritance_tax_rate", 0.5)
        
        for agent_id, agent in self.agents.items():
            if agent.type == AgentType.CITIZEN:
                agent.age += 1
                if agent.age >= agent.lifespan:
                    dead_citizens.append(agent_id)
                    
                    # 1 to 3 children (Variable Birth Rate)
                    num_children = random.randint(1, 3)
                    
                    for _ in range(num_children):
                        child_id = str(uuid.uuid4())
                        # Distribute wealth after tax among children
                        inherited_wealth = (agent.wealth * (1.0 - tax_rate)) / num_children
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
                            x=agent.x + random.uniform(-20, 20), # Spread children slightly
                            y=agent.y + random.uniform(-20, 20),
                            education=agent.education + random.uniform(-0.1, 0.1),
                            ideology=[i + random.uniform(-0.05, 0.05) for i in agent.ideology]
                        )
                        new_citizens[child_id] = child
                        # Initialize policy for child
                        self.agent_policies[child_id] = self._create_policy(AgentType.CITIZEN)
                        
                        # Inheritance of some social links (e.g., 20% of family network)
                        if agent.social_links:
                            family_network = random.sample(agent.social_links, min(2, len(agent.social_links)))
                            child.social_links.extend(family_network)
                    
                    # Notify News (Every 10 deaths to avoid spam)
                    if len(dead_citizens) % 10 == 0:
                        self.last_election_results.insert(0, {
                            "outcome": "Demographic Shift",
                            "winner_name": "New Generation",
                            "state_id": agent.state_id[:10],
                            "reason": f"Population turnover in state {agent.state_id[:8]}."
                        })

        
        # Remove dead, add new
        for d_id in dead_citizens:
            del self.agents[d_id]
            if d_id in self.agent_policies:
                del self.agent_policies[d_id]
        
        self.agents.update(new_citizens)

    def _process_media_narratives(self):
        """Media agents influence trust in their proximity."""
        media_agents = [a for a in self.agents.values() if a.type == AgentType.MEDIA]
        citizens = [a for a in self.agents.values() if a.type == AgentType.CITIZEN]
        
        for media in media_agents:
            # Algorithmic Amplification
            effective_reach = media.reach * media.algorithmic_amplification
            
            # Disinformation Rate: Chance to flip logic
            is_disinfo = random.random() < media.disinformation_rate
            
            # Narrative force based on ownership and bias
            # If owned by State, mostly positive bias
            narrative_force = media.bias * media.credibility
            if is_disinfo:
                narrative_force *= -1.5 # Disinfo is more volatile
            
            for citizen in citizens:
                dist = ((citizen.x - media.x)**2 + (citizen.y - media.y)**2)**0.5
                if dist < effective_reach:
                    # Education buffer: higher education = less influence from media
                    edu_buffer = 1.0 - (citizen.education * 0.5)
                    
                    impact = narrative_force * edu_buffer
                    
                    # Influence trust
                    citizen.trust_score = max(0, min(100, citizen.trust_score + impact))
                    
                    # Log narrative warfare
                    if is_disinfo and random.random() < 0.01:
                        self.last_election_results.insert(0, {
                            "outcome": "Narrative Warfare",
                            "winner_name": media.ownership,
                            "state_id": "Global",
                            "reason": f"Disinformation campaign detected by {media.id[:4]}"
                        })

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

        # Per-State Summary Metrics
        state_metrics = {}
        for i, state in enumerate(self.nation.states):
            s_citizens = [a for a in self.agents.values() if a.type == AgentType.CITIZEN and a.state_id == state.id]
            s_leader = self.agents.get(state.leader_id)
            
            # Map color to state
            color = self.state_colors[i % len(self.state_colors)]
            
            state_metrics[state.id] = {
                "name": state.name,
                "population": len(s_citizens),
                "avg_wealth_citizens": sum(c.wealth for c in s_citizens) / len(s_citizens) if s_citizens else 0,
                "leader_wealth": s_leader.wealth if s_leader else 0,
                "color": color
            }

        return {
            "tick": self.scheduler.current_tick,
            "nation": self.nation,
            "agents": list(self.agents.values()),
            "last_election_results": self.last_election_results,
            "metrics": metrics,
            "state_metrics": state_metrics,
            "settings": self.simulation_settings
        }


# Global Instance
simulation_instance = SimulationEngine()
