import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl

class FuzzyMoralityService:
    def __init__(self):
        # Antecedents (Inputs)
        self.greed = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'greed')
        self.trust = ctrl.Antecedent(np.arange(0, 101, 1), 'trust')
        self.pressure = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'pressure')
        
        # Consequents (Outputs)
        self.moral_resistance = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'moral_resistance')
        
        # Membership Functions - Greed
        self.greed['low'] = fuzzy.trimf(self.greed.universe, [0, 0, 0.5])
        self.greed['med'] = fuzzy.trimf(self.greed.universe, [0.2, 0.5, 0.8])
        self.greed['high'] = fuzzy.trimf(self.greed.universe, [0.5, 1, 1])
        
        # Membership Functions - Trust
        self.trust['low'] = fuzzy.trimf(self.trust.universe, [0, 0, 40])
        self.trust['med'] = fuzzy.trimf(self.trust.universe, [30, 50, 70])
        self.trust['high'] = fuzzy.trimf(self.trust.universe, [60, 100, 100])
        
        # Membership Functions - Pressure
        self.pressure['low'] = fuzzy.trimf(self.pressure.universe, [0, 0, 0.4])
        self.pressure['high'] = fuzzy.trimf(self.pressure.universe, [0.4, 1, 1])
        
        # Membership Functions - Moral Resistance
        self.moral_resistance['low'] = fuzzy.trimf(self.moral_resistance.universe, [0, 0, 0.4])
        self.moral_resistance['med'] = fuzzy.trimf(self.moral_resistance.universe, [0.3, 0.5, 0.7])
        self.moral_resistance['high'] = fuzzy.trimf(self.moral_resistance.universe, [0.6, 1, 1])
        
        # Define Rules
        rule1 = ctrl.Rule(self.greed['high'] & self.trust['low'], self.moral_resistance['low'])
        rule2 = ctrl.Rule(self.greed['low'] & self.trust['high'], self.moral_resistance['high'])
        rule3 = ctrl.Rule(self.pressure['high'] & self.trust['low'], self.moral_resistance['med'])
        rule4 = ctrl.Rule(self.greed['med'], self.moral_resistance['med'])
        
        self.morality_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
        self.morality_sim = ctrl.ControlSystemSimulation(self.morality_ctrl)

    def calculate_moral_resistance(self, greed_val: float, trust_val: float, pressure_val: float) -> float:
        """
        Returns a value between 0 and 1 indicating how much the agent resists 
        acting purely on greed or external pressure.
        """
        try:
            self.morality_sim.input['greed'] = greed_val
            self.morality_sim.input['trust'] = trust_val
            self.morality_sim.input['pressure'] = pressure_val
            
            self.morality_sim.compute()
            return self.morality_sim.output['moral_resistance']
        except Exception:
            return 0.5 # Default middle ground

class FuzzyEmotionService:
    def __init__(self):
        # Similar setup for scaling emotions
        pass
