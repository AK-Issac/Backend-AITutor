from flask import request, jsonify
from lib.speech_recognition import transcribe_audio
import subprocess
import os

def send():
    data = request.get_json()
    original_text = data.get("original_text", "").strip()
    human_text = data.get("human_text", "").strip()

    if not original_text or not human_text:
        return jsonify({"error": "Les deux textes (original et humain) sont requis."}), 400

    # Définition du contexte pour l'IA
    context = (
        "Vous êtes une IA tuteur de langue française. Votre rôle est d'aider les utilisateurs "
        "à reformuler des textes de manière correcte et naturelle.\n\n"
        "Voici le texte original fourni :\n"
        f"\"{original_text}\"\n\n"
        "Voici la reformulation de l'utilisateur :\n"
        f"\"{human_text}\"\n\n"
        "Analysez cette reformulation et indiquez si elle est correcte ou s'il y a des erreurs. "
        "Si elle est incorrecte, proposez une version améliorée avec des explications claires."
    )

    # Exécution de Ollama avec le contexte et les inputs
    result = subprocess.run(["ollama", "run", "llama3.2", context], capture_output=True, text=True)

    return jsonify({"response": result.stdout.strip()})

def sendComprehension():
    data = request.get_json()
    schema_type = data.get("schema_type", "").strip()  # "actentiel", "narratif", ou "communication"
    schema_data = data.get("schema_data", {})  # Données du schéma

    if not schema_type or not schema_data:
        return jsonify({"error": "Le type de schéma et les données sont requis."}), 400

    # Définition du contexte pour l'IA en fonction du type de schéma
    context = ""
    if schema_type == "actentiel":
        context = (
            "Vous êtes une IA tuteur de langue française. Votre rôle est d'aider les utilisateurs "
            "à analyser un texte en utilisant le schéma actentiel.\n\n"
            "Voici les données fournies par l'utilisateur :\n"
            f"Destinataire : {schema_data.get('destinataire', '')}\n"
            f"Destinateur : {schema_data.get('destinateur', '')}\n"
            f"Héros : {schema_data.get('hero', '')}\n"
            f"Quête : {schema_data.get('quete', '')}\n"
            f"Adjuvant : {schema_data.get('adjuvant', '')}\n"
            f"Opposant : {schema_data.get('opposant', '')}\n\n"
            "Analysez ces éléments et fournissez une réponse structurée."
        )
    elif schema_type == "narratif":
        context = (
            "Vous êtes une IA tuteur de langue française. Votre rôle est d'aider les utilisateurs "
            "à analyser un texte en utilisant le schéma narratif.\n\n"
            "Voici les données fournies par l'utilisateur :\n"
            f"Situation Initiale : {schema_data.get('situationInitiale', '')}\n"
            f"Déroulement : {schema_data.get('deroulement', '')}\n"
            f"Péripétie : {schema_data.get('peripetie', '')}\n"
            f"Dénouement : {schema_data.get('denouement', '')}\n"
            f"Situation Finale : {schema_data.get('situationFinale', '')}\n\n"
            "Analysez ces éléments et fournissez une réponse structurée."
        )
    elif schema_type == "communication":
        context = (
            "Vous êtes une IA tuteur de langue française. Votre rôle est d'aider les utilisateurs "
            "à analyser un texte en utilisant la situation de communication.\n\n"
            "Voici les données fournies par l'utilisateur :\n"
            f"Qui parle ? : {schema_data.get('quiParle', '')}\n"
            f"À qui ? : {schema_data.get('aQui', '')}\n"
            f"Pourquoi ? : {schema_data.get('pourquoi', '')}\n"
            f"Qui fait l'action ? : {schema_data.get('quiFaitAction', '')}\n"
            f"Comment ? : {schema_data.get('comment', '')}\n"
            f"Où ? : {schema_data.get('ou', '')}\n"
            f"Quand ? : {schema_data.get('quand', '')}\n\n"
            "Analysez ces éléments et fournissez une réponse structurée."
        )
    else:
        return jsonify({"error": "Type de schéma non reconnu."}), 400

    # Exécution de Ollama avec le contexte et les inputs
    result = subprocess.run(["ollama", "run", "llama3.2", context], capture_output=True, text=True)

    return jsonify({"response": result.stdout.strip()})

def clear():
    # TODO: Implémenter la logique pour effacer la mémoire de la page actuelle
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