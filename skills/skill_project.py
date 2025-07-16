# skills/skill_project.py
from WIDGETS import project
import re

class ProjectSkill:
    def match(self, text):
        return "project" in text.lower() and "folder" in text.lower()

    def execute(self, text):
        # Extract folder name
        match = re.search(r'project folder (named |called )?(\w+)', text.lower())
        if match:
            folder_name = match.group(2)
            return project.create_folder(folder_name)
        return "Please specify a project folder name."
