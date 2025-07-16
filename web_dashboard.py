# web_dashboard.py
from flask import Flask, render_template_string, request, session, redirect, url_for, jsonify
from skill_manager import SkillManager
import os
import json

app = Flask(__name__)
manager = SkillManager()
app.secret_key = os.getenv('DASHBOARD_SECRET', 'change_this_secret')

HTML = '''
<!DOCTYPE html>
<html>
<head><title>Alvin Web Dashboard</title></head>
<body>
<h1>Alvin Web Dashboard</h1>
{% if not session.get('authed') %}
<form method="post" action="/login">
    <input type="password" name="password" placeholder="Password">
    <input type="submit" value="Login">
</form>
{% else %}
<form method="post" id="chatForm">
    <input type="text" name="query" id="query" placeholder="Ask Alvin..." style="width:300px;">
    <input type="submit" value="Send">
    <button type="button" onclick="startRecognition()">🎤</button>
    <button type="button" onclick="speakResponse()">🔊</button>
</form>
{% if response %}<p><b>Alvin:</b> <span id="alvin_response">{{ response }}</span></p>{% endif %}
<a href="/logout">Logout</a>
<a href="/settings">Settings</a>
{% endif %}
<script>
// Voice input (Web Speech API)
function startRecognition() {
    if (!('webkitSpeechRecognition' in window)) {
        alert('Web Speech API not supported in this browser.');
        return;
    }
    var recognition = new webkitSpeechRecognition();
    recognition.lang = 'en-US';
    recognition.onresult = function(event) {
        document.getElementById('query').value = event.results[0][0].transcript;
    };
    recognition.start();
}
// Voice output (Web Speech API)
function speakResponse() {
    var text = document.getElementById('alvin_response');
    if (text) {
        var utter = new SpeechSynthesisUtterance(text.textContent);
        window.speechSynthesis.speak(utter);
    }
}
</script>
</body>
</html>
'''

SETTINGS_HTML = '''
<!DOCTYPE html>
<html>
<head><title>Alvin Settings</title></head>
<body>
<h1>Alvin Settings</h1>
<form method="post">
    <label>LLM Model: <input type="text" name="llm_model" value="{{ config.get('llm_model', '') }}"></label><br>
    <label>Voice ID: <input type="text" name="voice_id" value="{{ env.get('VOICE_ID', '') }}"></label><br>
    <label>ElevenLabs API Key: <input type="text" name="elevenlabs_api_key" value="{{ env.get('ELEVENLABS_API_KEY', '') }}"></label><br>
    <input type="submit" value="Save">
</form>
<a href="/">Back to Chat</a>
</body>
</html>
'''

@app.route('/login', methods=['POST'])
def login():
    if request.form['password'] == os.getenv('DASHBOARD_PASSWORD', 'alvin123'):
        session['authed'] = True
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('authed', None)
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    response = None
    if not session.get('authed'):
        return render_template_string(HTML, response=None)
    if request.method == 'POST':
        query = request.form['query']
        response = manager.route(query)
    return render_template_string(HTML, response=response)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    config_path = 'config.json'
    env_path = '.env'
    # Load config
    config = {}
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = json.load(f)
    # Load env
    env = {}
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    k, v = line.strip().split('=', 1)
                    env[k] = v
    if request.method == 'POST':
        # Update config
        config['llm_model'] = request.form['llm_model']
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        # Update env
        env['VOICE_ID'] = request.form['voice_id']
        env['ELEVENLABS_API_KEY'] = request.form['elevenlabs_api_key']
        with open(env_path, 'w') as f:
            for k, v in env.items():
                f.write(f"{k}={v}\n")
        return redirect(url_for('settings'))
    return render_template_string(SETTINGS_HTML, config=config, env=env)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
