# skills/skill_file_management.py
import os

class FileManagementSkill:
    def match(self, text):
        return any(k in text.lower() for k in ["delete file", "move file", "copy file"])

    def execute(self, text):
        import re
        if "delete file" in text:
            match = re.search(r'delete file (.+)', text)
            if match:
                path = match.group(1).strip()
                try:
                    os.remove(path)
                    return f"Deleted file: {path}"
                except Exception as e:
                    return f"Error deleting file: {e}"
            return "Please specify a file to delete."
        elif "move file" in text:
            match = re.search(r'move file (.+) to (.+)', text)
            if match:
                src, dst = match.group(1).strip(), match.group(2).strip()
                try:
                    os.rename(src, dst)
                    return f"Moved file from {src} to {dst}"
                except Exception as e:
                    return f"Error moving file: {e}"
            return "Please specify source and destination."
        elif "copy file" in text:
            match = re.search(r'copy file (.+) to (.+)', text)
            if match:
                src, dst = match.group(1).strip(), match.group(2).strip()
                try:
                    import shutil
                    shutil.copy(src, dst)
                    return f"Copied file from {src} to {dst}"
                except Exception as e:
                    return f"Error copying file: {e}"
            return "Please specify source and destination."
        return "Command not recognized."
