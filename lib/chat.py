from flask import request, jsonify
import subprocess
import os

context = """
    CONTEXTE GOES HERE
"""
def send():
    data = request.get_json()
    prompt = data.get("message", "")

    if not prompt:
        return jsonify({"error": "Message is required"}), 400

    # Use Ollama's command-line interface to generate a response
    result = subprocess.run([os.getenv("OLLAMA_ROUTE"), "run", "llama3.2", prompt], capture_output=True, text=True)
    print(result)
    return jsonify({"response": result.stdout.strip()})

def clear():
    #TODO Make the clearing for the memory of the current page
    return