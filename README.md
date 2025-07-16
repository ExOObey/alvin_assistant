# Alvin AI Assistant

Alvin is a modular, extensible AI assistant that combines ChatGPT-like conversational abilities (using Ollama and Hugging Face LLMs) with Jarvis-like real-world computer control, voice interaction, and advanced skills.

## Features
- Modular skills (system info, timer, project, computer control, web search, reminders, file management, system monitoring, help, Hugging Face chat)
- Ollama and Hugging Face LLM integration
- ElevenLabs TTS for voice output
- Wake word detection and voice-to-voice loop
- Flask web dashboard for browser-based interaction (with authentication)
- Configurable via `config.json` and `.env`
- Fast, async, and responsive
- Docker and pip install support
- Automated tests and CI

## Setup
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Copy `.env` and set your API keys and dashboard password:
   ```sh
   cp .env .env.local
   # Edit .env.local and set your secrets
   ```
3. Configure `config.json` for your preferences.
4. Run the assistant:
   ```sh
   python main.py
   ```

## Skills
Skills are located in the `skills/` directory and are auto-registered via `SkillManager`.

## Voice & Web
- Voice loop: `python voice_loop.py`
- Wake word: `python run_with_wakeword.py`
- Web dashboard: `python web_dashboard.py` (default password: alvin123 or set `DASHBOARD_PASSWORD` in `.env`)

## Testing
Run tests with:
```sh
python -m unittest discover
```

## Docker
Build and run with Docker:
```sh
docker build -t alvin .
docker run --env-file .env -p 5000:5000 alvin
```

## Profiling
Use the `profiling_utils.profile` decorator to profile function calls.

## Feedback
Feedback is logged to `feedback.log`.

## Contributing
Pull requests and suggestions are welcome!

## License
MIT License (see LICENSE file)

---

# How to Use Alvin AI Assistant

## 1. Installation & Setup

1. **Clone the repository** and enter the directory:
   ```sh
   git clone <your-repo-url>
   cd alvin_assistant
   ```
2. **Install Python dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Install and run Ollama (for local LLMs):**
   - [Ollama install instructions](https://ollama.com/download)
   - Pull a model (e.g. DeepSeek):
     ```sh
     ollama pull deepseek-r1:1.5b
     ollama serve &
     ```
4. **Configure Alvin:**
   - Edit `config.json` to set your preferred LLM (e.g. `deepseek-r1:1.5b` for Ollama, or a Hugging Face repo id for HF models).
   - Set your ElevenLabs API key and Voice ID in `.env`.

## 2. Running Alvin

- **Text mode:**
  ```sh
  python alvin.py
  ```
- **Web dashboard:**
  ```sh
  python web_dashboard.py
  # Open http://localhost:5000 in your browser
  ```
- **Voice mode (browser-based, no PyAudio required):**
  - Use the web dashboard for voice input/output (Web Speech API).
- **Voice mode (native, requires PyAudio):**
  ```sh
  python voice_loop.py
  ```

## 3. Configuration
- `config.json`: Main settings (model, voice, wake word, etc.)
- `.env`: API keys (ElevenLabs, etc.) and dashboard password
- All settings can be edited live via the web dashboard's settings page.

## 4. Skills & Extensibility
- Skills are modular Python files in `skills/` and auto-registered.
- Add new skills by creating a new file in `skills/` and registering with `SkillManager`.
- Example skills: system info, timer, project folder creation, web search, reminders, file management, etc.

## 5. Testing
Run all tests:
```sh
python -m unittest test_alvin
```

## 6. Troubleshooting
- **Model not found:** Ensure your `config.json` model matches an Ollama-pulled model or a valid Hugging Face repo id.
- **Audio not working:** PyAudio is optional; browser-based voice works via the web dashboard.
- **Config not loading:** Make sure `config.json` is valid JSON and not empty.
- **SSL/LibreSSL warnings:** These are safe to ignore unless you have HTTPS/networking issues.

## 7. Advanced
- **Docker:**
  ```sh
  docker build -t alvin .
  docker run --env-file .env -p 5000:5000 alvin
  ```
- **Profiling:** Use `profiling_utils.profile` to profile functions.
- **Feedback:** Feedback is logged to `feedback.log`.

## 8. Security
- Protect your `.env` and API keys.
- Change the dashboard password in `.env`.

## 9. Contributing
Pull requests and suggestions are welcome!

---

# Functionality Overview

- **Text, voice, and web UI interaction**
- **Ollama and Hugging Face LLM support** (auto-detects model type)
- **Modular skills** (add your own in `skills/`)
- **Web dashboard** for config, chat, and voice (no PyAudio required)
- **Robust error handling and logging**
- **Configurable via `config.json` and `.env`**
- **Graceful fallback if dependencies are missing**
- **Test suite for reliability**

---

For more, see the code and comments, or open an issue for help!
