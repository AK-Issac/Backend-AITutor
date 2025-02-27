#  AI Backend

## Prerequisites
- **Python 3.x**  
- **Pip 25.0**  
- **Git**  
- **C++ Compiler** (Available on [visualstudio.microsoft.com](https://visualstudio.microsoft.com/vs/features/cplusplus/))
- **Ollama** (Available on [ollama.com](https://ollama.com))
- **FFmpeg** (Available on [github.com](https://github.com/BtbN/FFmpeg-Builds/releases))
---

## Installation Guide

## Installation and Ollama Configuration

### 1. **Install Ollama**
Download and install Ollama from [ollama.com](https://ollama.com).  

Now execute :  
```sh
ollama --version
```
If the command works, you're good to go

---

### 2. **Download the LLama Model**
Execute this command to install **LLaMA 3.2** :  
```sh
ollama pull llama3.2
```
You can verify the installation with :  
```sh
ollama list
```

---

## Installation and FFmpeg Configuration 

### 1. **Install FFmpeg Build**
Download and install FFmpeg from [github.com](https://github.com/BtbN/FFmpeg-Builds/releases).

#### Windows :
Install **ffmpeg-master-latest-win64-gpl-shared.zip**

#### Linux :
Install **ffmpeg-master-latest-linux64-gpl-shared.tar.xz**

---

### 2. **Configurate environment variables**
Extract the folder and add the bin to system PATH

---

## Vosk installation

### 1. **Install Vosk**
Download and install Vosk from [alphacephei.com](https://alphacephei.com/vosk/models).
French
vosk-model-fr-0.22

---

### 2. **Add Vosk to the project**
Extract the folder, create a folder named **models** in the project folder and add Vosk to it

---

## Project Installation

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

## Running the Application

### 1. **Run Ollama in server mode**
Ollama needs to run before running Flask. Open a terminal and run :  
```sh
ollama serve
```

---

### 2. **Launch Flask API**
In another terminal, start Flask API with :  
```sh
python main.py
```
Your server will be accessible on `http://127.0.0.1:8000`.

## Debugging

If you have errors, verify the following points :

✅ **Is FFmpegtalled correctly ?**  
```sh
ffmpeg -version
```

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
