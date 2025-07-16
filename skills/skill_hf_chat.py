# skills/skill_hf_chat.py
from huggingface_llm import HuggingFaceLLM

class HuggingFaceChatSkill:
    def __init__(self):
        self.hf_llm = HuggingFaceLLM()

    def match(self, text):
        # Only match if no other skill matches (fallback)
        return True

    def execute(self, text):
        return self.hf_llm.chat(text)
