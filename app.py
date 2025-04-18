import os
import requests
from flask import Flask, render_template, request
from twilio.twiml.messaging_response import MessagingResponse
import json
from dotenv import load_dotenv  # To load .env variables

# Load environment variables
load_dotenv()

# Ensure the API key is loaded from environment variables
API_KEY = os.environ.get("OPENROUTER_API_KEY")  # Save this in your .env or system environment variables

app = Flask(__name__)

# Function to call OpenRouter API
def ask_llm(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",  # Model choice; you can change this if needed
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

# Load fallback responses for predefined questions
with open("C:/Users/bharg/OneDrive/Documents/New folder/test/project/general_response.json") as f:
    responses = json.load(f)

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
        answer = ask_llm(user_input)  # Use LLM for dynamic responses
    return render_template("chat.html", answer=answer)

# WhatsApp Bot Route
@app.route("/bot", methods=["POST"])
def bot_reply():
    incoming_msg = request.form.get("Body").lower()
    resp = MessagingResponse()
    msg = resp.message()

    response = ask_llm(incoming_msg)  # Use LLM for dynamic responses
    msg.body(response)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
