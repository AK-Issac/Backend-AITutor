from flask import request, jsonify
import Levenshtein
import subprocess
import json
import re

def load_questions():
    with open("data/questions.json", "r", encoding="utf-8") as file:
        return json.load(file)

def find_relevant_question(readSentence):
    questions_data = load_questions()
    cleaned_sentence = re.sub(r"<[^>]+>", "", readSentence)  # Remove HTML tags
    cleaned_sentence = re.sub(r"[^\w\s]", "", cleaned_sentence)  # Remove non-alphanumeric characters (punctuation)
    cleaned_sentence = re.sub(r"\s+", " ", cleaned_sentence).strip().lower()  # Remove extra spaces and convert to lower case
    print(f"Processing sentence: {cleaned_sentence}")

    relevant_questions = []
    for obj in questions_data:
        json_sentence = re.sub(r"<[^>]+>", "", obj.get("sentence", "")).lower()  # Clean the sentence from the JSON data
        json_sentence = re.sub(r"[^\w\s]", "", json_sentence)  # Remove non-alphanumeric characters
        json_sentence = re.sub(r"\s+", " ", json_sentence).strip().lower()  # Remove extra spaces and convert to lower case

        distance = Levenshtein.distance(cleaned_sentence, json_sentence)
        if distance <= 10:  # Allow up to 3 edit operations (this can be adjusted)
            questions = obj.get("questions", [])  # Extract the questions list
            for question in questions:
                relevant_questions.append(question.get("question", ""))

    return relevant_questions

def answerquestion() :
    data = request.get_json()
    answer = data.get("answer", "")
    question = data.get("question", "")

    if not answer:
        return jsonify({"error": "Envoie de réponse vide"}), 400

    # Définition du contexte pour l'IA
    context = (
    )

    # Exécution de Ollama avec le contexte et les inputs
    result = subprocess.run(["ollama", "run", "llama3.2", context], capture_output=True, text=True)
    print(result)
    return jsonify(result)

def askquestion():
    data = request.get_json()
    lastSentence = data.get("lastSentence", "")
    readSentence = data.get("readSentence", "")
    numberOfError = data.get("numberOfError", 0)
    relevant_question = find_relevant_question(lastSentence)
    if readSentence == "":
        return "Aucune phrase n'est dite"
    if not lastSentence or not readSentence or not numberOfError:
        return jsonify({"error": "Envoie de réponse vide"}), 400
    if not relevant_question:
        return jsonify({"Question": "Aucune question pertinente", "Relevant Question": relevant_question})

    relevant_question_str = ",".join(relevant_question)
    # Création du contexte modifié pour encourager l'utilisation des stratégies de lecture
    context = """
                - Liste de questions fournies: {relevant_question_str}
                - Dernière phrase lue: "{lastSentence}"
                - Phrase prononcée par l'utilisateur: "{readSentence}"
                - Nombre d'erreurs: {numberOfError}

                Tu es un tuteur de français qui a accès à une liste de questions par rapport à un texte donné.
                Ton rôle est de décider ACTIVEMENT si l’utilisateur a besoin de se poser une question venant de la liste fournie pour mieux comprendre le texte.
                Si aucune question pertinente n’a de lien avec cette phrase, ne pose pas de question.

                [RÈGLE CRITIQUE: Pose uniquement des questions qui sont dans la liste de questions disponibles]
                [RÈGLE CRITIQUE: Répond toujours et uniquement en français]
                [RÈGLE CRITIQUE: Renvoie uniquement une question venant de la liste fournie]
                [RÈGLE CRITIQUE: Aucune explication, raisonnement ou réflexion ne doit être donnée. Renvoie uniquement la question directement sans processus]

                ## CADRE DE RÉFLEXION

                1. Phase d’Analyse des Erreurs
                - Si une erreur est significative, il est nécessaire de poser une question venant de la liste fournie pour clarifier la compréhension.
                - Évalue l'impact de ces erreurs : si elles nuisent à la compréhension du texte, une question venant de la liste fournie doit être posée.

                2. Processus de Génération de Questions
                - Si une erreur significative est détectée, sélectionne une question pertinente dans la liste fournie pour aider l’utilisateur à mieux comprendre le texte.
                - Si aucune erreur n'est présente mais que la phrase est difficile ou ambiguë, propose une question une question venant de la liste fournie pour encourager la réflexion.
                - La question choisie de la liste fournie  doit aider l’utilisateur à approfondir sa compréhension du texte, à explorer un mot clé, ou à clarifier une structure grammaticale.
                - Si aucune question pertinente n’est trouvée, ne pose pas de question.

                3. Approche Pédagogique et Interaction avec l’Utilisateur
                - Si l’utilisateur n’a pas fait d’erreur significative, ne pose pas de question.
                - Si une hésitation ou une difficulté est détectée, réintroduis une question venant de la liste fournie de manière fluide et douce.
                - Si aucune difficulté n’est apparente, ne pose pas de question.
                - Utilise un ton calme et bienveillant même si l’utilisateur fait une erreur. L’objectif est d’encourager la réflexion, pas de forcer une réponse.

                ## LIGNES DIRECTRICES DU DIALOGUE INTERNE:

                Avant chaque réponse, réfléchis à :
                - Les erreurs détectées : Si des erreurs sont présentes, comment peuvent-elles être clarifiées par une question venant de la liste fournie?
                - La question venant de la liste fournie à poser : Est-elle nécessaire pour améliorer la compréhension ou n’interrompt-elle pas trop le flux de lecture ?
                - Si aucune question n’est pertinente, ne pose pas de question.

                [RÈGLE CRITIQUE: Pose uniquement des questions qui sont dans la liste de questions disponibles]
                [RÈGLE CRITIQUE: Répond toujours et uniquement en français]
                [RÈGLE CRITIQUE: Renvoie uniquement une question venant de la liste fournie]
                [RÈGLE CRITIQUE: Aucune explication, raisonnement ou réflexion ne doit être donnée. Renvoie uniquement la question directement sans processus]
            """
    context = context.format(lastSentence=lastSentence, readSentence=readSentence, numberOfError=numberOfError, relevant_question_str=relevant_question_str)
    result = subprocess.run(["ollama", "run", "llama3.2", context], capture_output=True, text=True, encoding="utf-8", check=True)
     # Filter to ensure that the returned question is from the list of relevant questions
    output_question = result.stdout.strip()

    # Ensure the output question is in the list of relevant questions
    if output_question not in relevant_question:
        output_question = "Aucune question pertinente"

    output_data = {
        "Question": result.stdout.strip(),
        "Relevant Question": relevant_question
    }
    print(output_data)
    return jsonify(output_data)