# skills/skill_help.py
class HelpSkill:
    def __init__(self):
        self.commands = [
            "system info",
            "set timer",
            "create project folder",
            "click at X Y",
            "move mouse to X Y",
            "type <text>",
            "screenshot",
            "read screen",
            "open app <name>",
            "close app <name>",
            "search <query>",
            "remind me in X minutes/hours/seconds",
            "delete/move/copy file",
            "cpu/ram/battery/system status",
            "help"
        ]
    def match(self, text):
        return "help" in text.lower() or "what can you do" in text.lower()
    def execute(self, text):
        return "Available commands:\n" + "\n".join(self.commands)
