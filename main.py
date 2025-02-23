from flask import Flask
from flask_cors import CORS
from lib.chat import send, answerquestion, askquestion, sendComprehension
from lib.speech_recognition import transcribe

app = Flask(__name__)
CORS(app)

# API Endpoint pour analyser la reformulation
app.add_url_rule('/api/chat', 'send', send, methods=['POST'])
app.add_url_rule('/api/redaction', 'sendComprehension', sendComprehension, methods=['POST'])
app.add_url_rule('/api/lecture/transcribe', 'transcribe', transcribe, methods=['POST'])
app.add_url_rule('/api/lecture/answerquestion', 'answerquestion', answerquestion, methods=['POST'])
app.add_url_rule('/api/lecture/askquestion', 'askquestion', askquestion, methods=['POST'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)