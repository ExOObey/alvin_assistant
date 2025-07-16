# huggingface_llm.py
from transformers import pipeline

class HuggingFaceLLM:
    def __init__(self, model_name="mistralai/Mistral-7B-Instruct-v0.2"):
        self.generator = pipeline("text-generation", model=model_name, device_map="auto")

    def chat(self, prompt, max_length=256):
        result = self.generator(prompt, max_length=max_length, do_sample=True)
        return result[0]['generated_text']

def load_llm(model_name):
    """Simple wrapper to create a HuggingFaceLLM instance for a given model name."""
    return HuggingFaceLLM(model_name)
