# WIDGETS.py
# This file provides system, timer, and project utility functions for Alvin.
import os
import platform
import psutil
import time

def system_info():
    """Gathers and returns system information including CPU, RAM, and GPU details."""
    info = []
    info.append("System Information:")
    info.append(f"Platform: {platform.system()} {platform.release()}")
    info.append(f"Processor: {platform.processor()}")
    info.append(f"CPU Cores: {os.cpu_count()}")
    info.append(f"RAM: {round(psutil.virtual_memory().total / (1024**3), 2)} GB")
    # Optional: Add GPU info if GPUtil is available
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        if gpus:
            for gpu in gpus:
                info.append(f"GPU: {gpu.name} ({gpu.memoryTotal}MB)")
        else:
            info.append("GPU: None detected")
    except ImportError:
        info.append("GPU: GPUtil not installed")
    return "\n".join(info)

def timer_set(time_str):
    """Counts down from a specified time in HH:MM:SS format. Returns output as a string."""
    try:
        h, m, s = map(int, time_str.split(':'))
    except Exception:
        return "Invalid time format. Please use HH:MM:SS."
    total_seconds = h * 3600 + m * 60 + s
    output = [f"Timer set for {time_str}."]
    while total_seconds:
        mins, secs = divmod(total_seconds, 60)
        hours, mins = divmod(mins, 60)
        output.append(f"{hours:02d}:{mins:02d}:{secs:02d}")
        time.sleep(1)
        total_seconds -= 1
    output.append("Time's up!")
    return "\n".join(output)

def project_create_folder(folder_name):
    """Creates a project folder and a text file to store chat history. Returns a status string."""
    try:
        os.makedirs(folder_name, exist_ok=True)
        chat_file = os.path.join(folder_name, "chat_history.txt")
        with open(chat_file, "a") as f:
            f.write(f"Project {folder_name} created.\n")
        return f"Project folder '{folder_name}' created with chat history file."
    except Exception as e:
        return f"Error creating project folder: {e}"

# Aliases for Alvin's function calls (with docstrings)
class system:
    """System-related utilities for Alvin."""
    info = staticmethod(system_info)

class timer:
    """Timer utilities for Alvin."""
    set = staticmethod(timer_set)

class project:
    """Project utilities for Alvin."""
    create_folder = staticmethod(project_create_folder)
