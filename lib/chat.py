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
