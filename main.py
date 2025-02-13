from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

# API Endpoint for Chat using Ollama
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get("message", "")

    if not prompt:
        return jsonify({"error": "Message is required"}), 400

    # Use Ollama's command-line interface to generate a response
    result = subprocess.run(["ollama", "run", "llama3.2", prompt], capture_output=True, text=True)

    return jsonify({"response": result.stdout.strip()})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
