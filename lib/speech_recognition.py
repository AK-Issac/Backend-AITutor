import os
import json
from vosk import Model, KaldiRecognizer
import wave

# Load the Vosk model
MODEL_PATH = os.path.join("models", "vosk-model-fr-0.22")
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Vosk model not found at {MODEL_PATH}. Please download the model.")

model = Model(MODEL_PATH)

def transcribe_audio(audio_file_path):
    """
    Transcribe an audio file using Vosk.
    """
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Audio file not found at {audio_file_path}")

    # Open the audio file
    wf = wave.open(audio_file_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000]:
        raise ValueError("Audio file must be WAV format, mono, 16-bit, and 8kHz or 16kHz.")

    # Initialize the recognizer
    rec = KaldiRecognizer(model, wf.getframerate())

    # Process the audio file
    transcription = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            transcription.append(result.get("text", ""))

    # Get the final result
    final_result = json.loads(rec.FinalResult())
    transcription.append(final_result.get("text", ""))

    return " ".join(transcription).strip()