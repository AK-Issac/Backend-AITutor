from flask import request, jsonify
from lib.speech_recognition import transcribe_audio
import subprocess
import os

context = """
    CONTEXTE GOES HERE
"""
def send():
    data = request.get_json()
    prompt = data.get("message", "")

    if not prompt:
        return jsonify({"error": "Message is required"}), 400

    # Use Ollama's command-line interface to generate a response
    result = subprocess.run([os.getenv("OLLAMA_ROUTE"), "run", "llama3.2", prompt], capture_output=True, text=True)
    print(result)
    return jsonify({"response": result.stdout.strip()})

def clear():
    #TODO Make the clearing for the memory of the current page
    return

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
