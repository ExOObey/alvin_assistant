# skills/skill_web_search.py
from transformers import pipeline

class WebSearchSkill:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def match(self, text):
        return any(k in text.lower() for k in ["search", "look up", "find", "summarize"])

    def execute(self, text):
        # For demo: just summarize the query itself
        # In production: fetch web content, then summarize
        summary = self.summarizer(text, max_length=60, min_length=10, do_sample=False)
        return summary[0]['summary_text']
