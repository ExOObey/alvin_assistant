import unittest
import asyncio
from alvin import Alvin

class TestAlvin(unittest.TestCase):
    def setUp(self):
        try:
            self.loop = asyncio.get_event_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
        self.alvin = Alvin()

    def test_basic_response(self):
        response = self.alvin.respond("What is 2+2?")
        self.assertIn("4", response)

    def test_system_info(self):
        response = self.alvin.respond("Tell me about my system.")
        self.assertIn("System Information", response)

    def test_timer(self):
        response = self.alvin.respond("Set a timer for 00:00:02")
        self.assertIn("Timer set for 00:00:02", response)

    def test_project_create(self):
        response = self.alvin.respond("Create a project folder named TestProject")
        self.assertIn("Project folder", response)

if __name__ == "__main__":
    unittest.main()
