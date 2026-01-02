from abc import ABC, abstractmethod
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
from typing import List, Dict, Any, Optional
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from app.ml.dqn import DQNAgent

class DecisionPolicy(ABC):
    @abstractmethod
    def decide(self, state: np.ndarray) -> int:
        pass

    @abstractmethod
    def learn(self, state: np.ndarray, action: int, reward: float, next_state: np.ndarray, done: bool):
        pass

class RuleBasedPolicy(DecisionPolicy):
    def __init__(self, rules: List[Dict[str, Any]]):
        self.rules = rules

    def decide(self, state: np.ndarray) -> int:
        # Example state: [trust, unemployment, leader_honesty, ...]
        # rules: [{"condition": lambda s: s[0] < 0.3 and s[1] > 0.5, "action": 1}, ...]
        for rule in self.rules:
            if rule["condition"](state):
                return rule["action"]
        return 0 # Default action

    def learn(self, state: np.ndarray, action: int, reward: float, next_state: np.ndarray, done: bool):
        pass # Rule-based doesn't learn in this simple form

class ANNPolicy(DecisionPolicy):
    def __init__(self, state_size: int, action_size: int, hidden_size: int = 16):
        self.model = nn.Sequential(
            nn.Linear(state_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, action_size),
            nn.Softmax(dim=-1)
        )
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.01)

    def decide(self, state: np.ndarray) -> int:
        state_tensor = torch.FloatTensor(state)
        probs = self.model(state_tensor)
        return torch.multinomial(probs, 1).item()

    def learn(self, state: np.ndarray, action: int, reward: float, next_state: np.ndarray, done: bool):
        # Simplified policy gradient step
        state_tensor = torch.FloatTensor(state)
        probs = self.model(state_tensor)
        log_prob = torch.log(probs[action])
        loss = -log_prob * reward
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

class DQNPolicy(DecisionPolicy):
    def __init__(self, state_size: int, action_size: int, long_horizon: bool = False):
        self.agent = DQNAgent(state_size, action_size)
        self.long_horizon = long_horizon

    def decide(self, state: np.ndarray) -> int:
        return self.agent.choose_action(state)

    def learn(self, state: np.ndarray, action: int, reward: float, next_state: np.ndarray, done: bool):
        if self.long_horizon:
            # Long horizon reward might consolidate multiple steps or increase gamma
            reward *= 1.5 
        self.agent.remember(state, action, reward, next_state, done)
        self.agent.learn()

class HybridPolicy(DecisionPolicy):
    def __init__(self, state_size: int, action_size: int):
        self.strategic_layer = DQNPolicy(state_size, action_size)
        
        # Scikit-learn models for specific behaviors
        self.perception_layer = RandomForestClassifier(n_estimators=10)
        self.decision_layer = DecisionTreeClassifier()
        self.social_layer = KNeighborsClassifier(n_neighbors=3)
        
        # New: Fuzzy Logic Morality Layer
        from app.core.fuzzy import FuzzyMoralityService
        self.morality_evaluator = FuzzyMoralityService()

        # Mock training data to initialize models
        X = np.random.rand(10, state_size)
        y = np.random.randint(0, action_size, 10)
        self.perception_layer.fit(X, y)
        self.decision_layer.fit(X, y)
        self.social_layer.fit(X, y)

    def decide(self, state: np.ndarray) -> int:
        """
        Combined decision using weighted voting between layers.
        Strategic Layer (DQN) has high weight for leaders.
        Perception/Social layers modify the 'raw' strategic choice.
        """
        # 1. Get strategic action
        strat_action = self.strategic_layer.decide(state)
        
        # 2. Get ensemble opinion
        ensemble_actions = [
            self.perception_layer.predict(state.reshape(1, -1))[0],
            self.decision_layer.predict(state.reshape(1, -1))[0],
            self.social_layer.predict(state.reshape(1, -1))[0]
        ]
        
        # 3. Simple Voting
        from collections import Counter
        all_actions = [strat_action] + ensemble_actions
        final_action = Counter(all_actions).most_common(1)[0][0]
        
        # 4. Fuzzy Morality Constraint
        # Input: trust (state[0]), greed (assumed constant for policy or from state)
        # For simplicity, we assume some state dims represent these or we pass them
        # Let's say we check if the action is 'extreme' (e.g., Steal = 1)
        if final_action == 1: # Action 1 is 'Steal' in economy.py
            # Calculate resistance based on current state trust and a mock greed
            resistance = self.morality_evaluator.calculate_moral_resistance(0.7, state[0]*100, 0.5)
            if resistance > 0.6:
                return 0 # Revert to 'Maintain' (Action 0) due to guilt/resistance
        
        return final_action

    def learn(self, state: np.ndarray, action: int, reward: float, next_state: np.ndarray, done: bool):
        # Strategic layer learns continuously
        self.strategic.remember(state, action, reward, next_state, done)
        self.strategic.learn()
        
        # Other layers might retrain periodically (e.g., every 100 steps)
        # For this prototype, we'll keep them static or update with small probability
        if random.random() < 0.05:
             # Online update (very simplified)
             X = state.reshape(1, -1)
             y = np.array([action])
             
             # Scikit-learn doesn't support easy 'partial_fit' for all models
             # This is a placeholder for real online learning
             pass
