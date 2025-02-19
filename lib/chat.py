from flask import request, jsonify
import subprocess

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

def clear():
    #TODO Make the clearing for the memory of the current page
    return