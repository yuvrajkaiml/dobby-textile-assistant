import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from groq_client import get_response
from config import SYSTEM_PROMPT, get_provider_name

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'provider': get_provider_name()})


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    messages = data.get('messages', [])
    # ensure there's at least a system message
    if not any(m.get('role') == 'system' for m in messages):
        messages.insert(0, { 'role': 'system', 'content': SYSTEM_PROMPT })
    try:
        reply = get_response(messages)
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', '5000'))
    debug = os.getenv('FLASK_DEBUG', '1') == '1'
    app.run(host=host, port=port, debug=debug)
