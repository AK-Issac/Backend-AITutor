Voici votre **README.md** complet avec toutes les instructions :  

```md
# 🚗 Voiture AI Backend

## 📌 Prérequis

Avant de commencer, assurez-vous d'avoir installé :  
- **Python 3.x**  
- **Pip 25.0 ou supérieur**  
- **Git**  
- **Ollama** (disponible sur [ollama.com](https://ollama.com))

---

## ⚡ Installation

### 1️⃣ **Cloner le Dépôt**
```sh
git clone https://github.com/AK-Issac/Backend-AITutor
cd Backend-AITutor
```

---

### 2️⃣ **Créer un Environnement Virtuel**

#### ✅ Windows :
```sh
python -m venv venv
```

#### ✅ Linux/Mac :
```sh
python3 -m venv venv
```

---

### 3️⃣ **Activer l'Environnement Virtuel**

#### ✅ Windows :
```sh
venv\Scripts\activate
```

#### ✅ Linux/Mac :
```sh
source venv/bin/activate
```

---

### 4️⃣ **Installer les Dépendances**
```sh
pip install -r requirements.txt
```

---

## 🚀 Installation et Configuration d'Ollama

### 5️⃣ **Installer Ollama**
Téléchargez et installez Ollama depuis [ollama.com](https://ollama.com).  

Ensuite, ouvrez votre terminal et exécutez :  
```sh
ollama --version
```
Si la commande fonctionne, Ollama est bien installé.

---

### 6️⃣ **Télécharger le modèle LLaMA**
Exécutez cette commande pour télécharger **LLaMA 3.2** :  
```sh
ollama pull llama3.2
```
Vous pouvez vérifier que le modèle est bien installé avec :  
```sh
ollama list
```

---

### 7️⃣ **Tester Ollama en ligne de commande**
Avant d'intégrer Ollama dans Flask, testons-le directement :  
```sh
ollama run llama3.2
```
Si la commande affiche une réponse générée par l'IA, tout est bon ! 🚀

---

## 🏗️ Lancer le Serveur Flask

### 8️⃣ **Démarrer Ollama en mode serveur**
Ollama doit être actif avant de lancer Flask. Ouvrez un terminal et exécutez :  
```sh
ollama serve
```

---

### 9️⃣ **Lancer l'API Flask**
Dans un autre terminal, démarrez l'API Flask avec :  
```sh
python main.py
```
Votre serveur sera accessible sur `http://127.0.0.1:8000`.

---

## 🛠️ Tester avec Postman

1. **Ouvrir Postman**  
2. **Sélectionner "POST"**  
3. **Entrer l'URL suivante** :  
   ```
   http://127.0.0.1:8000/api/chat
   ```
4. **Aller dans l'onglet "Body" → Sélectionner "raw" → Choisir "JSON"**  
5. **Entrer ce JSON comme requête** :  
   ```json
   {
       "message": "Bonjour, comment vas-tu ?"
   }
   ```
6. **Cliquer sur "Send"** 🚀  

Si tout fonctionne, vous recevrez une réponse de LLaMA comme ceci :  
```json
{
    "response": "Bonjour ! Je vais bien, merci de demander. Comment puis-je vous aider ?"
}
```

---

## 🔍 Dépannage

Si vous avez une erreur, vérifiez les points suivants :

✅ **Ollama est-il bien installé ?**  
```sh
ollama --version
```

✅ **Le modèle est-il bien téléchargé ?**  
```sh
ollama list
```

✅ **Ollama est-il en cours d'exécution ?**  
```sh
ollama serve
```

✅ **Le serveur Flask est-il lancé ?**  
```sh
python main.py
```

---

## 🚫 Désactiver l'Environnement Virtuel
Si vous souhaitez quitter l'environnement virtuel, exécutez :  
```sh
deactivate
```

---

🎉 **Félicitations !** Votre API Flask avec LLaMA fonctionne parfaitement ! 🚀
```

Tout est bien structuré et prêt à être utilisé sur **GitHub** ! 🎯