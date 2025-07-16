# skill_manager.py
from skills.skill_system import SystemSkill
from skills.skill_timer import TimerSkill
from skills.skill_project import ProjectSkill
from skills.skill_alvin import AlvinChatSkill
from skills.skill_computer_control import ComputerControlSkill
from skills.skill_web_search import WebSearchSkill
from skills.skill_reminder import ReminderSkill
from skills.skill_file_management import FileManagementSkill
from skills.skill_system_monitor import SystemMonitorSkill
from skills.skill_help import HelpSkill
from skills.skill_hf_chat import HuggingFaceChatSkill

class SkillManager:
    def __init__(self):
        self.skills = [
            HelpSkill(),
            SystemSkill(),
            TimerSkill(),
            ProjectSkill(),
            ComputerControlSkill(),
            WebSearchSkill(),
            ReminderSkill(),
            FileManagementSkill(),
            SystemMonitorSkill(),
            AlvinChatSkill(),
            HuggingFaceChatSkill(),  # fallback LLM chat
        ]

    def route(self, text):
        for skill in self.skills:
            if skill.match(text):
                return skill.execute(text)
        return "Sorry, I don't know how to do that."
