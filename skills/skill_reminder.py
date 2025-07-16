# skills/skill_reminder.py
import threading
import time

class ReminderSkill:
    def match(self, text):
        return "remind" in text.lower() or "alarm" in text.lower()

    def execute(self, text):
        import re
        match = re.search(r'remind me in (\d+) (seconds|minutes|hours)', text.lower())
        if match:
            amount, unit = int(match.group(1)), match.group(2)
            seconds = amount
            if unit == "minutes":
                seconds *= 60
            elif unit == "hours":
                seconds *= 3600
            threading.Thread(target=self._reminder, args=(seconds,)).start()
            return f"Reminder set for {amount} {unit}."
        return "Please specify a time for the reminder."

    def _reminder(self, seconds):
        time.sleep(seconds)
        print("Alvin: Sir, this is your reminder!")
