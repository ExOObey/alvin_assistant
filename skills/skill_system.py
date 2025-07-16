# skills/skill_system.py
from WIDGETS import system

class SystemSkill:
    def match(self, text):
        return any(word in text.lower() for word in ["system info", "cpu", "ram", "gpu", "computer information"])

    def execute(self, text):
        return system.info()
