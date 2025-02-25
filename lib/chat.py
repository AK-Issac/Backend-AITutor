from flask import request, jsonify
import subprocess
import sys
import locale

# Forcer l'encodage UTF-8 global
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def clear():
    #TODO Make the clearing for the memory of the current page
    return

def sendComprehension():
    data = request.get_json()
    schema_type = data.get("schema_type", "").strip()
    schema_data = data.get("schema_data", {})

    if not schema_type or not schema_data:
        return jsonify({"error": "Le type de schéma et les données sont requis."}), 400

    # Réponses modèles prédéfinies
    model_responses = {
        "actentiel": (
            "Sujet : Marc Carrière\n"
            "Objet : Rejoindre son chalet sans encombre\n"
            "Destinateur : Son désir de repos et d'oubli\n"
            "Destinataire : Lui-même (son bien-être)\n"
            "Adjuvants : La solitude, la musique qui joue à la radio\n"
            "Opposants : L'alcool, la route sinueuse, l'orignal"
        ),
        "narratif": (
            "Situation initiale : Marc roule de nuit sur l'autoroute 55 en direction de son chalet\n"
            "Élément déclencheur : Un orignal surgit soudainement sur la route\n"
            "Péripéties : Marc réalise qu'il va heurter l'animal/L'accident se produit\n"
            "Dénouement : L'orignal atterrit sur le siège passager\n"
            "Situation finale : Marc continue à rouler en état de choc"
        ),
        "communication": (
            "Qui parle ? : Le narrateur (point de vue externe ou interne)\n"
            "À qui ? : Au lecteur du roman\n"
            "Pourquoi ? : Raconter un événement marquant reflétant l'état psychologique\n"
            "Qui fait l'action ? : Marc Carrière\n"
            "Comment ? : En conduisant distrait puis en percutant l'orignal\n"
            "Où ? : Autoroute 55, environnement nocturne\n"
            "Quand ? : Pendant un trajet de nuit vers le chalet"
        )
    }

    # Construction du contexte pédagogique
    context = (
        "Vous êtes un tuteur de français expert en analyse littéraire. "
        "Votre rôle est de comparer la réponse de l'élève avec une réponse modèle "
        "pour l'aider à progresser. Procédez en 4 étapes :\n\n"
        "1. Valider les éléments corrects\n"
        "2. Pointer les erreurs/manques\n"
        "3. Expliquer avec des exemples du texte\n"
        "4. Proposer des pistes d'amélioration\n\n"
        "Réponse de l'élève pour le schéma " + schema_type + " :\n" +
        "\n".join([f"{k} : {v}" for k, v in schema_data.items()]) +
        "\n\nRéponse modèle attendue :\n" + model_responses[schema_type] + 
        "\n\nAnalyse comparative :\n"
        "- Comparez point par point les deux versions\n"
        "- Soulignez les éléments clés manquants dans la réponse élève\n"
        "- Expliquez pourquoi la réponse modèle est pertinente en citant le texte\n"
        "- Restez bienveillant et pédagogique dans vos remarques"
    )

    result = subprocess.run(
    ["ollama", "run", "llama3.2", context],
    capture_output=True,
    text=True,
    encoding='utf-8',  # Forcer l'encodage UTF-8
    errors='replace'   # Remplacer les caractères invalides par un symbole de remplacement
)

    return jsonify({
    "response": result.stdout.strip(),
    "model_response": model_responses[schema_type]
}), 200, {'Content-Type': 'application/json; charset=utf-8'}