# wakeword_listener.py
# Wake word detection for "Hey Alvin" using Porcupine
import sounddevice as sd
import numpy as np
import pvporcupine
import queue

class WakeWordListener:
    def __init__(self, keyword="alvin"):
        self.keyword = keyword
        self.q = queue.Queue()
        self.porcupine = pvporcupine.create(keywords=[self.keyword])
        self.samplerate = 16000
        self.channels = 1
        self.blocksize = 512
        self.stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            dtype='int16',
            blocksize=self.blocksize,
            callback=self.audio_callback
        )

    def audio_callback(self, indata, frames, time, status):
        self.q.put(indata.copy())

    def listen(self):
        print("Listening for wake word 'Hey Alvin'...")
        with self.stream:
            while True:
                data = self.q.get()
                pcm = np.frombuffer(data, dtype=np.int16)
                result = self.porcupine.process(pcm)
                if result >= 0:
                    print("Wake word detected!")
                    return True
