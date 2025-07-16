# skills/skill_alvin_chat.py
from alvin import Alvin
class AlvinChatSkill:
    def __init__(self):
        self.alvin = Alvin()
    def match(self, text):
        # ...existing code...
    def execute(self, text):
        # Use Alvin's LLM to generate a response (synchronously for now)
        return self.alvin.respond(text)
# ...existing code...
