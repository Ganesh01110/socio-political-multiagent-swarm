import random

class LLMFeedbackService:
    def __init__(self):
        self.complaint_templates = [
            "I can barely afford bread while {leader_name} lives like a king!",
            "Corruption is rampant in {state_name}. The taxes are crushing us.",
            "Why is my neighbor getting more funds than me? This system is rigged.",
            "I miss the old days before the Sworm took over.",
            "Does the Supreme Leader even know what's happening here?",
        ]
        
        self.propaganda_templates = [
            "Under the wise guidance of {leader_name}, our state has reached new heights!",
            "Stability is our greatest treasure. Do not listen to the dissenters.",
            "The budget is lean because we are building a better future.",
            "Obey, work, and you shall be rewarded. The Sworm is eternal.",
            "Enemies of the system are enemies of the people.",
        ]

    def generate_feedback(self, nation_state_info: dict, is_propaganda: bool = False) -> str:
        """
        In a real scenario, this would call an LLM API.
        For Phase 7, we use sophisticated templates to mock the behavior.
        """
        leader_name = nation_state_info.get("leader_name", "the Leader")
        state_name = nation_state_info.get("state_name", "our home")
        
        if is_propaganda:
            msg = random.choice(self.propaganda_templates)
        else:
            msg = random.choice(self.complaint_templates)
            
        return msg.format(leader_name=leader_name, state_name=state_name)
