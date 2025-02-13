#  AI Backend

## Prerequisites
- **Python 3.x**  
- **Pip 25.0**  
- **Git**  
- **Ollama** (Available on [ollama.com](https://ollama.com))

---

## Installation Guide

### 1. **Clone the Repository**
```sh
git clone https://github.com/AK-Issac/Backend-AITutor
cd Backend-AITutor
```

---

### 2. **Create a Virtual Environment**

#### Windows :
```sh
python -m venv venv
```

#### Linux/Mac :
```sh
python3 -m venv venv
```

---

### 3. **Activate the Virtual Environment**

#### Windows :
```sh
venv\Scripts\activate
```

#### Linux/Mac :
```sh
source venv/bin/activate
```

---

### 4. **Install Dependencies**
```sh
pip install -r requirements.txt
```

---

## Installation and Ollama Configuration 

### 5. **Install Ollama**
Download and install Ollama from [ollama.com](https://ollama.com).  

Now execute :  
```sh
ollama --version
```
If the command works, you're good to go

---

### 6. **Download the LLama Model**
Execute this command to install **LLaMA 3.2** :  
```sh
ollama pull llama3.2
```
You can verify the installation with :  
```sh
ollama list
```

---

### 7. **Test Ollama in Command Line Interface**
Avant d'intégrer Ollama dans Flask, testons-le directement :  
```sh
ollama run llama3.2
```
Si la commande affiche une réponse générée par l'IA, tout est bon ! 🚀

---

## Running the Application

### 7. **Run Ollama in server mode**
Ollama needs to run before running Flask. Open a terminal and run :  
```sh
ollama serve
```

---

### 8. **Launch Flask API**
In another terminal, start Flask API with :  
```sh
python main.py
```
Your server will be accessible on `http://127.0.0.1:8000`.

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

## Debugging

If you have errors, verify the following points :

✅ **Is Ollama installed correctly ?**  
```sh
ollama --version
```

✅ **Is the model installed correctly ?**  
```sh
ollama list
```

✅ **Is Ollama running in server mode ?**  
```sh
ollama serve
```

✅ **Is the Flask server running ?**  
```sh
python main.py
```

## Deactivating the Virtual Environment

To deactivate the virtual environment, run:

```sh
deactivate
```
