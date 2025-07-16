# run_with_wakeword.py
from wakeword_listener import WakeWordListener
from skill_manager import SkillManager

if __name__ == "__main__":
    listener = WakeWordListener()
    manager = SkillManager()
    while True:
        listener.listen()  # Wait for "Hey Alvin"
        print("Alvin is listening...")
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        print("Alvin:", manager.route(user_input))
