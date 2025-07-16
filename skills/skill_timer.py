# skills/skill_timer.py
from WIDGETS import timer
import re

class TimerSkill:
    def match(self, text):
        return "timer" in text.lower() or "countdown" in text.lower()

    def execute(self, text):
        # Extract time in HH:MM:SS or MM:SS or SS
        match = re.search(r'(\d{1,2}:\d{2}:\d{2}|\d{1,2}:\d{2}|\d+)', text)
        if match:
            time_str = match.group(1)
            if ":" not in time_str:
                # If only seconds provided
                time_str = f"00:00:{int(time_str):02d}"
            elif time_str.count(":") == 1:
                # If MM:SS provided
                time_str = f"00:{time_str}"
            return timer.set(time_str)
        return "Please specify a time for the timer."
