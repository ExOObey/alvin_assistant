import asyncio
from alvin import Alvin  # Alvin class should be defined in alvin.py
from skill_manager import SkillManager

if __name__ == "__main__":
    manager = SkillManager()
    alvin = Alvin()
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        # You can route through SkillManager or directly use Alvin's respond method
        print("Alvin:", alvin.respond(user_input))
