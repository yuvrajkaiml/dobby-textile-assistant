import os
import json
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from llm_provider import LLMProviderFactory
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
        provider_name = get_provider_name()
        provider = LLMProviderFactory.get_provider(provider_name)
        reply = provider.get_response(messages)
        
        # Try to parse the reply as JSON
        try:
            # Clean up potential markdown code blocks
            clean_reply = reply.strip()
            if clean_reply.startswith("```json"):
                clean_reply = clean_reply[7:]
            if clean_reply.startswith("```"):
                clean_reply = clean_reply[3:]
            if clean_reply.endswith("```"):
                clean_reply = clean_reply[:-3]
                
            structured_reply = json.loads(clean_reply)
            return jsonify({'reply': reply, 'structured': structured_reply})
        except json.JSONDecodeError:
            # Fallback for when LLM fails to output valid JSON
            return jsonify({'reply': reply, 'structured': None})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', '5000'))
    debug = os.getenv('FLASK_DEBUG', '1') == '1'
    app.run(host=host, port=port, debug=debug)
