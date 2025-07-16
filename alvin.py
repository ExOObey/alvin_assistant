import ollama
import asyncio
import websockets
import json
import base64
from RealtimeSTT import AudioToTextRecorder
import torch
import re
import time
from WIDGETS import system, timer, project
from huggingface_llm import HuggingFaceLLM
import logging
from dotenv import load_dotenv
import os

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
VOICE_ID = os.getenv('VOICE_ID')

try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    pyaudio = None
    PYAUDIO_AVAILABLE = False
    print("[WARNING] PyAudio is not installed. Audio features will be disabled.")

FORMAT = pyaudio.paInt16 if PYAUDIO_AVAILABLE else None
CHANNELS = 1
SEND_SAMPLE_RATE = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNK_SIZE = 1024

class Alvin:
    def __init__(self):
        # Load config
        try:
            config_path = os.path.abspath('config.json')
            with open(config_path) as f:
                self.config = json.load(f)
            logging.info(f"Loaded config from: {config_path}")
        except Exception as e:
            self.config = {}
            logging.warning(f"Failed to load config.json: {e}")
        logging.info(f"Config contents: {self.config}")
        logging.info("initializing...")
        if torch.cuda.is_available():
            self.device = "cuda"
            logging.info("CUDA is available. Using GPU.")
        else:
            self.device = "cpu"
            logging.info("CUDA is not available. Using CPU.")
        self.model = self.config.get('llm_model', "deepseek-r1:1.5b")
        logging.info(f"Using LLM model: {self.model}")
        # Only initialize HuggingFaceLLM if the model name is a valid Hugging Face repo id (no colon and no slash)
        if ":" not in self.model and "/" in self.model:
            self.hf_llm = HuggingFaceLLM(model_name=self.model)  # Hugging Face LLM for chat fallback
        else:
            self.hf_llm = None
            logging.info("Skipping HuggingFaceLLM initialization for Ollama or non-HF models.")
        self.system_behavior = """
            Your name is Alvin (Advanced Logical Virtual INtelligence) you are a helpful AI assistant.  You are an expert in All STEM Fields providing concise and accurate information. When asked to perform a task, respond with the code to perform that task wrapped in ```tool_code```.  If the task does not require a function call, provide a direct answer without using ```tool_code```.  Always respond in a helpful and informative manner."

            You speak with a british accent and address people as Sir.
        """
        self.instruction_prompt_with_function_calling = '''
            At each turn, if you decide to invoke any of the function(s), it should be wrapped with ```tool_code```. If you decide to call a function the response should only have the function wrapped in tool code nothing more. The python methods described below are imported and available, you can only use defined methods also only call methods when you are sure they need to be called. The generated code should be readable and efficient. 
            
            The response to a method will be wrapped in ```tool_output``` use the response to give the user an answer based on the information provided that is wrapped in ```tool_ouput```.

            For regular prompts do not call any functions or wrap the response in ```tool_code```.

            The following Python methods are available:

            ```python
            def camera.open() -> None:
                """Open the camera"""

            def system.info() -> None:
                """ Gathers and prints system information including CPU, RAM, and GPU details. Only call when user ask about computer information. """

            def timer.set(time_str):
                """
                Counts down from a specified time in HH:MM:SS format.

                Args:
                    time_str (str): The time to count down from in HH:MM:SS format.
                """
            def project.create_folder(folder_name):
                """
                Creates a project folder and a text file to store chat history.

                Args:
                    folder_name (str): The name of the project folder to create.
                ```
        User: {user_message}
        '''
        self.model_params = {
            'temperature': 0.1,
            'top_p': 0.9,
        }
        self.conversation_history = []
        self.response_start_time = None
        self.audio_start_time = None

    @property
    def input_queue(self):
        if not hasattr(self, '_input_queue') or self._input_queue is None:
            import asyncio
            self._input_queue = asyncio.Queue(maxsize=2)
        return self._input_queue

    @property
    def response_queue(self):
        if not hasattr(self, '_response_queue') or self._response_queue is None:
            import asyncio
            self._response_queue = asyncio.Queue(maxsize=4)
        return self._response_queue

    @property
    def audio_queue(self):
        if not hasattr(self, '_audio_queue') or self._audio_queue is None:
            import asyncio
            self._audio_queue = asyncio.Queue(maxsize=4)
        return self._audio_queue

    def clear_queues(self):
        self._input_queue = None
        self._response_queue = None
        self._audio_queue = None

    async def input_message(self):
        while True:
            try:
                prompt = await asyncio.to_thread(input, "Enter your message: ")
                if prompt.lower() == "exit":
                    await self.input_queue.put(None)
                    break
                await self.clear_queues()
                await self.input_queue.put(prompt)
            except Exception as e:
                logging.error(f"Error in input_message: {e}")
                continue

    async def send_prompt(self):
        while True:
            try:
                prompt = await self.input_queue.get()
                if prompt is None:
                    break
                self.response_start_time = time.time()
                messages = [{"role": "system", "content": self.system_behavior}] + self.conversation_history + [{"role": "user", "content": self.instruction_prompt_with_function_calling.format(user_message=prompt)}]
                try:
                    # Use streaming API for lowest latency
                    response = ollama.chat(model=self.model, messages=messages, stream=True)
                    full_response = ""
                    in_function_call = False
                    function_call = ""
                    for chunk in response:
                        chunk_content = chunk['message']['content']
                        if chunk_content == "```":
                            if in_function_call == True:
                                in_function_call = False
                                function_call += "```"
                                tool_output = self.extract_tool_call(function_call)
                                messages = [{"role": "system", "content": self.system_behavior}] + self.conversation_history + [{"role": "user", "content": self.instruction_prompt_with_function_calling.format(user_message=tool_output)}]
                                response = ollama.chat(model=self.model, messages=messages, stream=True)
                                for chunk in response:
                                    chunk_content = chunk['message']['content']
                                    logging.info(chunk_content)
                                    await self.response_queue.put(chunk_content)
                                continue
                            else:
                               in_function_call = True
                        if in_function_call == False:
                            await self.response_queue.put(chunk_content)
                        else:
                            function_call += chunk_content                        
                        if chunk_content:
                            logging.info(chunk_content)
                            full_response += chunk_content
                    self.conversation_history.append({"role": "user", "content": prompt})
                    self.conversation_history.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    logging.error(f"An error occurred in send_prompt: {e}")
            except asyncio.CancelledError:
                break
            except Exception as e:
                logging.error(f"Unexpected error in send_prompt: {e}")
            finally:
                await self.response_queue.put(None)

    def extract_tool_call(self, text):
        import io
        from contextlib import redirect_stdout
        pattern = r"```tool_code\s*(.*?)\s*```"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            code = match.group(1).strip()
            f = io.StringIO()
            with redirect_stdout(f):
                result = eval(code)
            output = f.getvalue()
            r = result if output == '' else output
            return f'```tool_output\n{str(r).strip()}\n```'
        return None

    async def tts(self):
        uri = f"wss://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream-input?model_id=eleven_flash_v2_5&output_format=pcm_24000"
        while True:
            try:
                async with websockets.connect(uri) as websocket:
                    try:
                        await websocket.send(json.dumps({
                            "text": " ",
                            "voice_settings": {"stability": 0.4, "similarity_boost": 0.8, "speed": 1.1},
                            "xi_api_key": ELEVENLABS_API_KEY,
                        }))
                        async def listen():
                            while True:
                                try:
                                    message = await websocket.recv()
                                    data = json.loads(message)
                                    if data.get("audio"):
                                        if self.audio_start_time is None:
                                            self.audio_start_time = time.time()
                                            if self.response_start_time is not None:
                                                latency = self.audio_start_time - self.response_start_time
                                                logging.info(f"Time from prompt to first audio byte: {latency:.4f} seconds")
                                        await self.audio_queue.put(base64.b64decode(data["audio"]))
                                    elif data.get('isFinal'):
                                        break
                                except websockets.exceptions.ConnectionClosed:
                                    logging.error("Connection closed in listen")
                                    break
                                except json.JSONDecodeError as e:
                                    logging.error(f"JSON Decode Error in listen: {e}")
                                    break
                                except Exception as e:
                                    logging.error(f"Error in listen: {e}")
                                    break
                        listen_task = asyncio.create_task(listen())
                        try:
                            while True:
                                text = await self.response_queue.get()
                                if text is None:
                                    break
                                await websocket.send(json.dumps({"text": text}))
                        except Exception as e:
                            logging.error(f"Error processing text: {e}")
                        finally:
                            await listen_task
                            self.response_start_time = None
                            self.audio_start_time = None
                    except websockets.exceptions.WebSocketException as e:
                        logging.error(f"WebSocket error: {e}")
                    except Exception as e:
                        logging.error(f"Error during websocket communication: {e}")
            except websockets.exceptions.WebSocketException as e:
                logging.error(f"WebSocket connection error: {e}")
            except Exception as e:
                logging.error(f"Error connecting to websocket: {e}")

    async def play_audio(self):
        if not PYAUDIO_AVAILABLE or self.pya is None:
            print("[INFO] PyAudio is not available. Skipping audio playback.")
            return
        try:
            stream = await asyncio.to_thread(
                self.pya.open,
                format=FORMAT,
                channels=CHANNELS,
                rate=RECEIVE_SAMPLE_RATE,
                output=True,
            )
            while True:
                try:
                    bytestream = await self.audio_queue.get()
                    await asyncio.to_thread(stream.write, bytestream)
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logging.error(f"Error in play_audio loop: {e}")
        except pyaudio.PyAudioError as e:
            logging.error(f"PyAudio error: {e}")
        except Exception as e:
            logging.error(f"Error opening audio stream: {e}")

    async def stt(self):
        if self.recorder is None:
            logging.error("Audio recorder is not initialized.")
            return
        while True:
            try:
                text = await asyncio.to_thread(self.recorder.text)
                await self.clear_queues()
                await self.input_queue.put(text)
            except Exception as e:
                logging.error(f"Error in listen: {e}")
                continue

    async def main(self):
        # Run all tasks concurrently, cancel on any fatal error
        tasks = [
            asyncio.create_task(self.stt()),
            asyncio.create_task(self.send_prompt()),
            asyncio.create_task(self.tts()),
            asyncio.create_task(self.play_audio()),
        ]
        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            logging.error(f"Fatal error in main: {e}")
            for t in tasks:
                t.cancel()

    def respond(self, prompt):
        """Synchronously get a response from Alvin for a given prompt."""
        import asyncio
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        async def get_response():
            self.clear_queues()
            await self.input_queue.put(prompt)
            await self.send_prompt()
            # Collect response from response_queue
            response = []
            while not self.response_queue.empty():
                chunk = await self.response_queue.get()
                if chunk:
                    response.append(chunk)
            return ''.join(response)
        if loop.is_running():
            # If already running, schedule as a task and wait
            return loop.create_task(get_response())
        else:
            return loop.run_until_complete(get_response())
