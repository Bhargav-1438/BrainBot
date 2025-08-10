import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure the API key is loaded from environment variables
API_KEY = os.environ.get("OPENROUTER_API_KEY")

app = Flask(__name__)

# Function to call OpenRouter API
def ask_llm(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are BrainBot, a smart assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            print("Error:", response.status_code, response.text)
            return "Sorry, I couldn't process that. Try again later."
    except requests.exceptions.RequestException as e:
        print("Request error:", e)
        return "Sorry, there was an issue with the request. Please try again later."

# Home (Landing) page
@app.route("/", methods=["GET"])
def home():
    return render_template("landing.html")

# Chat Interface Page (GET) + Handle Chat POST
@app.route("/chat", methods=["GET", "POST"])
def chat_interface():
    answer = ""
    if request.method == "POST":
        user_input = request.form.get("question")
        answer = ask_llm(user_input)
    return render_template("chat.html", answer=answer)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)