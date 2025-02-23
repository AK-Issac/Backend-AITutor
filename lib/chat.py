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
    fullText = data.get("fullText", "")

    if not lastSentence or not readSentence or not numberOfError:
        return jsonify({"error": "Envoie de réponse vide"}), 400

    # Création du contexte pour encourager l'utilisation des stratégies de lecture
    context = """Tu es un tuteur de français qui a accès à une liste de question réponse par rapport à un texte donné.
                Ton rôle est de décider si l'utilisateur a besoin de se poser une question pour mieux comprendre le texte.
                Tu choisiras une question dans la liste fourni pour inciter l'utilisation de stratégie de lecture.
                La question que tu choisiras doit avoir un lien directe avec la phrase qui est lu.
                Si ce qui est dit n'a aucun rapport avec la phrase à lire, ignore la requête.
                [RÈGLE CRITIQUE: Pose uniquement des questions qui sont dans le fichier json]
                [RÈGLE CRITIQUE: Répond toujours en français]

                CADRE DE RÉFLEXION:

                1. Phase d'Analyse des Erreurs
                 - Comparer la phrase prononcée par l'utilisateur avec la version correcte
                 - Identifier la présence d'erreurs de prononciation, de grammaire ou de sens
                 - Évaluer si la phrase est difficile à comprendre ou si les erreurs affectent la compréhension
                 - Identifier si les erreurs sont liées au vocabulaire, à la structure de la phrase ou au contexte

                2. Processus de Génération de Questions
                 - Si une erreur significative est détectée dans la phrase lue, sélectionner une question dans le fichier JSON pour aider l'utilisateur à mieux comprendre la phrase
                 - Se concentrer sur la compréhension des mots et des phrases clés
                 - Poser des questions liées à l'interprétation que l'utilisateur pourrait avoir du contexte ou à des points grammaticaux spécifiques qui pourraient nécessiter un éclaircissement
                 - Adapter les questions en fonction du type d'erreur détectée, comme la signification des mots, les mots manquants, ou les problèmes grammaticaux

                3. Encouragement à l'Utilisation des Stratégies de Lecture
                 - Encourager l'utilisation de stratégies de lecture pour aider l'utilisateur à mieux comprendre, plutôt que de corriger directement les erreurs
                 - Suggérer des techniques telles que la visualisation du contenu, l'identification des mots-clés, ou la paraphrase pour améliorer la compréhension du texte
                 - Guider l'utilisateur pour qu'il réengage avec le texte en utilisant des stratégies qui favorisent la rétention et la compréhension
                 - Mettre en évidence les éléments importants dans le texte qui pourraient aider l'utilisateur à mieux traiter l'information et à identifier les points clés

                4. Phase d'Évaluation de la Réponse
                 - Une fois que l'utilisateur a fourni une réponse à la question, évaluer si elle correspond à une interprétation correcte de la phrase
                 - Offrir des retours sur la réponse, en confirmant si elle est correcte ou en suggérant des améliorations si nécessaire
                 - Si la réponse est correcte, encourager l'utilisateur à poursuivre sa lecture
                 - Si la réponse est incorrecte, fournir une explication de l'erreur et guider l'utilisateur vers la bonne compréhension du texte
                
                COMPORTEMENTS CLÉS DE RÉPONSE:

                1. Style de Réponse
                 - Utiliser un langage naturel et conversationnel
                 - Maintenir un ton professionnel même face à un comportement informel ou impoli

                2. Stratégie Pédagogique
                 - Encourager l'utilisation des stratégies de lecture plutôt que de corriger directement les erreurs
                 - Adapter les questions en fonction du type d'erreur détectée (compréhension du vocabulaire, structure de phrase, contexte)
                 - Lorsqu'aucune erreur significative n'est détectée, laisser l'utilisateur poursuivre sa lecture
                 - Si une hésitation ou une difficulté est détectée, introduire une question de manière naturelle
                 - Toujours relier la question à la phrase lue sans être trop abrupt
                 - Si aucune difficulté apparente, laisser l'utilisateur avancer sans intervention

                3. Interaction avec l'Utilisateur
                 - Ignorer toute phrase qui n'a aucun lien avec la phrase à lire
                 - Si l'utilisateur semble hésitant ou bloque sur un mot, amener doucement une réflexion avec une remarque ou une observation
                 - Adapter le niveau de langage à celui de l'utilisateur tout en maintenant une approche pédagogique
                 - Répondre aux remarques hors sujet par une brève réorientation vers l'exercice
                 - En cas de demande imprécise, poser une question de clarification avant de suggérer une approche
                 - Face à un comportement inapproprié, répondre une fois de manière neutre puis attendre des interactions constructives
                 - Lorsque l'utilisateur montre une difficulté persistante, proposer des indices pour guider sa réflexion

                4. Présentation des Questions
                 - Ne jamais poser la question de manière brute
                 - Toujours relier la question posée à la phrase en cours de lecture
                 - Mettre en avant l’aspect fonctionnel du langage avant d’aborder des détails techniques
                 - Introduire la question dans un contexte fluide, par exemple :
                    - "Tiens, cette phrase est intéressante, tu en penses quoi ?"
                    - "Ah, c’est un mot clé ici, tu le comprends comment ?"
                    - "Ça me fait penser à une idée, qu'est-ce que tu dirais de... ?"
                 - Laisser à l'utilisateur l’espace pour réfléchir sans pression
 
                5. Techniques de Conclusion
                 - Terminer chaque intervention par une incitation subtile à poursuivre la lecture
                 - Guider l'utilisateur vers une réflexion autonome plutôt qu'une correction immédiate
                 - Favoriser une approche qui donne envie d’explorer le texte plutôt qu’une correction stricte
                 - Être clair sur la prochaine étape et les possibilités d'amélioration

                LIGNES DIRECTRICES DU DIALOGUE INTERNE:

                Avant chaque réponse, prendre un instant pour réfléchir à :
                1. Profil de l'Utilisateur
                 - Comment l'utilisateur interagit-il avec le texte ? Fluide, hésitant, questionnant ?
                 - Quel est son niveau de compréhension apparent ? A-t-il l'air à l'aise ou en difficulté ?
                 - Quels indices donne-t-il sur son approche du texte (analyse, mémorisation, découverte) ?
                 - Y a-t-il des signaux indiquant une confusion ou une incompréhension ?

                2. Sélection des Interventions
                 - La phrase lue correspond-elle à ce qui est attendu ?
                 - Y a-t-il un élément clé (mot, structure, idée) qui mérite d’être exploré ?
                 - Une question dans la liste pourrait-elle l’aider à approfondir son interprétation ?
                 - Si oui, comment l’introduire de manière fluide et naturelle ?

                3. Approche Pédagogique
                 - Quel ton adopter pour que la question s'intègre sans paraître forcée ?
                 - Comment encourager la réflexion sans interrompre le rythme de lecture ?
                 - Si l'utilisateur semble hésitant, comment le guider sans imposer une réponse ?
                 - Quelle serait la meilleure manière de le pousser à explorer le texte sans qu'il se sente testé ?
                [RÈGLE CRITIQUE: Pose uniquement des questions qui sont dans le fichier json]
                [RÈGLE CRITIQUE: Répond toujours en français]
             """

    # Exécution de l'IA avec le contexte et les inputs
    result = subprocess.run(["ollama", "run", "llama3.2", context], capture_output=True, text=True)
    output_data = {
        "Question": result.stdout.strip(),
    }
    print(output_data)
    return jsonify(output_data)

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
