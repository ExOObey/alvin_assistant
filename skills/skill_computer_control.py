# skills/skill_computer_control.py
# This skill integrates self-operating-computer actions into Alvin.
# You must have the self-operating-computer project in your workspace and import its modules.

try:
    import pyautogui
    import pytesseract
    from PIL import Image
except ImportError:
    pyautogui = None
    pytesseract = None
    Image = None

class ComputerControlSkill:
    def match(self, text):
        keywords = ["click", "move mouse", "type", "screenshot", "read screen", "open app", "close app"]
        return any(k in text.lower() for k in keywords)

    def execute(self, text):
        if pyautogui is None:
            return "Computer control libraries are not installed. Please install pyautogui, pytesseract, and pillow."
        text = text.lower()
        import re
        try:
            if "click" in text:
                match = re.search(r'click( at (\d+) (\d+))?', text)
                if match and match.group(2) and match.group(3):
                    x, y = int(match.group(2)), int(match.group(3))
                    pyautogui.click(x, y)
                    return f"Clicked at ({x}, {y})"
                else:
                    pyautogui.click()
                    return "Clicked at current mouse position."
            elif "move mouse" in text:
                match = re.search(r'move mouse to (\d+) (\d+)', text)
                if match:
                    x, y = int(match.group(1)), int(match.group(2))
                    pyautogui.moveTo(x, y)
                    return f"Moved mouse to ({x}, {y})"
                return "Please specify coordinates."
            elif "type" in text:
                match = re.search(r'type (.+)', text)
                if match:
                    to_type = match.group(1)
                    pyautogui.typewrite(to_type)
                    return f"Typed: {to_type}"
                return "Please specify text to type."
            elif "screenshot" in text:
                screenshot = pyautogui.screenshot()
                screenshot.save("alvin_screenshot.png")
                return "Screenshot saved as alvin_screenshot.png."
            elif "read screen" in text and pytesseract and Image:
                screenshot = pyautogui.screenshot()
                text = pytesseract.image_to_string(screenshot)
                return f"Screen text: {text.strip()}"
            elif "open app" in text:
                match = re.search(r'open app (.+)', text)
                if match:
                    app_name = match.group(1).strip()
                    import subprocess
                    subprocess.Popen([app_name])
                    return f"Opened app: {app_name}"
                return "Please specify an app to open."
            elif "close app" in text:
                match = re.search(r'close app (.+)', text)
                if match:
                    app_name = match.group(1).strip()
                    import os
                    os.system(f"pkill {app_name}")
                    return f"Closed app: {app_name}"
                return "Please specify an app to close."
            else:
                return "Command not recognized or not implemented."
        except Exception as e:
            return f"Error executing command: {e}"
