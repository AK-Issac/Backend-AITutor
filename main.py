from flask import Flask
from flask_cors import CORS
from lib.chat import sendComprehension
from lib.Redaction import send 
from lib.Redaction import send2
from lib.speech_recognition import transcribe
from lib.lecture import answerquestion, askquestion

app = Flask(__name__)
CORS(app)

# API Endpoint pour analyser la reformulation
app.add_url_rule('/api/redaction1', 'send',send, methods=['POST'])
app.add_url_rule('/api/redaction2', 'send2', send2, methods=['POST'])
app.add_url_rule('/api/comprehension', 'sendComprehension', sendComprehension, methods=['POST'])
app.add_url_rule('/api/lecture/transcribe', 'transcribe', transcribe, methods=['POST'])
app.add_url_rule('/api/lecture/answerquestion', 'answerquestion', answerquestion, methods=['POST'])
app.add_url_rule('/api/lecture/askquestion', 'askquestion', askquestion, methods=['POST'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)