import os
import json
from vosk import Model, KaldiRecognizer
from flask import request, jsonify
import subprocess
import wave

# Load the Vosk model
MODEL_PATH = os.path.join("models", "vosk-model-fr-0.22")
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Vosk model not found at {MODEL_PATH}. Please download the model.")

model = Model(MODEL_PATH)

def convert_audio_to_wav(input_path, output_path):
    """
    Converts any audio file to WAV format with correct specs.
    """
    command = [
        "ffmpeg", "-i", input_path,
        "-ac", "1", "-ar", "16000", "-sample_fmt", "s16",
        output_path
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

def transcribe():
    """
    Endpoint for speech recognition.
    """
    if "file" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["file"]
    if audio_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded file temporarily
    temp_audio_path = os.path.join("temp", audio_file.filename)
    os.makedirs("temp", exist_ok=True)
    audio_file.save(temp_audio_path)

    # Convert to WAV
    converted_audio_path = os.path.join("temp", "converted.wav")
    try:
        convert_audio_to_wav(temp_audio_path, converted_audio_path)
        print(f"Converted audio saved at: {converted_audio_path}")

        # Transcribe the converted file
        transcription = transcribe_audio(converted_audio_path)
        print(f"Transcription result: {transcription}")
        return jsonify({"transcription": transcription})
    except Exception as e:
        print(f"Error during transcription: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        # Clean up temporary files
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
        if os.path.exists(converted_audio_path):
            os.remove(converted_audio_path)

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