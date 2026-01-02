import random
import json
import os

class QLearningAgent:
    def __init__(self, actions=[0, 1, 2, 3], learning_rate=0.1, discount_factor=0.9, epsilon=0.1):
        self.q_table = {} # State -> {Action -> Value}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.actions = actions

    def get_q_value(self, state, action):
        return self.q_table.get(str(state), {}).get(action, 0.0)

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        
        # Greedy action
        state_key = str(state)
        current_q = self.q_table.get(state_key, {})
        if not current_q:
            return random.choice(self.actions)
        
        # Find max Q
        max_q = max(current_q.values())
        # Random choice among ties
        best_actions = [a for a, q in current_q.items() if q == max_q]
        # If some actions haven't been explored in this state, they are implicitly 0.
        # But here we only choose from "known" bests or random if empty.
        # Actually, simpler: just iterate all actions
        best_value = -float('inf')
        best_action = random.choice(self.actions)
        
        for action in self.actions:
            q = self.get_q_value(state, action)
            if q > best_value:
                best_value = q
                best_action = action
            elif q == best_value:
                # Tie-break roughly
                if random.random() < 0.5:
                    best_action = action
        
        return best_action

    def learn(self, state, action, reward, next_state):
        current_q = self.get_q_value(state, action)
        
        # Max Q for next state
        max_next_q = -float('inf')
        for a in self.actions:
            q = self.get_q_value(next_state, a)
            if q > max_next_q:
                max_next_q = q
        
        if max_next_q == -float('inf'):
            max_next_q = 0.0

        # Q-Learning Formula
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        
        # Update Table
        state_key = str(state)
        if state_key not in self.q_table:
            self.q_table[state_key] = {}
        self.q_table[state_key][action] = new_q

    def save_model(self, filepath="q_table.json"):
        try:
            # Json keys must be strings
            with open(filepath, 'w') as f:
                json.dump(self.q_table, f)
        except Exception as e:
            print(f"Failed to save model: {e}")

    def load_model(self, filepath="q_table.json"):
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    self.q_table = json.load(f)
                    # Convert keys back if needed (JSON loads keys as strings)
            except Exception as e:
                print(f"Failed to load model: {e}")
