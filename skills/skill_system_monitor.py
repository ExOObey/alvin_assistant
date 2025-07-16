# skills/skill_system_monitor.py
import psutil

class SystemMonitorSkill:
    def match(self, text):
        return any(k in text.lower() for k in ["cpu usage", "ram usage", "battery", "system status"])

    def execute(self, text):
        if "cpu" in text:
            return f"CPU Usage: {psutil.cpu_percent()}%"
        elif "ram" in text:
            mem = psutil.virtual_memory()
            return f"RAM Usage: {mem.percent}% ({mem.used // (1024**2)}MB/{mem.total // (1024**2)}MB)"
        elif "battery" in text:
            if hasattr(psutil, 'sensors_battery'):
                batt = psutil.sensors_battery()
                if batt:
                    return f"Battery: {batt.percent}% {'Plugged in' if batt.power_plugged else 'On battery'}"
                else:
                    return "Battery info not available."
            else:
                return "Battery info not supported on this system."
        elif "system status" in text:
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory()
            return f"CPU: {cpu}%, RAM: {mem.percent}%"
        return "Command not recognized."
