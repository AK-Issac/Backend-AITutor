from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from lib.chat import clear, send
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

load_dotenv()

app = Flask(__name__)
CORS(app)

app.add_url_rule('/api/chat', 'clear', clear, methods=['DELETE'])
app.add_url_rule('/api/chat', 'send', send, methods=['POST'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)