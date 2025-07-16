# voice_loop.py
# Full voice-to-voice loop for Alvin: wake word -> record -> transcribe -> process -> speak
import asyncio
from wakeword_listener import WakeWordListener
from skill_manager import SkillManager
from RealtimeSTT import AudioToTextRecorder
import pyaudio
import time

async def main_voice_loop():
    listener = WakeWordListener()
    manager = SkillManager()
    recorder = AudioToTextRecorder(model='large-v3', language='en')
    pya = pyaudio.PyAudio()
    print("Alvin is running in voice mode. Say 'Hey Alvin' to begin.")
    while True:
        listener.listen()  # Wait for wake word
        print("Listening for your command...")
        # Record and transcribe
        text = await asyncio.to_thread(recorder.text)
        print(f"You: {text}")
        if text.lower() == "exit":
            break
        # Process
        response = manager.route(text)
        print(f"Alvin: {response}")
        # Speak response (using ElevenLabs TTS)
        # (Assumes you have a tts function in Alvin or a standalone one)
        # from alvin import Alvin
        # alvin = Alvin()
        # await alvin.tts_response(response)
        # For now, just print. You can uncomment above to use TTS.

if __name__ == "__main__":
    asyncio.run(main_voice_loop())
