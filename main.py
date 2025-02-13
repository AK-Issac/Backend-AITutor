from flask import Flask
from flask_cors import CORS
from lib.chat import send

app = Flask(__name__)
CORS(app)

# API Endpoint for Chat using Ollama
app.add_url_rule('/api/chat', 'send', send,  methods=['POST'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
