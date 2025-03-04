from flask import request, jsonify
import subprocess
import sys
import locale

# Forcer l'encodage UTF-8 global
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def send():
    data = request.get_json()
    full_text = "Au chalet, je dormirais bien. Me coucherais tôt. Pour la perdrix, pas besoin de se lever aux aurores. Sept, huit heures d’un sommeil sans interruption, sans même un rêve ou deux, sans penser à, ou alors si peu, et de façon générale, dans le cadre global des échecs d’une vie d’amoureux. Le sommeil lui-même étant la chose rêvée. Et la forêt défilait, noire et unie, basculant de chaque côté dans un néant renouvelable qui rendait tangible la fuite contre laquelle luttait ma mémoire. L’effet de l’alcool se décantant peu à peu, je devenais moins alerte et ce n’était pas une bonne idée sur cette route sinueuse hantée par les poids lourds. J’ai baissé la vitre et un filet d’air glacé s’est engouffré à l’intérieur avec la précision d’une lame. Betsi pendant ce temps : Tu es si seul Mon ami Dans ce noir Tu es si seul Mon amour Et moi toujours Je me suis dit c’est un cheval, puis tout de suite non c’est un orignal qui traverse la route et j’ai pensé je vais le, ses pattes interminables et la chose était en train de se produire. Le choc initial fut étrangement ténu, compte tenu de la stature du cervidé fauché à la hauteur de ses grandes pattes grêles, et je voyais comme au ralenti se peindre un air ennuyé sur les traits de la bête tandis qu’un bref envol la soulevait pour la renverser sur le capot. J’ai eu le temps de penser à un détail que j’ai tout de suite oublié mais que sur le coup j’aurais voulu retenir indéfiniment, et l’énorme animal s’écrasait sur le pare-brise, causant un fracas si invraisemblable que j’ai continué de regarder droit devant moi comme si le voyage avait dû se poursuivre normalement, et c’est pourquoi sans doute j’ai réussi à conserver la maîtrise du véhicule alors que l’orignal replié sur lui-même prenait place à côté de moi. Bombardé de grêlons de vitre, couvert d’une fine poussière et éclaboussé de sang chaud, j’ai encore eu le temps de remarquer qu’il s’étirait la patte arrière en une ruade convulsive pour lâcher un bref jet de pisse puissant, en même temps qu’il donnait un grand coup de sabot sur le poste de radio qui s’est tu instantanément. Je roulais maintenant à trente kilomètres à l’heure et je ralentissais encore, ne voulant pas regarder à côté. Je sentais irradier une grande chaleur amère de la masse difforme qui venait d’expirer là sur la banquette : un renâclement indigné suivi d’un gros soupir. J’ai immobilisé la voiture sur le côté de la route, ne comprenant pas encore comment tout cela était possible. Au loin j’apercevais un halo, les phares d’une auto venant en sens inverse. Je suis sorti pour traverser la route en diagonale sans jeter le moindre regard autour de moi, arrachant un coup de klaxon saisissant à un camion qui arrivait juste derrière. J’étais presque étonné de retrouver la rivière à mes pieds, pleine de silencieux clapotis. Je savais si peu ce que je faisais que j’aurais pu me mettre à nager. Il me restait tout juste assez de présence d’esprit pour constater que je tremblais violemment. L’autre automobile avait ralenti et se rapprochait doucement, comme pour ne rien déranger. Je suis revenu sur mes pas, m’avançant ébloui dans le faisceau des phares qui illuminaient toute la scène, ma voiture arrêtée dont le moteur tournait encore et, côté passager, avec ses pattes trop grandes dépassant du pare-brise éventré, comme un géant qui aurait essayé de s’asseoir à la place d’un nain, l’orignal grotesquement recroquevillé, son air innocent qui semblait s’efforcer d’expliquer comment il avait seulement eu l’intention de faire un bout de chemin en ma compagnie, la langue sortie, le cou tout croche, le panache de travers dans la nuit. ; "  # Texte complet de l'histoire
    human_extract = data.get("human_text", "").strip()
    original_extract = data.get("original_text", "").strip()

    if not human_extract or not original_extract:
        return jsonify({"error": "Les deux extraits (humain et original) sont requis."}), 400

    # Construction du contexte d'analyse
    context = (
        "Vous êtes un tuteur de français expert en analyse littéraire. Voici votre mission :\n\n"
        "1. ANALYSE DES EXTRAITS :\n"
        f"TEXTE COMPLET :\n{full_text}\n\n"
        f"EXTRAIT 'HUMAIN' (éléments psychologiques/émotionnels) :\n{human_extract}\n\n"
        f"EXTRAIT 'ORIGINAL' (éléments narratifs/clés) :\n{original_extract}\n\n"
        
        "2. CONSIGNES D'ANALYSE :\n"
        "a) Pour l'extrait 'Humain' :\n"
        "- Vérifier si les surlignages correspondent bien à des éléments psychologiques\n"
        "- Identifier les émotions/motivations du personnage\n"
        "- Relier chaque élément à des passages précis du texte\n\n"
        
        "b) Pour l'extrait 'Original' :\n"
        "- Vérifier la pertinence narrative des éléments choisis\n"
        "- Identifier les procédés littéraires utilisés\n"
        "- Analyser leur rôle dans la construction du récit\n\n"
        
        "3. STRUCTURE DE RÉPONSE :\n"
        "✅ Validation des bonnes réponses\n"
        "📌 Éléments manquants/erreurs\n"
        "📖 Explications textuelles (avec citations)\n"
        "💡 Suggestions d'amélioration\n\n"
        
        "EXEMPLE DE RÉPONSE :\n"
        "=== Analyse Humaine ===\n"
        "✅ Vous avez bien identifié la solitude de Marc ('si seul mon amour')\n"
        "📌 Manque la dualité fatigue/alcool (ligne 22)\n"
        "📖 La 'mémoire qui lutte' (l.14) montre...\n\n"
        "=== Analyse Originale ===\n"
        "✅ Bon choix de l'image de l'orignal symbole\n"
        "📌 Oubli du motif de la route sinueuse\n"
        "💡 Ajouter la symbolique des phares (l.45)..."
    )

    # Exécution de l'analyse
    try:
        result = subprocess.run(["ollama", "run", "llama3.2", context], capture_output=True, text=True, encoding="utf-8", check=True)
        return jsonify({
            "response": result.stdout.strip(),
            "analysis": {
                "human": extract_section(result.stdout, "Analyse Humaine"),
                "original": extract_section(result.stdout, "Analyse Originale")
            }
        }), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        print("Erreur lors de l'exécution de subprocess.run :", str(e))  # Log pour débogage
        return jsonify({"error": str(e)}), 500

def extract_section(text, section_name):
    # Fonction utilitaire pour parser la réponse structurée
    start = text.find(f"=== {section_name} ===")
    end = text.find("===", start + 1)
    return text[start:end] if start != -1 else "Section non trouvée"

def send2():
    data = request.get_json()
    print("Données reçues :", data)  # Log pour débogage

    original_text = data.get("original_text", "").strip()
    human_text = data.get("human_text", "").strip()
    student_plan = data.get("form_data", {})  # Structure du plan élève

    if not original_text or not human_text:
        return jsonify({"error": "Les deux textes (original et humain) sont requis."}), 400

    # Réponse modèle et question d'analyse
    question_analyse = "Est-il vrai que le personnage de Marc perçoit l'accident avec l'orignal comme une métaphore de sa propre vie ?"
    
    modele_reponse = {
        "these": "Oui, l'accident avec l'orignal est une métaphore de la vie de Marc, reflétant son état d'esprit et ses échecs personnels.",
        "arguments": [
            {
                "nom": "Perte de contrôle",
                "sous_arguments": [
                    {
                        "texte": "L'accident est soudain et chaotique comme ses échecs amoureux",
                        "preuve": "« Je me suis dit c'est un cheval... » (confusion similaire à ses relations)"
                    },
                    {
                        "texte": "Tentative de garder le contrôle post-impact",
                        "preuve": "« J'ai continué de regarder droit devant moi... »"
                    }
                ]
            },
            {
                "nom": "Symbolique de l'orignal",
                "sous_arguments": [
                    {
                        "texte": "L'orignal représente les ambitions contrariées",
                        "preuve": "Comparaison géant/nain"
                    },
                    {
                        "texte": "Résignation face au destin",
                        "preuve": "« air ennuyé sur les traits de la bête »"
                    }
                ]
            }
        ]
    }

    # Construction du contexte d'analyse
    context = (
        "Vous êtes un expert en analyse littéraire. Voici votre mission :\n\n"
        "1. QUESTION D'ANALYSE :\n"
        f"{question_analyse}\n\n"
        
        "2. TEXTE COMPLET :\n"
        f"{original_text}\n\n"
        
        "3. PLAN ÉLÈVE À ANALYSER :\n"
        f"Thèse : {student_plan.get('ideePrincipale1', '')}\n"
        "Arguments :\n"
        f"- {student_plan.get('sousArgument1_1', '')} | Preuve: {student_plan.get('preuve1_1', '')}\n"
        f"- {student_plan.get('sousArgument1_2', '')} | Preuve: {student_plan.get('preuve1_2', '')}\n"
        f"- {student_plan.get('sousArgument2_1', '')} | Preuve: {student_plan.get('preuve2_1', '')}\n"
        f"- {student_plan.get('sousArgument2_2', '')} | Preuve: {student_plan.get('preuve2_2', '')}\n\n"
        
        "4. MODÈLE DE RÉPONSE :\n"
        f"Thèse : {modele_reponse['these']}\n"
        "Arguments modèles :\n"
        f"- {modele_reponse['arguments'][0]['nom']}: {modele_reponse['arguments'][0]['sous_arguments'][0]['texte']}\n"
        f"- {modele_reponse['arguments'][1]['nom']}: {modele_reponse['arguments'][1]['sous_arguments'][0]['texte']}\n\n"
        
        "5. CONSIGNES D'ANALYSE :\n"
        "a) Comparer structure argumentative\n"
        "b) Vérifier pertinence des preuves citées\n"
        "c) Analyser la compréhension de la métaphore\n"
        "d) Proposer des améliorations structurées\n\n"
        
        "6. FORMAT DE RÉPONSE ATTENDU :\n"
        "✅ Points forts\n"
        "📌 Éléments manquants\n"
        "📖 Suggestions d'amélioration\n"
        "💡 Conseils méthodologiques"
    )

    # Exécution de l'analyse
    try:
        result = subprocess.run(["ollama", "run", "llama3.2", context], capture_output=True, text=True, encoding="utf-8", check=True)
        
        return jsonify({
            "response": result.stdout.strip(),
            "model_reponse": modele_reponse,
            "question_analyse": question_analyse
        }), 200, {'Content-Type': 'application/json; charset=utf-8'}
        
    except Exception as e:
        print("Erreur lors de l'exécution de subprocess.run :", str(e))  # Log pour débogage
        return jsonify({"error": str(e)}), 500
